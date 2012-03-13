#!/usr/bin/env python
# -*- encoding=utf-8 -*-
""" Ban the ip address when netstat show that
there are too much connection from target ip using iptables

root required
"""

import os

white_list = ['127.0.0.1']
max_conn_count = 30

if __name__ == '__main__':
    cmd_str = "netstat -ntu | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -n |tail -n 10"

    lines = os.popen(cmd_str).readlines()
    for line in lines:
        items = line.strip().split()
        if len(items) == 2:
            count, ip = items
            print count, ip
            if (int(count) > max_conn_count) and (ip not in white_list):
                print 'start to block ', count, ip
                ips = ip.split('.')
                map(lambda ip_sec: int(ip_sec), ips)
                os.system('iptables -A INPUT -p tcp --dport 80 -j DROP -s %s' % ip)

