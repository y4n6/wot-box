# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.14.3 (tags/v3.14.3:323c59a, Feb  3 2026, 16:04:56) [MSC v.1944 64 bit (AMD64)]
# Embedded file name: ./src/scripts/client/gui/mods/mod_recent_stat_provider_kttc.py
# Compiled at: 2022-09-01 00:06:56
import json, traceback, re, sys
if 'urllib.request' in sys.modules:
    from urllib.request import quote
else:
    from urllib2 import quote
from mod_recent_stat_constant import PLAYER_ID_NOT_KNOWN, STAT_FIELDS
from mod_recent_stat_logging import logInfo, logError
from mod_recent_stat_network import getRawSiteText, getFormattedHtmlText, getJsonText
from mod_recent_stat_provider import StatProvider

class Kttc(StatProvider):
    name = 'Kttc'

    def _getStatistics(self, region, nickname, playerId, playerIdToData):
        playerData = playerIdToData[playerId]
        qname = quote(nickname)
        full_url = ('http://wotbox.ouj.com/wotbox/index.php?r=default/index&pn={}').format(qname)
        recentStatJson = getFormattedHtmlText(full_url)
        findCE = re.search("<span class='num'>(\\d+)</span>", recentStatJson)
        findWR = re.search("win-rate='(\\d+)'", recentStatJson)
        if findCE:
            playerData.xwn8 = int(findCE.group(1))
        if findWR:
            playerData.wn8 = int(findWR.group(1))
            playerData.hasRecentStat = True
        return


