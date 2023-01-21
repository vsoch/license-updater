__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022-2023, Vanessa Sochat"
__license__ = "MPL 2.0"


import abc
import importlib
import inspect
import os
import re
from collections.abc import Mapping

from license_updater.logger import logger

here = os.path.abspath(os.path.dirname(__file__))


class UpdaterFinder(Mapping):
    """
    Create a cache of available updaters.
    """

    _updaters = {}

    def __init__(self):
        """
        Instantiate an updater
        """
        self.collection_path = os.path.join(here, "updaters")
        self.load()

    def __getitem__(self, name):
        return self._updaters.get(name)

    def __iter__(self):
        return iter(self._updaters)

    def __len__(self):
        return len(self._updaters)

    def load(self):
        """
        Load new updaters
        """
        self._updaters = self._load_updaters()

    def _load_updaters(self):
        """
        Load updaters based on listing folders in the collection.
        """
        lookup = {}
        for name in os.listdir(self.collection_path):
            updater_dir = os.path.join(self.collection_path, name)
            updater_file = os.path.join(updater_dir, "update.py")

            # Skip files in collection folder
            if os.path.isfile(updater_dir):
                continue

            # Continue if the file doesn't exist
            if not os.path.exists(updater_file):
                logger.debug("%s does not appear to have an update.py, skipping." % updater_dir)
                continue

            # The class name means we split by underscore, capitalize, and join
            class_name = "".join([x.capitalize() for x in name.split("_")]) + "Updater"
            module = "license_updater.main.updaters.%s.update" % name

            # Not instantiated - will be instantiated for a specific action
            lookup[name] = getattr(importlib.import_module(module), class_name)
        return lookup


class UpdaterBase:

    name = "updater"
    description = "An abstract base updater."
    date_time_format = "%Y-%m-%dT%H:%M:%S%z"
    file_regex = None

    def __init__(self):
        self._data = {}
        self.headers = {}
        self.count = 0

    def matches(self, path):
        """
        Determine if an updater matches a file.
        """
        if not self.file_regex:
            return True
        return re.search(self.file_regex, path) is not None

    @abc.abstractmethod
    def detect(self, *args, **kwargs):
        pass

    @property
    def slug(self):
        return re.sub("(-|_)", "", self.name)

    @property
    def title(self):
        return self.name.capitalize()

    @property
    def settings(self):
        """
        Get settings specific to updater
        """
        return self.global_settings.updaters.get(self.name, {})

    @property
    def classpath(self):
        return os.path.dirname(inspect.getfile(self.__class__))
