# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.14.3 (tags/v3.14.3:323c59a, Feb  3 2026, 16:04:56) [MSC v.1944 64 bit (AMD64)]
# Embedded file name: ./src/scripts/client/gui/mods/mod_recent_stat_config.py
# Compiled at: 2022-04-13 18:13:56
from abc import ABCMeta
import traceback
from mod_recent_stat_logging import logError, logInfo

class Config:
    __metaclass__ = ABCMeta
    _defaultConfigPaths = ('no path', )

    def warnCantFindFiles(self):
        logInfo("Can't open configs %s" % self._defaultConfigPaths)
        return

    def warnNoAttribute(self, attributeName):
        logInfo('No attribute "%s" in config "%s"' % (attributeName, self._defaultConfigPaths))
        return

    def warnInvalidAttribute(self, attributeName, value, expectedValues):
        logInfo('In config "%s": attribute "%s" has an invalid value "%s". Possible values: %s.' % (self._defaultConfigPaths, attributeName, value, expectedValues))
        return


