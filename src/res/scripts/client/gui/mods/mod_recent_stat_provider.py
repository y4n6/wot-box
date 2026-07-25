# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.14.3 (tags/v3.14.3:323c59a, Feb  3 2026, 16:04:56) [MSC v.1944 64 bit (AMD64)]
# Embedded file name: ./src/scripts/client/gui/mods/mod_recent_stat_provider.py
# Compiled at: 2022-04-13 18:13:56
from abc import ABCMeta, abstractmethod
import traceback
from mod_recent_stat_logging import logError

class StatProvider:
    __metaclass__ = ABCMeta
    name = 'Abstract Stat Provider'

    def getStatistics(self, region, nickname, playerId, playerIdToData):
        try:
            self._getStatistics(region, nickname, playerId, playerIdToData)
        except BaseException:
            logError('Error in getStatistics(%s, %s, %s)' % (region, nickname, playerId), traceback.format_exc())

        return

    @abstractmethod
    def _getStatistics(self, region, nickname, playerId, playerIdToData):
        return


