#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import urllib
import urllib2
import logging
import md5
import requests

HOST = 'http://127.0.0.1:8005'
DOWNLOAD_LIST_URI = '%s/download_list' % HOST
DOWNLOAD_TAG_URI = '%s/' % HOST
DOWNLOAD_TAG_FNAME = 'finish'

def calc_str_md5(tgt):
    return md5.new(tgt).hexdigest()

def start_supervised_download():
    """
    """
    prev_dl_md5 = ''
    while True:
        # sleep 5 seconds anyway
        time.sleep(2)
        # step 1. download file-list
        try:
            dl_list = urllib2.urlopen(DOWNLOAD_LIST_URI).read()
        except Exception as e:
            logging.info(str(e))
            logging.info('download list uri %s not exists' % DOWNLOAD_LIST_URI)

            continue

        # step 2. download file-list, and download everything in file-list
        dl_md5 = calc_str_md5(dl_list)
        if dl_md5 == prev_dl_md5:
            logging.info('md5 not change, no more processing')
            continue
        else:
            prev_dl_md5 = dl_md5
            logging.info('got new dl-md5: %s' % prev_dl_md5)

        with open(DOWNLOAD_TAG_FNAME, 'w') as f:
            f.write(dl_list)
            f.close()

        print open(DOWNLOAD_TAG_FNAME).read()

        dl_name_list =  dl_list.strip().split('\n')
        for name in dl_name_list:
            url = '%s/%s' % (DOWNLOAD_LIST_URI.rsplit('/', 1)[0], name)
            cmd = 'wget -r %s' % url
            logging.warning('run cmd: %s' % cmd)
            os.system(cmd)
            print cmd

        # step 3. upload finish tag file
        files = {'file': (DOWNLOAD_TAG_FNAME,
                          open(DOWNLOAD_TAG_FNAME),
                          'text/plain')}
        resp = requests.post(DOWNLOAD_TAG_URI, files=files,
                             headers={'referer': '127.0.0.1'})

if __name__ == '__main__':
    # change log level, for debug
    logging.basicConfig(level=logging.DEBUG)
    start_supervised_download()
