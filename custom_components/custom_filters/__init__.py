"""Support custom filters for jinja"""
import urllib.parse
import hashlib

from random import Random, SystemRandom, shuffle

from homeassistant.helpers import template

DOMAIN = 'custom_filters'


async def async_setup(hass, config):
    _TemplateEnvironment = template.TemplateEnvironment

    def unquote(string):
        return urllib.parse.unquote(string)

    def ternary(value, true_val, false_val, none_val=None):
        '''  value ? true_val : false_val '''
        if value is None and none_val is not None:
            return none_val
        elif bool(value):
            return true_val
        else:
            return false_val

    def randomize_list(mylist, seed=None):
        try:
            mylist = list(mylist)
            if seed:
                r = Random(seed)
                r.shuffle(mylist)
            else:
                shuffle(mylist)
        except Exception:
            pass
        return mylist


    def init(*args):
        env = _TemplateEnvironment(*args)

        env.filters['unquote'] = unquote
        env.filters['urldecode'] = unquote
        env.filters['ternary'] = ternary
        env.filters['shuffle'] = randomize_list

        return env

    template.TemplateEnvironment = init

    return True
