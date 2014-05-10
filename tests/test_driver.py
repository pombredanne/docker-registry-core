# -*- coding: utf-8 -*-

from docker_registry.testing import Driver
from docker_registry.testing import Query
import docker_registry.drivers.dumb as driverspace


class TestQuery(Query):
    def __init__(self):
        self.scheme = 'dumb'
        self.cls = driverspace


class TestDriver(Driver):
    def __init__(self):
        self.scheme = 'dumb'
        self.path = ''
