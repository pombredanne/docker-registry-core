# -*- coding: utf-8 -*-
"""
docker_registry.core.drivers.dumb
~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a very dumb driver, which uses memory to store data.
It obviously won't work out of very simple tests.
Should only be used as inspiration

"""

from docker_registry.core import driver
from docker_registry.core.compat import StringIO
from docker_registry.core.exceptions import FileNotFoundError


class Storage(driver.Base):

    _storage = {}

    def __init__(self, path=None, config=None):
        self.supports_bytes_range = True

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

    def stream_read(self, path, bytes_range=None):
        if path not in self._storage:
            raise FileNotFoundError('%s is not there' % path)

        f = self._storage[path]
        nb_bytes = 0
        total_size = 0
        if bytes_range:
            f.seek(bytes_range[0])
            total_size = bytes_range[1] - bytes_range[0] + 1
        else:
            f.seek(0)
        while True:
            buf = None
            if bytes_range:
                # Bytes Range is enabled
                buf_size = self.buffer_size
                if nb_bytes + buf_size > total_size:
                    # We make sure we don't read out of the range
                    buf_size = total_size - nb_bytes
                if buf_size > 0:
                    buf = f.read(buf_size)
                    nb_bytes += len(buf)
                else:
                    # We're at the end of the range
                    buf = ''
            else:
                buf = f.read(self.buffer_size)
            if not buf:
                break
            yield buf

    def stream_write(self, path, fp):
        # Size is mandatory
        if path not in self._storage:
            self._storage[path] = StringIO()

        f = self._storage[path]
        try:
            while True:
                buf = fp.read(self.buffer_size)
                if not buf:
                    break
                f.write(buf)
        except IOError:
            pass

    def list_directory(self, path=None):
        if path not in self._storage:
            raise FileNotFoundError('%s is not there' % path)

        ls = []
        for k in self._storage.keys():
            if (not k == path) and k.startswith(path):
                ls.append(k)

        if not len(ls):
            raise FileNotFoundError('%s is not there' % path)

        return ls
