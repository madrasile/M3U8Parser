# -*- coding: utf-8 -*-

"""Those are all functions needed for the Parser"""

def unQuote(text):
    return text.replace('\"', '')

def quote(text):
    return "\"%s\"" % text

def checkValue(value, exception):
    if value != None:
        return value
    else:
        raise exception

def checkList(list, exception):
    if len(list) > 0:
        return list
    else:
        raise exception