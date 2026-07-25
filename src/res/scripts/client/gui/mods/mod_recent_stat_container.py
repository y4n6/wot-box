# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.14.3 (tags/v3.14.3:323c59a, Feb  3 2026, 16:04:56) [MSC v.1944 64 bit (AMD64)]
# Embedded file name: ./src/scripts/client/gui/mods/mod_recent_stat_container.py
# Compiled at: 2022-04-13 18:13:56
from mod_recent_stat_config_format import ConfigFormat
from mod_recent_stat_constant import STAT_FIELDS

class PlayerData(object):
    battles = None
    kb = None
    wn8 = None
    xwn8 = None
    achievements = dict()
    hasRecentStat = False

    def createDict(self, configFormat):
        return {(STAT_FIELDS.KILO_BATTLES): (self.orNoInfo(self.kb, configFormat)), 
           (STAT_FIELDS.BATTLES): (self.orNoInfo(self.battles, configFormat)), 
           (STAT_FIELDS.WN8): (self.orNoInfo(self.wn8, configFormat)), 
           (STAT_FIELDS.XWN8): (self.orNoInfo(self.xwn8, configFormat))}

    @staticmethod
    def orNoInfo(value, configFormat):
        if value is None:
            return configFormat.noInfo
        else:
            return value


