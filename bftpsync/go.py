""" you yi si ma, damn eagle!
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging.config
import helper
import sys
import os
import time
import shutil
import configparser
import subprocess
import threading

import datetime


def massage_path(path, date_map):
    """

    Arguments:
    - `path`:
    - `date_map`:
    """
    for k, v in date_map.iteritems():
        path = path.replace(k, v)
    return path


def get_date_map(task_cfg, cfg_section):
    hour_delay, day_delay, minute_delay = map(lambda option: task_cfg.getint(cfg_section, option),
                                             ('hour_delay',
                                              'day_delay',
                                              'minute_delay'))

    dt = datetime.datetime.now() + datetime.timedelta(hours=hour_delay,
                                                      days=day_delay,
                                                      minutes=minute_delay)
    min_massage = dt.replace(minute=dt.minute / 10 * 10)

    date_map = {'$date$': helper.get_date_string(dt=dt),
                '$hour$': helper.get_datehour_string(dt=dt),
                '$10min': helper.get_date_string('%Y%m%d%M',
                                                 dt=min_massage)}
    return date_map


def get_files_info(bns_name, source_path, target_path):
    """

    Arguments:
    - `bns_name`:
    - `source_path`:
    - `target_path`:
    """
    cmd = 'get_instance_by_service -Dp %s' % bns_name
    deploy_detail = subprocess.check_output(cmd,
                                            shell=True)
    line_parser = lambda ln: ('ftp://%s%s/%s' % (ln[0], ln[2], source_path),
                              '%s/%s.%s' % (target_path, ln[0], ln[1]))
    return [line_parser(l.split()) for l in deploy_detail.split('\n')
            if l]


def get_cmds(infos):
    """

    Arguments:
    - `infos`:
    """
    return ['wget -c "%s" -O "%s"' % info for info in infos]


def update_file(cmd):
    """

    Arguments:
    - `cmd`:
    """
    os.system(cmd)


def gen_task_info(task_cfg, cfg_section):
    """

    Arguments:
    - `date_str`:
    """
    bns_name, source_path, target_path = map(lambda option: task_cfg.get(cfg_section, option),
                                             ('bns_name',
                                              'source_path',
                                              'target_path'))
    date_map = get_date_map(task_cfg, cfg_section)
    source_path = massage_path(source_path, date_map)
    target_path = massage_path(target_path, date_map)
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    ths = []
    for cmd in get_cmds(get_files_info(bns_name,
                                       source_path,
                                       target_path)):
        print cmd
        t = threading.Thread(target=update_file, args=(cmd, ))
        ths.append(t)
        t.start()

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('tasks.conf')
    gen_task_info(config, 'erised')
