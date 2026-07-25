# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.14.3 (tags/v3.14.3:323c59a, Feb  3 2026, 16:04:56) [MSC v.1944 64 bit (AMD64)]
# Embedded file name: ./src/scripts/client/gui/mods/mod_recent_stat_config_wg_id.py
# Compiled at: 2022-04-13 18:13:56
from mod_recent_stat_config import Config

class ConfigWgId(Config):
    _defaultConfigPaths = ('mods/configs/io.github.servb.recent_stat/wg_api_application_id.txt',
                           '../mods/configs/io.github.servb.recent_stat/wg_api_application_id.txt')

    def __init__(self, configPaths=_defaultConfigPaths):
        self._configPaths = configPaths
        self.wgId = self._defaultWgId()
        self.load()
        return

    @staticmethod
    def _defaultWgId():
        return '6bcfe604e2408e210eb25510a1f6eeaa'

    def load(self):
        anyLoaded = True
        for configPath in self._configPaths:
            try:
                with open(configPath, 'r') as configFile:
                    self.wgId = configFile.readline().strip()
            except IOError:
                pass

        if not anyLoaded:
            self.warnCantFindFiles()
        return


