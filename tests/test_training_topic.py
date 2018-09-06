"""Training:topic functions."""
import os
import shutil

from planemo.training.topic import Topic
from planemo.training.utils import load_yaml
from .test_utils import (
    TEST_DATA_DIR
)


def test_topic_init():
    """Test :func:`planemo.training.topic.Topic.init`."""
    # test requirement with default parameter
    topic = Topic()
    assert topic.name == "new_topic"
    assert topic.type == "use"
    assert topic.title == "The new topic"
    assert topic.summary == "Summary"
    assert topic.docker_image == ""
    assert "maintainers" in topic.maintainers
    assert topic.parent_dir == "topics"
    assert topic.dir == "topics/new_topic"
    assert topic.requirements[0].link == "/introduction/"
    assert topic.references[0].link == "link"
    # test requirement with non default
    topic = Topic(name="topic2", target="admin", title="The 2nd topic", summary="", parent_dir="dir")
    assert topic.name == "topic2"
    assert topic.type == "admin"
    assert topic.title == "The 2nd topic"
    assert topic.summary == ""
    assert topic.parent_dir == "dir"
    assert topic.dir == "dir/topic2"
    assert len(topic.requirements) == 0
    assert len(topic.references) == 0


def test_topic_init_from_kwds():
    """Test :func:`planemo.training.topic.Topic.init_from_kwds`."""
    topic = Topic()
    topic.init_from_kwds({
        'topic_name': "topic",
        'topic_title': "New topic",
        'topic_target': "admin",
        'topic_summary': "Topic summary"
    })
    assert topic.name == "topic"
    assert topic.type == "admin"
    assert topic.title == "New topic"
    assert topic.summary == "Topic summary"
    assert topic.dir == "topics/topic"
    assert len(topic.requirements) == 0
    assert len(topic.references) == 0


def test_topic_get_requirements():
    """Test :func:`planemo.training.topic.Topic.get_requirements`."""
    topic = Topic()
    reqs = topic.get_requirements()
    assert len(reqs) == 1
    assert 'title' in reqs[0]


def test_topic_get_references():
    """Test :func:`planemo.training.topic.Topic.get_references`."""
    topic = Topic()
    refs = topic.get_references()
    assert len(refs) == 1
    assert 'authors' in refs[0]


def test_topic_export_metadata_to_ordered_dict():
    """Test :func:`planemo.training.topic.Topic.export_metadata_to_ordered_dict`."""
    topic = Topic()
    metadata = topic.export_metadata_to_ordered_dict()
    assert 'name' in metadata
    assert metadata['name'] == "new_topic"
    assert 'type' in metadata
    assert 'title' in metadata
    assert 'summary' in metadata
    assert 'requirements' in metadata
    assert 'docker_image' in metadata
    assert 'maintainers' in metadata
    assert 'references' in metadata


def test_topic_exists():
    """Test :func:`planemo.training.topic.Topic.exists`."""
    topic = Topic()
    assert not topic.exists()
    os.makedirs(topic.dir)
    assert topic.exists()
    shutil.rmtree(topic.parent_dir)


def test_topic_create_topic_structure():
    """Test :func:`planemo.training.topic.Topic.create_topic_structure`."""
    topic = Topic()
    topic.create_topic_structure()
    topic_name = "new_topic"
    topic_title = "The new topic"
    # check the folder and its structure
    assert topic.exists()
    assert os.path.exists(topic.img_folder)
    assert os.path.exists(topic.tuto_folder)
    # create the index.md and the topic name
    assert os.path.exists(topic.index_fp)
    assert topic_name in open(topic.index_fp, 'r').read()
    # create the README.md and the topic name
    assert os.path.exists(topic.readme_fp)
    assert topic_title in open(topic.readme_fp, 'r').read()
    # check metadata content
    assert os.path.exists(topic.metadata_fp)
    metadata = load_yaml(topic.metadata_fp)
    assert metadata['name'] == topic_name
    # check dockerfile
    assert os.path.exists(topic.dockerfile_fp)
    assert topic_name in open(topic.dockerfile_fp, 'r').read()
    assert topic_title in open(topic.dockerfile_fp, 'r').read()
    # check introduction slide
    assert os.path.exists(topic.intro_slide_fp)
    assert topic_title in open(topic.intro_slide_fp, 'r').read()
    # check in metadata directory
    assert os.path.exists(os.path.join("metadata", "%s.yaml" % topic_name))
    # clean
    shutil.rmtree(topic.parent_dir)
    shutil.rmtree("metadata")
