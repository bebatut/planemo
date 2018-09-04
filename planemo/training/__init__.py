from planemo.io import info
from .topic import Topic
from .tutorial import Tutorial


class Training:
    'Class to describe a training'

    def __init__(self, kwds):
        self.kwds = kwds
        self.topics_dir = "topics"
        self.topic = Topic(parent_dir=self.topics_dir)
        self.topic.init_from_kwds(self.kwds)
        self.galaxy_url = kwds['galaxy_url']
        self.galaxy_api_key = kwds['galaxy_api_key']

    def init_training(self, ctx):
        """Create/update a topic/tutorial"""
        if not self.topic.exists():
            info("The topic %s does not exist. It will be created" % self.topic.name)
            self.topic.create_topic_structure()

        if not self.kwds['tutorial_name']:
            if self.kwds["slides"]:
                raise Exception("A tutorial name is needed to create the skeleton of a tutorial slide deck")
            if self.kwds['workflow'] or self.kwds['workflow_id']:
                raise Exception("A tutorial name is needed to create the skeleton of the tutorial from a workflow")
            if self.kwds['zenodo_link']:
                raise Exception("A tutorial name is needed to add Zenodo information")
        else:
            self.tuto = Tutorial(training=self, topic=self.topic)
            self.tuto.init_from_kwds(self.kwds)
            if not self.tuto.exists():
                info("The tutorial %s in topic %s does not exist. It will be created." % (self.tuto.name, self.topic.name))
                self.tuto.create_tutorial(ctx)

    def check_topic_init_tuto(self):
        """Check that the topic and tutorial are already there and retrieve them"""
        # check topic
        if not self.topic.exists():
            raise Exception("The topic %s does not exists. It should be created" % self.topic.name)
        # initiate the tutorial
        self.tuto = Tutorial(training=self, topic=self.topic)
        self.tuto.init_from_existing_tutorial(self.kwds['tutorial_name'])

    def fill_data_library(self, ctx):
        """Fill a data library for a tutorial."""
        self.check_topic_init_tuto()
        # get the zenodo link
        z_link = ''
        if 'zenodo_link' in self.tuto.zenodo_link and self.tuto.zenodo_link != '':
            if self.kwds['zenodo_link']:
                info("The data library and the metadata will be updated with the new Zenodo link")
                z_link = self.kwds['zenodo_link']
                self.tuto.zenodo_link = z_link
            else:
                info("The data library will be extracted using the Zenodo link in the metadata of the tutorial")
                z_link = self.tuto.zenodo_link
        elif self.kwds['zenodo_link']:
            info("The data library will be created and the metadata will be filled with the new Zenodo link")
            z_link = self.kwds['zenodo_link']
            self.tuto.zenodo_link = z_link

        if z_link == '' or z_link is None:
            raise Exception("A Zenodo link should be provided either in the metadata file or as argument of the command")

        # extract the data library from Zenodo
        self.tuto.prepare_data_library_from_zenodo()

        # update the metadata
        self.tuto.write_hands_on_tutorial()

    def generate_tuto_from_wf(self, ctx):
        """Generate the skeleton of a tutorial from a workflow."""
        self.check_topic_init_tuto()
        if self.tuto.has_workflow():
            info("Create tutorial skeleton from workflow")
            self.tuto.create_hands_on_tutorial(ctx)
            self.tuto.export_workflow_file()
        else:
            raise Exception(
                "A path to a local workflow or the id of a workflow on a running Galaxy instance should be provided"
            )


def init_training(kwds, ctx):
    """ """
    training = Training(kwds)
    training.init_training(ctx)


def fill_data_library(kwds, ctx):
    """ """
    print("test")
    training = Training(kwds)
    training.fill_data_library(ctx)


def generate_tuto_from_wf(kwds, ctx):
    """ """
    training = Training(kwds)
    training.generate_tuto_from_wf(ctx)


__all__ = (
    "init_training",
    "fill_data_library",
    "generate_tuto_from_wf",
)