# -*- coding: utf-8 -*-

from nose.tools import raises

from docker_registry.core import driver
from docker_registry.core.exceptions import NotImplementedError
import docker_registry.drivers.dumb as driverspace


class Query(object):

    def __init__(self, scheme):
        self.scheme = scheme
        self.cls = driverspace

    def testDriverIsAvailable(self):
        drvs = driver.available()
        assert self.scheme in drvs

    def testFetchingDriver(self):
        dumb = driver.fetch(self.scheme)
        assert self.cls.Storage == dumb
        assert driver.Base in dumb.__bases__

    @raises(NotImplementedError)
    def testFetchingNonExistentDriver(self):
        driver.fetch("nonexistentstupidlynameddriver")
