# -*- coding: utf-8 -*-

# from unittest import TestCase
# import cStringIO as StringIO
import random
import string

from nose.tools import raises
from docker_registry.core import driver
from docker_registry.core.compat import is_py2
from docker_registry.core.exceptions import FileNotFoundError


class Driver(object):

    def __init__(self, scheme, path=None):
        self.scheme = scheme
        self.path = path

    # Load the requested driver
    def setUp(self):
        storage = driver.fetch(self.scheme)
        self._storage = storage(self.path)

    def tearDown(self):
        pass

    def gen_random_string(self, length=16):
        return ''.join([random.choice(string.ascii_uppercase + string.digits)
                        for x in range(length)]).lower()

    def test_exists_non_existent_path(self):
        filename = self.gen_random_string()
        assert not self._storage.exists(filename)

    def test_exists_existent_path(self):
        filename = self.gen_random_string()
        content = self.gen_random_string()
        self._storage.put_content(filename, content)
        assert self._storage.exists(filename)

    def test_write_read(self):
        filename = self.gen_random_string()
        content = self.gen_random_string()
        self._storage.put_content(filename, content)

        ret = self._storage.get_content(filename)
        assert ret == content

    def test_size(self):
        filename = self.gen_random_string()
        content = self.gen_random_string()
        self._storage.put_content(filename, content)

        ret = self._storage.get_size(filename)
        assert ret == len(content)

    def test_write_read_unicode(self):
        filename = self.gen_random_string()

        content = u"∫".encode('utf8')
        self._storage.put_content(filename, content)

        ret = self._storage.get_content(filename)
        assert ret == content
        ret = self._storage.get_size(filename)
        assert ret == len(content)

    def test_write_read_unicode_str(self):
        filename = self.gen_random_string()

        content = "∫"
        if is_py2:
            content = content.decode('utf8')
        content = content.encode('utf8')
        self._storage.put_content(filename, content)

        ret = self._storage.get_content(filename)
        assert ret == content
        ret = self._storage.get_size(filename)
        assert ret == len(content)

        content = "∫"
        self._storage.put_content(filename, content)

        ret = self._storage.get_content(filename)
        assert ret == content
        ret = self._storage.get_size(filename)
        assert ret == len(content)

    def test_write_read_bytes(self):
        filename = self.gen_random_string()

        content = b"a"
        self._storage.put_content(filename, content)

        ret = self._storage.get_content(filename)
        assert ret == content
        ret = self._storage.get_size(filename)
        assert ret == len(content)

    def test_write_read_twice(self):
        filename = self.gen_random_string()
        content = self.gen_random_string()
        self._storage.put_content(filename, content)
        ret = self._storage.get_content(filename)
        l = self._storage.get_size(filename)

        content2 = self.gen_random_string()
        self._storage.put_content(filename, content2)
        ret2 = self._storage.get_content(filename)
        l2 = self._storage.get_size(filename)

        assert ret == content
        assert l == len(content)
        assert ret2 == content2
        assert l2 == len(content2)

    def test_remove_existent(self):
        filename = self.gen_random_string()
        content = self.gen_random_string()
        self._storage.put_content(filename, content)
        self._storage.remove(filename)
        assert not self._storage.exists(filename)

    @raises(FileNotFoundError)
    def test_read_inexistent(self):
        filename = self.gen_random_string()
        self._storage.get_content(filename)

    @raises(FileNotFoundError)
    def test_remove_inexistent(self):
        filename = self.gen_random_string()
        self._storage.remove(filename)

    @raises(FileNotFoundError)
    def test_get_size_inexistent(self):
        filename = self.gen_random_string()
        self._storage.get_size(filename)

    # def test_stream(self):
    #     filename = self.gen_random_string()
    #     # test 7MB
    #     content = self.gen_random_string(7 * 1024 * 1024)

    #     assert not self._storage.exists(filename)

    #     # test exists
    #     io = StringIO.StringIO(content)
    #     self._storage.stream_write(filename, io)
    #     io.close()
    #     assert self._storage.exists(filename)

    #     # test read / write
    #     data = ''
    #     for buf in self._storage.stream_read(filename):
    #         data += buf

    #     assert content == data

    #     # test bytes_range only if the storage backend suppports it
    #     if self._storage.supports_bytes_range:
    #         b = random.randint(0, len(content) / 2)
    #         bytes_range = (b, random.randint(b + 1, len(content) - 1))
    #         data = ''
    #         for buf in self._storage.stream_read(filename, bytes_range):
    #             data += buf
    #         expected_content = content[bytes_range[0]:bytes_range[1] + 1]
    #         assert data == expected_content

    #     # test remove
    #     self._storage.remove(filename)
    #     assert not self._storage.exists(filename)

    # @raises(OSError)
    # def test_inexistent_list_directory(self):
    #     notexist = self.gen_random_string()
    #     iterator = self._storage.list_directory(notexist)
    #     next(iterator)
