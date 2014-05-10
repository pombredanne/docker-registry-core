# -*- coding: utf-8 -*-
"""
docker_registry.core.drivers.dumb
~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a very dumb driver, which uses memory to store data.
It obviously won't work out of very simple tests.
Should only be used as inspiration

"""

from docker_registry.core import driver
from docker_registry.core.exceptions import FileNotFoundError


class Storage(driver.Base):

    _storage = {}

    def __init__(self, path=None):
        pass

    def exists(self, path):
        return path in self._storage

    def get_size(self, path):
        if path not in self._storage:
            raise FileNotFoundError('%s is not there' % path)
        return len(self._storage[path])

    def get_content(self, path):
        if path not in self._storage:
            raise FileNotFoundError('%s is not there' % path)
        return self._storage[path]

    def put_content(self, path, content):
        self._storage[path] = content

    def remove(self, path):
        if path not in self._storage:
            raise FileNotFoundError('%s is not there' % path)
        del self._storage[path]

    # def stream_read(self, path, bytes_range=None):

    # def stream_write(self, path, fp):
    #     """
    #     Method to stream write
    #     """
    #     raise NotImplementedError(
    #         "You must implement stream_write(self, path, fp) " +
    #         "on your storage %s" %
    #         self.__class__.__name__)

    # def list_directory(self, path=None):
    #     """
    #     Method to list directory
    #     """
    #     raise NotImplementedError(
    #         "You must implement list_directory(self, path=None) " +
    #         "on your storage %s" %
    #         self.__class__.__name__)
