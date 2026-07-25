# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.14.3 (tags/v3.14.3:323c59a, Feb  3 2026, 16:04:56) [MSC v.1944 64 bit (AMD64)]
# Embedded file name: ./src/scripts/client/gui/mods/mod_recent_stat_config_main.py
# Compiled at: 2022-04-13 18:13:56
import json
from mod_recent_stat_config import Config
from mod_recent_stat_constant import BADGE_TYPE, CONFIG_MAIN, STAT_PROVIDER
from mod_recent_stat_provider_kttc import Kttc
from mod_recent_stat_provider_noobmeter import Noobmeter
from mod_recent_stat_string import removeComments

class ConfigMain(Config):
    _defaultConfigPaths = ('mods/configs/io.github.servb.recent_stat/config_main.json',
                           '../mods/configs/io.github.servb.recent_stat/config_main.json')
    _defaultRegion = 'ru'
    _defaultTimeout = 7
    _defaultRecentStatProviderNames = (STAT_PROVIDER.KTTC,)
    _defaultBadgeType = BADGE_TYPE.XWN8_COLOR

    def __init__(self, configPaths=_defaultConfigPaths):
        self._configPaths = configPaths
        self.region = self._defaultRegion
        self.timeout = self._defaultTimeout
        self._recentStatProviderNames = self._defaultRecentStatProviderNames
        self.badgeType = self._defaultBadgeType
        self._load()
        self.recentStatProviders = self.createProviders(self._recentStatProviderNames)
        return

    def _load(self):
        anyLoaded = True
        for configPath in self._configPaths:
            try:
                with open(configPath, 'r') as configFile:
                    configJson = json.loads(removeComments(configFile.read()))
                    if CONFIG_MAIN.REGION in configJson:
                        self.region = configJson[CONFIG_MAIN.REGION]
                    else:
                        self.warnNoAttribute(CONFIG_MAIN.REGION)
                    if CONFIG_MAIN.TIMEOUT in configJson:
                        self.timeout = configJson[CONFIG_MAIN.TIMEOUT]
                    else:
                        self.warnNoAttribute(CONFIG_MAIN.TIMEOUT)
                    if CONFIG_MAIN.RECENT_STAT_PROVIDERS in configJson:
                        statProviders = configJson[CONFIG_MAIN.RECENT_STAT_PROVIDERS]
                        if isinstance(statProviders, list):
                            validProviders = []
                            for statProvider in statProviders:
                                if statProvider not in STAT_PROVIDER.SUPPORTED:
                                    self.warnInvalidAttribute(CONFIG_MAIN.RECENT_STAT_PROVIDERS, statProvider, STAT_PROVIDER.SUPPORTED)
                                else:
                                    validProviders.append(statProvider)

                            self._recentStatProviderNames = validProviders
                    else:
                        self.warnNoAttribute(CONFIG_MAIN.RECENT_STAT_PROVIDERS)
                    if CONFIG_MAIN.BADGE_TYPE in configJson:
                        self.badgeType = configJson[CONFIG_MAIN.BADGE_TYPE]
                    else:
                        self.warnNoAttribute(CONFIG_MAIN.BADGE_TYPE)
            except IOError:
                pass

        if not anyLoaded:
            self.warnCantFindFiles()
        return

    @staticmethod
    def createProviders(providerNames):
        return tuple(map((lambda providerName: Noobmeter() if providerName == STAT_PROVIDER.NOOBMETER else Kttc()), providerNames))

    def __str__(self):
        return "{region='%s', timeout=%s, providerNames=%s, badgeType='%s'}" % (self.region, self.timeout, list(map((lambda provider: provider.name), self.recentStatProviders)), self.badgeType)


