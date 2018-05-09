#!/usr/bin/env python2.7
# ~*~ coding: utf8 ~*~
# Port diff for linux
# Writen by: ry
# version: 2.0.1
#


# 
import sys
import shelve
import os.path
import subprocess


# Config
class Config:
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    TEMP_DIR = os.path.join(BASE_DIR, 'cache')
    DB_FILE = os.path.join(TEMP_DIR, 'listen.db')
    DB_INDEX = 'ftMMJEuuHJZcd'
    BIN_SS = os.path.join(BASE_DIR, 'scan_listen_port')
    BIN_EGREP = os.path.join(BASE_DIR, 'find_string')

# Get command
try:
    command = sys.argv[1]
except IndexError:
    sys.stderr.write('Usage: %s port_diff|tcp_syn_check|tcp_estab_check\n' % __file__)
    exit(1)

# Get link all
shell = """ \
      %s -atun | \
      %s '^udp|^tcp' """ % \
      (Config.BIN_SS, Config.BIN_EGREP)

result = subprocess.check_output(shell, shell=True)

def link(method):
    link_choall = []
    if result:
        for x in result.strip().split('\n'):
            row = x.split()
            protocal = row[0]
            state = row[1]
            local_port = row[4].split(':')[-1]
            if isinstance(method, (list, tuple)):
                for _m in method:
                    if _m == state:
                        link_choall.append((local_port, protocal))
            else:
                if method == state:
                    link_choall.append((local_port, protocal))
    else:
        return []
    return link_choall

if command == 'port_diff':
    # tcp state: LISTEN, udp state: UNCONN
    listen_port = link(('LISTEN', 'UNCONN'))
    if listen_port:
        listen_port = set(listen_port)
    else:
        sys.stdout.write('Not find tcp or udp listen port.')
        exit(1)

    try:
        db = shelve.open(Config.DB_FILE)
    except:
        sys.stdout.write('Listen DB error[%s].' % Config.DB_FILE)
        exit(1)

    old_list = db.get(Config.DB_INDEX)

    if old_list:
        result = ''
        miss = list(old_list - listen_port)
        add = list(listen_port - old_list)
        if miss:
            result += 'Port to reduce: %s. ' % (miss.__str__())
        if add:
            result += 'The port to increase: %s' % (add.__str__())
        if result:
            sys.stdout.write(result)
        else:
            sys.stdout.write('OK')
    else:
        sys.stdout.write('OK')

    # Save this list
    db[Config.DB_INDEX] = listen_port

    # Close db
    db.close()
elif command == 'tcp_syn_check':
    sys.stdout.write(link('SYN-RECV').__len__().__str__())
elif command == 'tcp_estab_check':
    sys.stdout.write(link('ESTAB').__len__().__str__())
else:
    sys.stderr.write('Usage: %s port_diff|tcp_syn_check|tcp_estab_check\n' % __file__)
    exit(1)
