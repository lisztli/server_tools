#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import sys
import urllib
import urllib2
import logging

DOWNLOAD_LIST_FNAME = 'download_list'
DOWNLOAD_TAG_FNAME = 'finish'

def generate_job(file_path):
    """

    Arguments:
    - `file_path`:
    """
    with open(DOWNLOAD_LIST_FNAME, 'w') as f:
        f.write(file_path)
        f.close()

    while True:
        try:
            if os.path.exists(DOWNLOAD_TAG_FNAME):
                with open(DOWNLOAD_TAG_FNAME) as f:
                    cnt = f.read()
                    if cnt.strip() == file_path:
                        cmd = 'rm -rf %s' % file_path
                        logging.warning(cmd)
                        # FIXME
                        # os.system(cmd)
                        break

            time.sleep(5)
        except Exception as e:
            logging.warning(str(e))

if __name__ == '__main__':
    for i in ['2016%02d' % i for i in range(1, 13)]:
        # os.system('hadoop fs -get %s .' %i)
        generate_job(i)
