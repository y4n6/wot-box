# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.14.3 (tags/v3.14.3:323c59a, Feb  3 2026, 16:04:56) [MSC v.1944 64 bit (AMD64)]
# Embedded file name: ./src/scripts/client/gui/mods/mod_recent_stat_logging.py
# Compiled at: 2025-10-20 11:12:33


def logInfo(message):
    print '[--- box-ce-mod ---]'
    print message
    print '[--- box-ce-mod ---]'
    return


def logError(message, exceptionText):
    print '[!--- box-ce-mod ---]'
    print message
    print '[!--- Exception text:]'
    print exceptionText
    print '[!--- box-ce-mod ---]'
    return


