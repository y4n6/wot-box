# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.14.3 (tags/v3.14.3:323c59a, Feb  3 2026, 16:04:56) [MSC v.1944 64 bit (AMD64)]
# Embedded file name: ./src/scripts/client/gui/mods/mod_recent_stat_constant.py
# Compiled at: 2022-04-13 18:13:56
PLAYER_ID_NOT_KNOWN = -1
COLUMN_ID_NOT_FOUND = -1
MAX_ITERATIONS = 1000

class STAT_PROVIDER(object):
    NOOBMETER = 'noobmeter'
    KTTC = 'kttc'
    SUPPORTED = frozenset((NOOBMETER, KTTC))


class STAT_FIELDS(object):
    WN8 = 'wn8'
    XWN8 = 'xwn8'
    BATTLES = 'battles'
    KILO_BATTLES = 'kb'


class CONFIG_MAIN(object):
    REGION = 'region'
    TIMEOUT = 'timeout'
    RECENT_STAT_PROVIDERS = 'recentStatProviders'
    BADGE_TYPE = 'badgeType'


class CONFIG_FORMAT(object):
    PLAYER_NAME = 'playerName'
    NO_INFO = 'noInfo'


class BADGE_TYPE(object):
    XWN8_COLOR = 'xwn8Color'
    BOB2020_TEAM_COLOR = 'bob2020TeamColor'


