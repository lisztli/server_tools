#!/usr/bin/env python
# -*- encoding=utf-8 -*-
"""  
Sync from server to local machine on both Win & Linux
Add config in sync.cfg to config the sync parameters
and make sure you add your pub key to authorized_keys on remote
server.
"""

import os
import sys
import ConfigParser

class Syncer():
    def __init__(self):
        #rsync command path
        self.rsync_cmd = 'd:\\software\\cwRsync\\bin\\rsync.exe'
        self.ssh_cmd = 'd:\\software\\cwRsync\\bin\\ssh.exe'
        #private key path
        self.id_rsa_path = 'd:\\software\\pietty\\ssh\\id_rsa'
        #where to store the backup files
        self.target_path = 'd:\\work\\bk'
        self.user = 'liszt'
        self.host = ''
        
        #rsync path on server
        self.rsync_path = '/home/liszt/bin/rsync'
        #where to backup
        self.source = '/var/log/'
        self.exclude_from = 'd:\\work\\bk\\exclude.txt'
        self.exclude = ''
        self.include_from = ''
        self.include = ''
        
    def merge_config(self, conf):
        for key in conf.keys():
            setattr(self, key, conf[key])

    @staticmethod
    def massage_win_path(path):
        if os.name == 'nt':
            return '/cygdrive/%s' % path.replace(':', '').replace('\\', '/')
        return path

    def get_target_dir(self):
        #create target dir
        try:
            os.makedirs(self.target_path)
        except Exception, e:
            print e
        return Syncer.massage_win_path(self.target_path)

    def get_ssh_cmd(self):
        key_path = Syncer.massage_win_path(self.id_rsa_path)
        return '-e "%s -i %s"' % (self.ssh_cmd, key_path)

    def get_rsync_cmd(self):
        return '--rsync-path="%s"' % self.rsync_path

    def get_exclude_cmd(self):
        if self.exclude_from:
            return '--exclude-from="%s"' % Syncer.massage_win_path(self.exclude_from)
        if self.exclude:
            return '--exclude="%s"' % self.exclude
        return ''

    def get_include_cmd(self):
        if self.include_from:
            return '--include-from="%s"' % Syncer.massage_win_path(self.include_from)
        if self.include:
            return '--include="%s"' % self.include
        return ''

    def get_cmd(self):
        target = self.get_target_dir()
        ssh_cmd = self.get_ssh_cmd()
        rsync_cmd = self.get_rsync_cmd()
        exclude_cmd = self.get_exclude_cmd()
        include_cmd = self.get_include_cmd()
        source = '%s@%s:%s' % (self.user,
                self.host,
                self.source)

        final_cmd = '%s -avz -P %s %s %s %s "%s" "%s"' % (self.rsync_cmd,
                                                          rsync_cmd,
                                                          include_cmd,
                                                          exclude_cmd,
                                                          ssh_cmd,
                                                          source,
                                                          target)
        print final_cmd
        try:
            os.system(final_cmd)
        except Exception, e:
            print e

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'input a cfg file path'
        sys.exit(0)
        
    if not os.path.isfile(sys.argv[1]):
        print 'use a file path'
        sys.exit(0)

    target_sections = sys.argv[2:]

    config = ConfigParser.ConfigParser()
    config.read(sys.argv[1])

    if not target_sections:
        target_sections = config.sections() 

    for sec in target_sections:
        print sec
        try:
            sec_dict = dict(config.items(sec))
        except Exception, e:
            print '[Error] parse section %s met error: %s' % (sec, e)
            continue
        syncer = Syncer()
        syncer.merge_config(sec_dict)
        syncer.get_cmd()

