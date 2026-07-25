# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.14.3 (tags/v3.14.3:323c59a, Feb  3 2026, 16:04:56) [MSC v.1944 64 bit (AMD64)]
# Embedded file name: ./src/scripts/client/gui/mods/mod_recent_stat_network.py
# Compiled at: 2022-09-01 00:01:49
import random, sys
if 'urllib.request' in sys.modules:
    from urllib.request import urlopen, Request
else:
    from urllib2 import urlopen, Request
from mod_recent_stat_string import removeTags
_DEFAULT_TIMEOUT = 10

def generateUserAgent():
    firefox = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{0}.0) Gecko/20100101 Firefox/{0}.0'
    firefoxVersion = random.randint(61, 62)
    userAgent = firefox.format(firefoxVersion)
    return userAgent


def generateHeaders():
    headers = {'User-Agent': (generateUserAgent())}
    return headers


def getRawSiteText(url, timeout=_DEFAULT_TIMEOUT):
    req = Request(url, headers=generateHeaders())
    html = urlopen(req, timeout=timeout).read().decode('utf-8')
    return html


def getFormattedHtmlText(url, timeout=_DEFAULT_TIMEOUT):
    return getRawSiteText(url, timeout).replace('&nbsp;', ' ').replace('"', "'")


def getJsonText(url, timeout=_DEFAULT_TIMEOUT):
    return getRawSiteText(url, timeout).replace("'", '"')


def getNextRowCells(string, idx, td='td'):
    cellBegin = '<%s' % td
    cellEnd = '</%s>' % td
    answer = list()
    rowEndIdx = string.find('</tr>', idx)
    nowTdIdx = string.find(cellBegin, idx, rowEndIdx)
    while nowTdIdx != -1:
        nowTdBeginIdx = string.find('>', nowTdIdx) + 1
        nowTdEndIdx = string.find(cellEnd, nowTdIdx)
        colspan = 1
        colspanBeginIdx = string.find('colspan', nowTdIdx, nowTdBeginIdx)
        if colspanBeginIdx != -1:
            colspanValueBeginIdx = string.find("'", colspanBeginIdx, nowTdBeginIdx) + 1
            assert colspanValueBeginIdx != -1, 'No colspan begin found in %s' % string[nowTdIdx:nowTdBeginIdx]
            colspanValueEndIdx = string.find("'", colspanValueBeginIdx, nowTdBeginIdx)
            assert colspanValueEndIdx != -1, 'No colspan end found in %s' % string[nowTdIdx:nowTdBeginIdx]
            colspan = int(string[colspanValueBeginIdx:colspanValueEndIdx])
        for _ in range(colspan):
            answer.append(string[nowTdBeginIdx:nowTdEndIdx])

        nowTdIdx = string.find(cellBegin, nowTdEndIdx)

    return answer


def getNumberFromCell(tdText):
    split = removeTags(tdText).replace(',', ' ').split()
    data = None
    for i in range(len(split) - 1):
        if split[i].isdigit() and split[i + 1].isdigit():
            data = split[i] + split[i + 1]
            return data

    for i in range(len(split)):
        if split[i].isdigit():
            data = split[i]

    return data


