""" you yi si ma, damn eagle
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import datetime

# log releated
def fmt_msg_for_log(msg):
    """

    Arguments:
    - `msg`:
    """
    if isinstance(msg, str):
        return '[info=%s]' % msg
    elif isinstance(msg, dict):
        pair_gen = lambda k, v: '%s=%s' % (k, isinstance(v, str) and v or json.dumps(v))
        return '[%s]' % ']['.join(pair_gen(k, v) for k, v in msg.iteritems())
    else:
        return '[info=%s]' % json.dumps(msg)


def get_loggers(logger):
    """

    Arguments:
    - `logger`:
    """
    return map(lambda lg: lambda l, p='':(lg('[logtype=%s]%s' % (p, fmt_msg_for_log(l))), l)[1],
               map(lambda a: getattr(logger, a),
                   ('info', 'warning', 'error')))

# the datetime releated

def get_date_string(fmt_str='%Y%m%d', dt=None):
    """get the date string by now like '20150720'
    """
    if not dt:
        dt = datetime.datetime.now()
    return dt.strftime(fmt_str)


get_datehour_string = lambda dt=None: get_date_string('%Y%m%d%H', dt)
get_hour_string = lambda dt=None: get_date_string('%H', dt)

def get_prev_hour():
    """ get the string of previously hour
    """
    dt = datetime.datetime.now() + datetime.timedelta(hours=-1)
    return get_datehour_string(dt)


def get_prev_day():
    """ get the string of previously day
    """
    dt = datetime.datetime.now() + datetime.timedelta(days=-1)
    return get_date_string(dt=dt)


def get_now_readable(dt=None):
    """

    Arguments:
    - `dt`:
    """
    if not dt:
        dt = datetime.datetime.now()
    return dt.strftime('%x %X')



parse_day_string = lambda date_str: datetime.datetime.strptime(date_str, '%Y%m%d')
