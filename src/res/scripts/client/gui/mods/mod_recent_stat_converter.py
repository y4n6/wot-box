# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.14.3 (tags/v3.14.3:323c59a, Feb  3 2026, 16:04:56) [MSC v.1944 64 bit (AMD64)]
# Embedded file name: ./src/scripts/client/gui/mods/mod_recent_stat_converter.py
# Compiled at: 2022-04-13 18:13:56


def formatBattlesToKiloBattles(battles):
    return int(round(int(battles) / 1000.0))


def getXWN8(wn8):
    return int(round(max(0.0, min(99.0, wn8 * (wn8 * (wn8 * (wn8 * (wn8 * (-wn8 * 9.762e-20 + 1.6221e-15) - 1.007e-11) + 2.7916e-08) - 3.6982e-05) + 0.05577) - 1.3))))


def isPlayerFake(accountDBID):
    return accountDBID == 0


