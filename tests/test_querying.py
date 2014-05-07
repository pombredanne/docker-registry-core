# -*- coding: utf-8 -*-

# import logging

from nose.tools import raises

from droid.core import driver
from droid.core.exceptions import NotImplementedError
from droid.drivers.dumb import Storage as dumbclass


def testDumbDriverIsAvailable():
    drvs = driver.available()
    assert "dumb" in drvs


def testFetchingDumbDriver():
    dumb = driver.fetch("dumb")
    assert dumbclass == dumb
    assert driver.Base in dumb.__bases__


@raises(NotImplementedError)
def testFetchingNonExistentDriver():
    driver.fetch("nonexistentstupidlynameddriver")
