#!/usr/bin/env python

# -*-coding:utf8-*-


import ConfigParser


class SimulatorException(Exception):
    pass


class Simulator(objects):

    def __init__(self, configfile=''):
        self.configfile = configfile
        self.readConfig()
        self.checkConfig()
        self.populateTests()

    def readConfig(self):
        self.config = ConfigParser.SafeConfigParser()
        if not self.config.read(configfile):
            raise SimulatorException()

    def checkConfig(self):
        pass

    def populateTests(self):
        pass

