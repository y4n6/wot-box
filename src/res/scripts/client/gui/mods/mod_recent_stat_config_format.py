# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.14.3 (tags/v3.14.3:323c59a, Feb  3 2026, 16:04:56) [MSC v.1944 64 bit (AMD64)]
# Embedded file name: ./src/scripts/client/gui/mods/mod_recent_stat_config_format.py
# Compiled at: 2022-04-15 04:21:04
import json
from mod_recent_stat_config import Config
from mod_recent_stat_constant import CONFIG_FORMAT
from mod_recent_stat_string import removeComments

class ConfigFormat(Config):
    _defaultConfigPaths = ('mods/configs/io.github.servb.recent_stat/config_format.json',
                           '../mods/configs/io.github.servb.recent_stat/config_format.json')
    _defaultPlayerName = '{xwn8} {wn8}% '
    _defaultNoInfo = '--'

    def __init__(self, configPaths=_defaultConfigPaths):
        self._configPaths = configPaths
        self.playerName = self._defaultPlayerName
        self.noInfo = self._defaultNoInfo
        self._load()
        return

    def _load(self):
        anyLoaded = True
        for configPath in self._configPaths:
            try:
                with open(configPath, 'r') as configFile:
                    configJson = json.loads(removeComments(configFile.read()))
                    if CONFIG_FORMAT.PLAYER_NAME in configJson:
                        self.playerName = configJson[CONFIG_FORMAT.PLAYER_NAME]
                    else:
                        self.warnNoAttribute(CONFIG_FORMAT.PLAYER_NAME)
                    if CONFIG_FORMAT.NO_INFO in configJson:
                        self.noInfo = configJson[CONFIG_FORMAT.NO_INFO]
                    else:
                        self.warnNoAttribute(CONFIG_FORMAT.NO_INFO)
            except IOError:
                pass

        if not anyLoaded:
            self.warnCantFindFiles()
        return

    def __str__(self):
        return "{playerName='%s', noInfo='%s'}" % (self.playerName, self.noInfo)


