#!/usr/bin/env python

import argparse
import os

from pyunifi.controller import Controller

def getFixedClients():
    clients = controller.get_clients()
    fixed_clients = [c for c in clients if c.get("use_fixedip", False) == True]
    fixed_clients.sort(key=lambda x: tuple(map(int, x.get('fixed_ip', '').split('.'))))
    aps = controller.get_aps()
    ap_names = dict([(ap['mac'], ap.get('name', '????')) for ap in aps])
    FORMAT = '%-15s\t%-30s\t%-18s\t%-12s\t%-4s\t%-4s\t%-3s\t%-3s\n'
    result = (FORMAT % ('ADDR', 'NAME', 'MAC', 'AP', 'CHAN', 'RSSI', 'RX', 'TX'))
    for client in fixed_clients:
        ap_name = ap_names.get(client.get('ap_mac', '????'), '????')
        ap_name = (ap_name[:9] + '...') if len(ap_name) > 12 else ap_name
        name = client.get('hostname') or client.get('name') or client.get('ip', '????')
        rssi = client.get('rssi', '????')
        mac = client.get('mac', '????')
        rx = int(client.get('rx_rate', 0) / 1000)
        tx = int(client.get('tx_rate', 0) / 1000)
        channel = client.get('channel','????')
        ip = client.get('fixed_ip', '????')
        result += (FORMAT % (ip, name, mac, ap_name, channel, rssi, rx, tx))
    return result

def getHosts():
    clients = controller.get_clients()
    fixed_clients = [c for c in clients if c.get("use_fixedip", False) == True]
    fixed_clients.sort(key=lambda x: tuple(map(int, x.get('fixed_ip', '').split('.'))))
    FORMAT = '%s\t%s\n'
    result = ''
    for client in fixed_clients:
        name = client.get('hostname') or client.get('name') or client.get('ip', '????')
        ip = client.get('fixed_ip', '????')
        result += (FORMAT % (ip, name))
    return result

if __name__ == '__main__':
    config = {}
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--controller', default='unifi', help='the controller address (default "unifi")')
    parser.add_argument('-p', '--port', default='443', help='the controller port (default "443")')
    parser.add_argument('-u', '--username', default='admin', help='the controller username (default("admin")')
    parser.add_argument('-P', '--password', default='', help='the controller password')
    parser.add_argument('-v', '--version', default='UDMP-unifiOS', help='the controller base version (default "UDMP-unifiOS")')
    parser.add_argument('-s', '--siteid', default='default', help='the site ID, UniFi >=3.x only (default "default")')
    parser.add_argument('-V', '--ssl-verify', default=False, action='store_true', help='verify ssl certificates')
    parser.add_argument('-C', '--certificate', default='', help='verify with ssl certificate pem file')
    parser.add_argument('--config', default='', help='config file with format argument=value')
    parser.add_argument('command', nargs='?', default='hosts')
    args = parser.parse_args()

    #first write config file valued to config{}
    if args.config != '' and os.path.isfile(args.config):
        with open(args.config) as configfile:
            for line in configfile:
                name, var = line.partition("=")[::2]
                if name.strip()[0] != '#':
                    config[name.strip()] = var
    #then overwrite config{} with any specified command line values or defaults
    for arg in vars(args):
        config[arg]=getattr(args, arg)

    if not config["ssl_verify"]:
        # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        pass
    elif config["ssl_verify"] and len(config["certificate"]) > 0:
        config["ssl_verify"] = config["certificate"]

    # setup commands
    command = args.command.lower()
    commands = {
        'fixedclients': getFixedClients,
        'hosts': getHosts,
    }

    if command in commands:
        controller = Controller(config["controller"], config["username"], config["password"], config["port"], config["version"], ssl_verify=config["ssl_verify"])
        print(commands[command]())
    else:
        print("command %s not implemented" % command)




"""
sites = controller.get_sites()
users = controller.get_users()
"""
