# -*- coding: utf-8 -*-
"""
docker_registry.core.driver
~~~~~~~~~~~~~~~~~~~~~~~~~~

This file defines:
 * a generic interface that describes a uniform "driver"
 * methods to register / get these "connections"

Pretty much, the purpose of this is just to abstract the underlying storage
implementation, for a given scheme.

"""

__all__ = ["fetch", "available", "Base"]

import logging
import pkgutil
import docker_registry.drivers

from .exceptions import NotImplementedError

logger = logging.getLogger(__name__)


class Base(object):

    """
    Storage is a convenience class that describes methods that must be
    implemented by any backend.
    You should inherit (or duck type) this if you are implementing your own.

    :param host: host name
    :type host: unicode
    :param port: port number
    :type port: int
    :param basepath: base path (will be prepended to actual requests)
    :type basepath: unicode
    """

    # Useful if we want to change those locations later without rewriting
    # the code which uses Storage
    REPOSITORIES = 'repositories'
    IMAGES = 'images'

    def __init__(self, path=None, config=None):
        pass

    # Set the IO buffer to 128kB
    buffer_size = 128 * 1024
    # By default no storage plugin supports it
    supports_bytes_range = False

    # FIXME(samalba): Move all path resolver in each module (out of the base)
    def images_list_path(self, namespace, repository):
        repository_path = self.repository_path(
            namespace=namespace, repository=repository)
        return '{0}/_images_list'.format(repository_path)

    def image_json_path(self, image_id):
        return '{0}/{1}/json'.format(self.IMAGES, image_id)

    def image_mark_path(self, image_id):
        return '{0}/{1}/_inprogress'.format(self.IMAGES, image_id)

    def image_checksum_path(self, image_id):
        return '{0}/{1}/_checksum'.format(self.IMAGES, image_id)

    def image_layer_path(self, image_id):
        return '{0}/{1}/layer'.format(self.IMAGES, image_id)

    def image_ancestry_path(self, image_id):
        return '{0}/{1}/ancestry'.format(self.IMAGES, image_id)

    def image_files_path(self, image_id):
        return '{0}/{1}/_files'.format(self.IMAGES, image_id)

    def image_diff_path(self, image_id):
        return '{0}/{1}/_diff'.format(self.IMAGES, image_id)

    def repository_path(self, namespace, repository):
        return '{0}/{1}/{2}'.format(
            self.REPOSITORIES, namespace, repository)

    def tag_path(self, namespace, repository, tagname=None):
        repository_path = self.repository_path(
            namespace=namespace, repository=repository)
        if not tagname:
            return repository_path
        return '{0}/tag_{1}'.format(repository_path, tagname)

    def repository_json_path(self, namespace, repository):
        repository_path = self.repository_path(
            namespace=namespace, repository=repository)
        return '{0}/json'.format(repository_path)

    def repository_tag_json_path(self, namespace, repository, tag):
        repository_path = self.repository_path(
            namespace=namespace, repository=repository)
        return '{0}/tag{1}_json'.format(repository_path, tag)

    def index_images_path(self, namespace, repository):
        repository_path = self.repository_path(
            namespace=namespace, repository=repository)
        return '{0}/_index_images'.format(repository_path)

    def private_flag_path(self, namespace, repository):
        repository_path = self.repository_path(
            namespace=namespace, repository=repository)
        return '{0}/_private'.format(repository_path)

    def is_private(self, namespace, repository):
        return self.exists(self.private_flag_path(namespace, repository))

    def content_redirect_url(self, path):
        """Get a URL for content at path

        Get a URL to which client can be redirected to get the content from
        the path. Return None if not supported by this engine.

        Note, this feature will only be used if the `storage_redirect`
        configuration key is set to `True`.
        """
        return None

    def get_content(self, path):
        """
        Method to get content
        """
        raise NotImplementedError(
            "You must implement get_content(self, path) on your storage %s" %
            self.__class__.__name__)

    def put_content(self, path, content):
        """
        Method to put content
        """
        raise NotImplementedError(
            "You must implement put_content(self, path, content) on %s" %
            self.__class__.__name__)

    def stream_read(self, path, bytes_range=None):
        """
        Method to stream read
        """
        raise NotImplementedError(
            "You must implement stream_read(self, path, , bytes_range=None) " +
            "on your storage %s" %
            self.__class__.__name__)

    def stream_write(self, path, fp):
        """
        Method to stream write
        """
        raise NotImplementedError(
            "You must implement stream_write(self, path, fp) " +
            "on your storage %s" %
            self.__class__.__name__)

    def list_directory(self, path=None):
        """
        Method to list directory
        """
        raise NotImplementedError(
            "You must implement list_directory(self, path=None) " +
            "on your storage %s" %
            self.__class__.__name__)

    def exists(self, path):
        """
        Method to test exists
        """
        raise NotImplementedError(
            "You must implement exists(self, path) on your storage %s" %
            self.__class__.__name__)

    def remove(self, path):
        """
        Method to remove
        """
        raise NotImplementedError(
            "You must implement remove(self, path) on your storage %s" %
            self.__class__.__name__)

    def get_size(self, path):
        """
        Method to get the size
        """
        raise NotImplementedError(
            "You must implement get_size(self, path) on your storage %s" %
            self.__class__.__name__)


def fetch(name):
    """
    The only public method you should access if you are not implementing
    your own driver. - use this to get a backend
    instance to which you can delegate actual requests.

    :param host: host name
    :type host: unicode
    :param port: port number
    :type port: int
    :param basepath: base path (will be prepended to actual requests)
    :type basepath: unicode
    :returns: a docker connection instance usable for the requested scheme
    :rtype: DockerConnection
    """
    try:
        # module = __import__("docker_registry.drivers.%s" % name)
        module = __import__('docker_registry.drivers.%s' % name, globals(),
                            locals(), ['Storage'], 0)
        logger.debug("Will return docker_registry.drivers.%s.Storage" % name)
    except Exception:
        raise NotImplementedError(
            """You requested storage driver docker_registry.drivers.%s
which is not installed. Try `pip install docker_registry-drivers-%s`
or check your configuration. The following are currently
available on your system: %s"""
            % (name, name, available())
        )
    return module.Storage


def available():
    return [modname for importer, modname, ispkg
            in pkgutil.iter_modules(docker_registry.drivers.__path__)]
