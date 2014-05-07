# -*- coding: utf-8 -*-

from droid.tests import Driver
from droid.tests import Query
import droid.drivers.dumb as driverspace


class TestQuery(Query):
    def __init__(self):
        self.scheme = 'dumb'
        self.cls = driverspace


class TestDriver(Driver):
    def __init__(self):
        self.scheme = 'dumb'
