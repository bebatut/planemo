"""Training:tutorial functions."""
import json
import os
import shutil

from nose.tools import assert_raises_regexp

from planemo import cli
from planemo.engine import (
    engine_context,
    is_galaxy_engine,
)
from planemo.runnable import for_path
from planemo.training import Training
from planemo.training.topic import Topic
from planemo.training.tutorial import (
    format_wf_steps,
    get_galaxy_datatype,
    get_hands_on_boxes_from_running_galaxy,
    get_hands_on_boxes_from_local_galaxy,
    get_wf_inputs,
    get_wf_param_values,
    get_zenodo_record,
    Tutorial
)
from planemo.training.utils import (
    load_yaml,
    save_to_yaml
)

from .test_utils import (
    TEST_DATA_DIR
)

datatype_fp = os.path.join(TEST_DATA_DIR, "training_datatypes.yaml")
zenodo_link = 'https://zenodo.org/record/1321885'
# load a workflow generated from Galaxy
WF_FP = os.path.join(TEST_DATA_DIR, "training_workflow.ga")
with open(WF_FP, "r") as wf_f:
    wf = json.load(wf_f)
# load wf_param_values (output of tutorial.get_wf_param_values on wf['steps']['4'])
with open(os.path.join(TEST_DATA_DIR, "training_wf_param_values.json"), "r") as wf_param_values_f:
    wf_param_values = json.load(wf_param_values_f)
# configuration
RUNNABLE = for_path(WF_FP)
CTX = cli.Context()
CTX.planemo_directory = "/tmp/planemo-test-workspace"
KWDS = {
    'topic_name': 'my_new_topic',
    'topic_title': "New topic",
    'topic_target': "use",
    'topic_summary': "Topic summary",
    'tutorial_name': "new_tuto",
    'tutorial_title': "Title of tuto",
    'hands_on': True,
    'slides': True,
    'workflow': None,
    'workflow_id': None,
    'zenodo_link': None,
    'datatypes': os.path.join(TEST_DATA_DIR, "training_datatypes.yaml"),
    'templates': None,
    # planemo configuation
    'conda_auto_init': True,
    'conda_auto_install': True,
    'conda_copy_dependencies': False,
    'conda_debug': False,
    'conda_dependency_resolution': False,
    'conda_ensure_channels': 'iuc,bioconda,conda-forge,defaults',
    'conda_exec': None,
    'conda_prefix': None,
    'conda_use_local': False,
    'brew_dependency_resolution': False,
    'daemon': False,
    'database_connection': None,
    'database_type': 'auto',
    'dependency_resolvers_config_file': None,
    'docker': False,
    'docker_cmd': 'docker',
    'docker_extra_volume': None,
    'docker_galaxy_image': 'quay.io/bgruening/galaxy',
    'docker_host': None,
    'docker_sudo': False,
    'docker_sudo_cmd': 'sudo',
    'engine': 'galaxy',
    'extra_tools': (),
    'file_path': None,
    'galaxy_api_key': None,
    'galaxy_branch': None,
    'galaxy_database_seed': None,
    'galaxy_email': 'planemo@galaxyproject.org',
    'galaxy_root': None,
    'galaxy_single_user': True,
    'galaxy_source': None,
    'galaxy_url': None,
    'host': '127.0.0.1',
    'ignore_dependency_problems': False,
    'install_galaxy': False,
    'job_config_file': None,
    'mulled_containers': False,
    'no_cleanup': False,
    'no_cache_galaxy': False,
    'no_dependency_resolution': True,
    'non_strict_cwl': False,
    'pid_file': None,
    'port': '9090',
    'postgres_database_host': None,
    'postgres_database_port': None,
    'postgres_database_user': 'postgres',
    'postgres_psql_path': 'psql',
    'profile': None,
    'shed_dependency_resolution': False,
    'shed_install': True,
    'shed_tool_conf': None,
    'shed_tool_path': None,
    'skip_venv': False,
    'test_data': None,
    'tool_data_table': None,
    'tool_dependency_dir': None
}
# 
topic = Topic()
training = Training(KWDS)

def test_get_galaxy_datatype():
    """Test :func:`planemo.training.tutorial.get_galaxy_datatype`."""
    assert get_galaxy_datatype("csv", datatype_fp) == "csv"
    assert get_galaxy_datatype("test", datatype_fp) == "strange_datatype"
    assert "# Please add" in get_galaxy_datatype("unknown", datatype_fp)


def test_get_zenodo_record():
    """Test :func:`planemo.training.tutorial.get_zenodo_record`."""
    z_record, req_res = get_zenodo_record(zenodo_link)
    file_link_prefix = "https://zenodo.org/api/files/51a1b5db-ff05-4cda-83d4-3b46682f921f"
    assert z_record == "1321885"
    assert 'files' in req_res
    assert req_res['files'][0]['type'] in ['rdata', 'csv']
    assert file_link_prefix in req_res['files'][0]['links']['self']
    # check with wrong zenodo link
    z_record, req_res = get_zenodo_record('https://zenodo.org/api/records/zenodooo')
    assert z_record is None
    assert 'files' in req_res
    assert len(req_res['files']) == 0
    # using DOI
    z_link = 'https://doi.org/10.5281/zenodo.1321885'
    z_record, req_res = get_zenodo_record(z_link)
    file_link_prefix = "https://zenodo.org/api/files/51a1b5db-ff05-4cda-83d4-3b46682f921f"
    assert z_record == "1321885"
    assert 'files' in req_res
    assert req_res['files'][0]['type'] in ['rdata', 'csv']
    assert file_link_prefix in req_res['files'][0]['links']['self']


def test_get_wf_inputs():
    """Test :func:`planemo.training.tutorial.get_wf_inputs`."""
    step_inp = {
        'tables_1|table': {'output_name': 'output', 'id': 2},
        'add_to_database|withdb': {'output_name': 'output', 'id': 0},
        'tables_0|table': {'output_name': 'output', 'id': 1},
        'add_to_database|tab_0|tt': {'output_name': 'output', 'id': 0},
        'tables_2|section|sect': {'output_name': 'output', 'id': 1},
        'tables_3|tables_0|sect': {'output_name': 'output', 'id': 1}
    }
    step_inputs = get_wf_inputs(step_inp)
    assert 'tables' in step_inputs
    assert '0' in step_inputs['tables']
    assert 'table' in step_inputs['tables']['0']
    assert '2' in step_inputs['tables']
    assert 'section' in step_inputs['tables']['2']
    assert 'sect' in step_inputs['tables']['2']['section']
    assert 'output_name' in step_inputs['tables']['2']['section']['sect']
    assert 'add_to_database' in step_inputs
    assert 'withdb' in step_inputs['add_to_database']
    assert 'tab' in step_inputs['add_to_database']
    assert '0' in step_inputs['add_to_database']['tab']
    assert 'tt' in step_inputs['add_to_database']['tab']['0']


def test_get_wf_param_values():
    """Test :func:`planemo.training.tutorial.get_wf_param_values`."""
    wf_step = wf['steps']['4']
    wf_param_value_tests = get_wf_param_values(wf_step['tool_state'], get_wf_inputs(wf_step['input_connections']))
    assert wf_param_values == wf_param_value_tests


def test_format_wf_steps():
    """Test :func:`planemo.training.tutorial.format_wf_steps`."""
    assert is_galaxy_engine(**KWDS)
    with engine_context(CTX, **KWDS) as galaxy_engine:
        with galaxy_engine.ensure_runnables_served([RUNNABLE]) as config:
            workflow_id = config.workflow_id(WF_FP)
            wf = config.gi.workflows.export_workflow_dict(workflow_id)
            body = format_wf_steps(wf, config.gi)
    assert '## Sub-step with **FastQC**' in body
    assert '## Sub-step with **Query Tabular**' in body
    assert '## Sub-step with **Select first**' in body


def test_get_hands_on_boxes_from_local_galaxy():
    """Test :func:`planemo.training.tutorial.get_hands_on_boxes_from_local_galaxy`."""
    tuto_body = get_hands_on_boxes_from_local_galaxy(KWDS, WF_FP, CTX)
    assert '## Sub-step with **FastQC**' in tuto_body
    assert '## Sub-step with **Query Tabular**' in tuto_body
    assert '## Sub-step with **Select first**' in tuto_body


def test_get_hands_on_boxes_from_running_galaxy():
    """Test :func:`planemo.training.tutorial.get_hands_on_boxes_from_running_galaxy`."""
    assert is_galaxy_engine(**KWDS)
    galaxy_url = 'http://%s:%s' % (KWDS['host'], KWDS['port'])
    with engine_context(CTX, **KWDS) as galaxy_engine:
        with galaxy_engine.ensure_runnables_served([RUNNABLE]) as config:
            wf_id = config.workflow_id(WF_FP)
            tuto_body = get_hands_on_boxes_from_running_galaxy(wf_id, galaxy_url, config.user_api_key)
    assert '## Sub-step with **FastQC**' in tuto_body
    assert '## Sub-step with **Query Tabular**' in tuto_body
    assert '## Sub-step with **Select first**' in tuto_body


def test_tutorial_init():
    """Test :func:`planemo.training.tutorial.tutorial.init`."""
    # with default parameter
    tuto = Tutorial(
        training = training,
        topic = topic)
    assert tuto.name == "new_tuto"
    assert tuto.title == "The new tutorial"
    assert tuto.zenodo_link == ""
    assert tuto.hands_on
    assert not tuto.slides
    assert tuto.init_wf_id is None
    assert tuto.init_wf_fp is None
    assert tuto.datatype_fp == ''
    assert "new_tuto" in tuto.dir
    assert '## Sub-step with **My Tool**' in tuto.body
    assert tuto.data_lib
    # with non default parameter
    tuto = Tutorial(
        training = training,
        topic = topic,
        name="my_tuto",
        title="The tutorial",
        zenodo_link="URL")
    assert tuto.name == "my_tuto"
    assert tuto.title == "The tutorial"
    assert tuto.zenodo_link == "URL"
    assert "my_tuto" in tuto.dir


def test_tutorial_init_from_kwds():
    """Test :func:`planemo.training.tutorial.tutorial.init_from_kwds`."""
    kwds = {
        'tutorial_name': "my_tuto",
        'tutorial_title': "Title of tuto",
        'hands_on': True,
        'slides': True,
        'workflow': WF_FP,
        'workflow_id': 'id',
        'zenodo_link': None,
        'datatypes': datatype_fp
    }
    tuto = Tutorial(
        training = training,
        topic = topic)
    tuto.init_from_kwds(kwds)
    assert tuto.name == "my_tuto"
    assert tuto.title == "Title of tuto"
    assert tuto.zenodo_link == ''
    assert "Which biological questions are addressed by the tutorial?" in tuto.questions
    assert tuto.hands_on
    assert tuto.slides
    assert tuto.init_wf_id == 'id'
    assert tuto.init_wf_fp == WF_FP
    assert tuto.datatype_fp == datatype_fp
    assert "my_tuto" in tuto.dir


def test_tutorial_init_from_existing_tutorial():
    """Test :func:`planemo.training.tutorial.tutorial.init_from_existing_tutorial`."""
    tuto = Tutorial(
        training = training,
        topic = topic)
    assert False
    

def test_tutorial_init_data_lib():
    """Test :func:`planemo.training.tutorial.tutorial.init_data_lib`."""
    tuto = Tutorial(
        training=training,
        topic=topic)
    tuto.init_data_lib()
    assert tuto.data_lib['destination']['type'] == 'library'
    assert tuto.data_lib['items'][0]['name'] == topic.title
    assert tuto.data_lib['items'][0]['items'][0]['name'] == tuto.title
    # from existing data library file
    os.makedirs(tuto.dir)
    save_to_yaml(tuto.data_lib, tuto.data_lib_fp)
    tuto.data_lib = {}
    tuto.init_data_lib()
    assert tuto.data_lib['items'][0]['name'] == topic.title
    assert tuto.data_lib['items'][0]['items'][0]['name'] == tuto.title
    shutil.rmtree("topics")
    # other tutorial already there and add the new one
    tuto.data_lib['items'][0]['items'][0]['name'] == 'Different tutorial'
    tuto.init_data_lib()
    print(tuto.data_lib)
    assert tuto.data_lib['items'][0]['items'][0]['name'] == 'Different tutorial'
    assert tuto.data_lib['items'][0]['items'][1]['name'] == tuto.title



def test_tutorial_get_tuto_metata():
    """Test :func:`planemo.training.tutorial.tutorial.get_tuto_metata`."""
    tuto = Tutorial(
        training=training,
        topic=topic)
    tuto.questions = ['q1', 'q2']
    metadata = tuto.get_tuto_metata()
    assert 'title: The new tutorial' in metadata
    assert '- q1' in metadata


def test_tutorial_set_dir_name():
    """Test :func:`planemo.training.tutorial.tutorial.set_dir_name`."""
    tuto = Tutorial(
        training=training,
        topic=topic)
    tuto.name = "the_tuto"
    tuto.set_dir_name()
    assert tuto.name in tuto.dir
    assert tuto.name in tuto.tuto_fp
    assert tuto.name in tuto.slide_fp
    assert tuto.name in tuto.data_lib_fp
    assert tuto.name in tuto.wf_dir
    assert tuto.name in tuto.wf_fp


def test_tutorial_exists():
    """Test :func:`planemo.training.tutorial.tutorial.exists`."""
    # default
    tuto = Tutorial(
        training=training,
        topic=topic)
    assert not tuto.exists()
    # after dir creation
    os.makedirs(tuto.dir)
    assert tuto.exists()
    shutil.rmtree("topics")


def test_tutorial_has_workflow():
    """Test :func:`planemo.training.tutorial.tutorial.has_workflow`."""
    # default
    tuto = Tutorial(
        training=training,
        topic=topic)
    assert not tuto.has_workflow()
    # 
    tuto.init_wf_fp = WF_FP
    assert tuto.has_workflow()
    # 
    tuto.init_wf_fp = None
    tuto.init_wf_id = ''
    assert not tuto.has_workflow()
    # 
    tuto.init_wf_id = 'ID'
    assert tuto.has_workflow()


def test_tutorial_export_workflow_file():
    """Test :func:`planemo.training.tutorial.tutorial.export_workflow_file`."""
    tuto = Tutorial(
        training=training,
        topic=topic)
    os.makedirs(tuto.dir)
    # with worflow fp
    tuto.init_wf_fp = WF_FP
    tuto.export_workflow_file()
    assert os.path.exists(tuto.wf_fp)
    # with workflow id
    tuto.init_wf_fp = None
    os.remove(tuto.wf_fp)
    assert is_galaxy_engine(**KWDS)
    galaxy_url = 'http://%s:%s' % (KWDS['host'], KWDS['port'])
    with engine_context(CTX, **KWDS) as galaxy_engine:
        with galaxy_engine.ensure_runnables_served([RUNNABLE]) as config:
            tuto.init_wf_id = config.workflow_id(WF_FP)
            tuto.training.galaxy_url = galaxy_url
            tuto.training.galaxy_api_key = config.user_api_key
            tuto.export_workflow_file()
    assert os.path.exists(tuto.wf_fp)
    shutil.rmtree("topics")


def test_tutorial_get_files_from_zenodo():
    """Test :func:`planemo.training.tutorial.tutorial.get_files_from_zenodo`."""
    tuto = Tutorial(
        training=training,
        topic=topic,
        zenodo_link=zenodo_link)
    tuto.datatype_fp = datatype_fp
    files, z_record = tuto.get_files_from_zenodo()
    assert z_record == "1321885"
    # test links
    file_link_prefix = "https://zenodo.org/api/files/51a1b5db-ff05-4cda-83d4-3b46682f921f"
    assert file_link_prefix in tuto.zenodo_file_links[0]
    # test files dict
    assert file_link_prefix in files[0]['url']
    assert files[0]['src'] == 'url'
    assert files[0]['info'] == zenodo_link
    assert "# Please add" in files[0]['ext']
    assert files[1]['ext'] == 'csv'


def test_tutorial_prepare_data_library_from_zenodo():
    """Test :func:`planemo.training.tutorial.tutorial.prepare_data_library_from_zenodo`."""
    assert False

def test_tutorial_write_hands_on_tutorial():
    """Test :func:`planemo.training.tutorial.tutorial.write_hands_on_tutorial`."""
    assert False

def test_tutorial_create_hands_on_tutorial():
    """Test :func:`planemo.training.tutorial.tutorial.create_hands_on_tutorial`."""
    assert False

def test_tutorial_create_tutorial():
    """Test :func:`planemo.training.tutorial.tutorial.create_tutorial`."""
    assert False
