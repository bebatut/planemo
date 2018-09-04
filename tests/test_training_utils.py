"""Training:utils functions."""
import os

from planemo.training.utils import (
    load_yaml,
    Requirement,
    Reference,
    save_to_yaml
)
from .test_utils import (
    TEST_DATA_DIR
)

metadata_fp = os.path.join(TEST_DATA_DIR, "training_metadata_w_zenodo.yaml") 

def test_load_yaml():
    """Test :func:`planemo.training.utils.load_yaml`."""
    metadata = load_yaml(metadata_fp)
    # test if name there
    assert metadata["name"] == "test"
    # test if order of material is conserved
    assert metadata["material"][1]["name"] == "test"


def test_save_to_yaml():
    """Test :func:`planemo.training.utils.save_to_yaml`."""
    metadata = load_yaml(metadata_fp)
    new_metadata_fp = "metadata.yaml"
    save_to_yaml(metadata, new_metadata_fp)
    assert os.path.exists(new_metadata_fp)
    assert 'material' in open(new_metadata_fp, 'r').read()
    os.remove(new_metadata_fp)


def test_requirement_init():
    """Test :func:`planemo.training.utils.Requirement.init`."""
    # test requirement with default parameter
    req = Requirement()
    assert req.title == ""
    assert req.type == "internal"
    assert req.link == "/introduction/"
    # test requirement with non default 
    req = Requirement(title="Introduction", req_type="external", link="URL")
    assert req.title == "Introduction"
    assert req.type == "external"
    assert req.link == "URL"


def test_requirement_export_to_ordered_dict():
    """Test :func:`planemo.training.utils.Requirement.export_to_ordered_dict`."""
    req = Requirement()
    exp_req = req.export_to_ordered_dict()
    assert 'title' in exp_req
    assert exp_req['title'] == ""
    assert 'type' in exp_req
    assert 'link' in exp_req


def test_reference_init():
    """Test :func:`planemo.training.utils.Reference.init`."""
    # test requirement with default parameter
    ref = Reference()
    assert ref.authors == "authors et al"
    assert ref.title == "the title"
    assert ref.link == "link"
    assert ref.summary == "Why this reference is useful"
    # test requirement with non default 
    ref = Reference(authors="the authors", title="a title", link="URL", summary="The summary")
    assert ref.authors == "the authors"
    assert ref.title == "a title"
    assert ref.link == "URL"
    assert ref.summary == "The summary"


def test_reference_export_to_ordered_dict():
    """Test :func:`planemo.training.utils.Reference.export_to_ordered_dict`."""
    ref = Reference()
    exp_ref = ref.export_to_ordered_dict()
    assert 'authors' in exp_ref
    assert 'title' in exp_ref
    assert exp_ref['title'] == "the title"
    assert 'link' in exp_ref
    assert 'summary' in exp_ref
