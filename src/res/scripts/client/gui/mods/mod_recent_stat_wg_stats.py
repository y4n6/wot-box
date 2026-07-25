# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.14.3 (tags/v3.14.3:323c59a, Feb  3 2026, 16:04:56) [MSC v.1944 64 bit (AMD64)]
# Embedded file name: ./src/scripts/client/gui/mods/mod_recent_stat_wg_stats.py
# Compiled at: 2025-09-06 02:43:14
import json, traceback
from mod_recent_stat_config_main import ConfigMain
from mod_recent_stat_config_wg_id import ConfigWgId
from mod_recent_stat_container import PlayerData
from mod_recent_stat_converter import formatBattlesToKiloBattles, getXWN8, isPlayerFake
from mod_recent_stat_logging import logError
from mod_recent_stat_network import getJsonText

class WgStats:
    _ACCOUNT_INFO_URL = 'https://api.worldoftanks.{region}/wot/account/info/?application_id={appId}&fields=statistics.all.battles%2Cstatistics.all.wins%2Cstatistics.all.damage_dealt%2Cstatistics.all.frags%2Cstatistics.all.spotted%2Cstatistics.all.capture_points%2Cstatistics.all.dropped_capture_points&account_id={joinedIds}'
    _ACCOUNT_TANK_URL = 'https://api.worldoftanks.{region}/wot/account/tanks/?application_id={appId}&fields=statistics.battles%2Ctank_id&account_id={joinedIds}'
    _ACCOUNT_ACHIEVEMENTS_URL = 'https://api.worldoftanks.{region}/wot/account/achievements/?application_id={appId}&fields=achievements&account_id={joinedIds}'

    def __init__(self, configMain, configWgId):
        self._wn8Expected = None
        self._configMain = configMain
        self._configWgId = configWgId
        self.loadWn8Expected()
        return

    def loadWn8Expected(self):
        self._wn8Expected = dict()
        return

    def loadPlayerDataByVehicleList(self, vehicles, playerIdToData):
        idsToBeLoaded = set()
        for _vehicleID, vehicleData in vehicles.items():
            if 'accountDBID' in vehicleData:
                playerId = vehicleData['accountDBID']
                if playerId in playerIdToData or isPlayerFake(playerId):
                    continue
                idsToBeLoaded.add(playerId)

        for playerId in idsToBeLoaded:
            playerIdToData[playerId] = PlayerData()

        if len(idsToBeLoaded) == 0:
            return
        return

    @staticmethod
    def getWN8(winrate, avgDmg, avgFrags, avgSpot, avgDef, accountTanks, wn8Expected):
        if wn8Expected is None:
            return 0
        else:
            eFrags = 0
            eDmg = 0
            eSpot = 0
            eDef = 0
            eWinrate = 0
            eBattles = 0
            for accountTank in accountTanks:
                tankBattles = accountTank['statistics']['battles']
                tankId = accountTank['tank_id']
                if tankId in wn8Expected:
                    tankData = wn8Expected[tankId]
                    eFrags += tankBattles * tankData['expFrag']
                    eDmg += tankBattles * tankData['expDamage']
                    eSpot += tankBattles * tankData['expSpot']
                    eDef += tankBattles * tankData['expDef']
                    eWinrate += tankBattles * tankData['expWinRate']
                    eBattles += tankBattles

            if 0 in (eWinrate, eDmg, eFrags, eSpot, eDef):
                return 0
            rWin = max((winrate * eBattles / eWinrate - 0.71) / 0.29000000000000004, 0)
            rDmg = max((avgDmg * eBattles / eDmg - 0.22) / 0.78, 0)
            rFrag = max(min(rDmg + 0.2, (avgFrags * eBattles / eFrags - 0.12) / 0.88), 0)
            rSpot = max(min(rDmg + 0.1, (avgSpot * eBattles / eSpot - 0.38) / 0.62), 0)
            rDef = max(min(rDmg + 0.1, (avgDef * eBattles / eDef - 0.1) / 0.9), 0)
            return int(round(980 * rDmg + 210 * rDmg * rFrag + 155 * rFrag * rSpot + 75 * rDef * rFrag + 145 * min(1.8, rWin)))


