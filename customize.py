# uncompyle6 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.7.3 (v3.7.3:ef4ec6ed12, Mar 25 2019, 16:52:21) 
# [Clang 6.0 (clang-600.0.57)]
# Embedded file name: /Users/zanebaylon/Desktop/Art_Dash/customize.py
# Compiled at: 2022-08-09 08:31:45
# Size of source mod 2**32: 1727 bytes
import yaml

def parse_flair(red_title):
    strValue = red_title
    ch1 = '['
    ch2 = ']'
    listOfWords = strValue.split(ch1, 1)
    strValue = listOfWords[1]
    listOfWords = strValue.split(ch2, 1)
    strValue = listOfWords[0]
    tag = strValue.lower()
    flair_key = ""
    trs = "translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')"
    if 'm' in tag:
        if '/' in tag:
            if 'f' in tag:
                flair_key = 'contains(' + trs + ", 'straight') or contains(" + trs + ", 'yiff')"
            if 'm/m' in tag:
                flair_key = 'contains(' + trs + ", 'gay') or contains(" + trs + ", 'yiff') or " + trs + " = 'male'"
            else:
                log.error("Unexpexted '/' in tag")
        else:
            flair_key = 'contains(' + trs + ", 'gay') or contains(" + trs + ", 'solo') or " + trs + " = 'male'"
    elif 'f' in tag:
        if '/' in tag:
            if 'f/f' in tag:
                flair_key = 'contains(' + trs + ", 'gay') or contains(" + trs + ", 'yiff') or contains(" + trs + ", 'female')"
            if 'm' in tag:
                flair_key = 'contains(' + trs + ", 'straight') or contains(" + trs + ", 'yiff')"
            else:
                log.error("Unexpexted '/' in tag")
        else:
            flair_key = 'contains(' + trs + ", 'gay') or contains(" + trs + ", 'solo') or contains(" + trs + ", 'female')"
    return flair_key


with open('config.yaml', 'r') as (stream):
    try:
        parameters = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        try:
            raise exc
        finally:
            exc = None
            del exc

red_title = parameters.get('red_title')

def parse():
    parse_flair(red_title=red_title)


parse()
