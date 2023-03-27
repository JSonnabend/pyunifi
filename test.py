#!/usr/bin/env python

import argparse

from pyunifi.controller import Controller

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--controller', default='unifi', help='the controller address (default "unifi")')
parser.add_argument('-u', '--username', default='admin', help='the controller username (default("admin")')
parser.add_argument('-p', '--password', default='', help='the controller password')
parser.add_argument('-b', '--port', default='443', help='the controller port (default "443")')
parser.add_argument('-v', '--version', default='UDMP-unifiOS', help='the controller base version (default "UDMP-unifiOS")')
parser.add_argument('-s', '--siteid', default='default', help='the site ID, UniFi >=3.x only (default "default")')
parser.add_argument('-V', '--ssl-verify', default=False, action='store_true', help='verify ssl certificates')
parser.add_argument('-C', '--certificate', default='', help='verify with ssl certificate pem file')
args = parser.parse_args()

ssl_verify = (args.ssl_verify)

if ssl_verify and len(args.certificate) > 0:
        ssl_verify = args.certificate

controller = Controller(args.controller, args.username, args.password, args.port, args.version, args.siteid, ssl_verify=ssl_verify)

sites = controller.get_sites()
aps = controller.get_aps()
ap_names = dict([(ap['mac'], ap.get('name', '????')) for ap in aps])
clients = controller.get_clients()
fixed_clients = [c for c in clients if c.get("use_fixedip", False) == True]
fixed_clients.sort(key=lambda x: tuple(map(int, x.get('fixed_ip', '').split('.'))))
users = controller.get_users()

FORMAT = '%-15s\t%-30s  %-18s  %-12s  %-4s  %-4s  %-3s  %-3s'
print(FORMAT % ('ADDR', 'NAME', 'MAC', 'AP', 'CHAN', 'RSSI', 'RX', 'TX'))
for client in fixed_clients:
    ap_name = ap_names.get(client.get('ap_mac', '????'), '????')
    ap_name = (ap_name[:9] + '...') if len(ap_name) > 12 else ap_name
    name = client.get('name') or client.get('hostname') or client.get('ip', '????')
    rssi = client.get('rssi', '????')
    mac = client.get('mac', '????')
    rx = int(client.get('rx_rate', 0) / 1000)
    tx = int(client.get('tx_rate', 0) / 1000)
    channel = client.get('channel','????')
    ip = client.get('fixed_ip', '????')

    print(FORMAT % (ip, name, mac, ap_name, channel, rssi, rx, tx))
