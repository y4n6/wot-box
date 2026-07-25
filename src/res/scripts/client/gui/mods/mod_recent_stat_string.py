# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.14.3 (tags/v3.14.3:323c59a, Feb  3 2026, 16:04:56) [MSC v.1944 64 bit (AMD64)]
# Embedded file name: ./src/scripts/client/gui/mods/mod_recent_stat_string.py
# Compiled at: 2022-04-13 18:13:56


def removeSubstringsByBeginAndEnd(string, begin, end):
    answer = ''
    nextStart = 0
    while nextStart < len(string):
        beginIdx = string.find(begin, nextStart)
        if beginIdx == -1:
            answer += string[nextStart:]
            return answer
        answer += string[nextStart:beginIdx]
        endIdx = string.find(end, beginIdx + 1)
        if endIdx == -1:
            return answer
        nextStart = endIdx + len(end)

    return answer


def removeTags(htmlText):
    return removeSubstringsByBeginAndEnd(htmlText, '<', '>')


def removeComments(jsonText):
    return removeSubstringsByBeginAndEnd(jsonText, '/*', '*/')


