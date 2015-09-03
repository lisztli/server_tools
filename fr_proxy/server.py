#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import signal
import gevent
from gevent.server import StreamServer
from gevent.socket import create_connection, gethostbyname

import cfg

class PortForwarder(StreamServer):

    def __init__(self, listener, **kwargs):
        StreamServer.__init__(self, listener, **kwargs)

    def handle(self, source, address):
        log('%s:%s accepted', *address[:2])
        try:
            f = source.makefile('r')
            # the token
            l = f.readline()
            if l[:-1] != cfg.handshake_token:
                self.close()
            log('handshake-token check ok')
            # the ssh info
            sshd_host = f.readline()[:-1]
            log('get-sshd-info: %s' % sshd_host)

            dest = create_connection(parse_address(sshd_host))
        except IOError, ex:
            log('%s:%s failed to connect to %s:%s: %s', address[0], address[1], self.dest[0], self.dest[1], ex)
            return
        except Exception as e:
            print str(e)
            return
        gevent.spawn(forward, source, dest)
        gevent.spawn(forward, dest, source)

    def close(self):
        if self.closed:
            sys.exit('Multiple exit signals received - aborting.')
        else:
            log('Closing listener socket')
            StreamServer.close(self)

def echo(source):
    f = source.makefile('r')
    for l in f:
        log('receive data: %s' % l)
        source.sendall(l)

def forward(source, dest):
    source_address = '%s:%s' % source.getpeername()[:2]
    dest_address = '%s:%s' % dest.getpeername()[:2]
    try:
        while True:
            data = source.recv(1024)
            log('%s->%s: %r', source_address, dest_address, data)
            if not data:
                break
            dest.sendall(data)
    finally:
        source.close()
        dest.close()


def parse_address(address):
    try:
        hostname, port = address.rsplit(':', 1)
        port = int(port)

    except ValueError:
        sys.exit('Expected HOST:PORT: %r' % address)
    return gethostbyname(hostname), port


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        sys.exit('Usage: %s source-address ' % __file__)
    source = args[0]
    server = PortForwarder(source)
    log('Starting port forwarder %s:%s', *(server.address[:2]))
    gevent.signal(signal.SIGTERM, server.close)
    gevent.signal(signal.SIGINT, server.close)
    server.serve_forever()


def log(message, *args):
    message = message % args
    sys.stderr.write(message + '\n')


if __name__ == '__main__':
    main()
