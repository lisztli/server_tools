#!/usr/bin/env python
# -*- encoding=utf-8 -*-

import time
import os
import sys

if __name__ == '__main__':
    #config
    target_dir = '/home/liszt/db_bak'

    db_user = ''
    db_pwd = ''
    db_host = '127.0.0.1'
    
    db_names = ['db1', 'db2']

    if len(sys.argv) > 1:
        target_dir = sys.argv[1]

    if not os.path.exists(target_dir):
        print 'target dir doesnt exists', target_dir
        sys.exit(0)

    today_str = time.strftime('%y%m%d_%H%M', time.gmtime())
    today_dir = '%s/%s' %(target_dir, today_str)
    
    os.mkdir(today_dir)

    #dump dbs
    for db_name in db_names:
        sql_file = '%s/%s_%s.sql.zip' % (today_dir, db_name, today_str)
        dump_str = 'mysqldump -u%s -p%s -h%s %s | gzip --best -c -f > %s' % (db_user,
                                                                             db_pwd,
                                                                             db_host,
                                                                             db_name,
                                                                             sql_file)
        print dump_str
        os.system(dump_str)

