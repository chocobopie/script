from jnpr.junos import Device
from getpass import getpass
from jnpr.junos.utils.start_shell import StartShell
from pprint import pprint
from lxml import etree
import sys
import yaml
import json
import os
import re
import csv

#hostname = input("Local Node IP loopback: ")
#hostname2 = input("Peer Node IP loopback: ")
junos_username = ''
junos_password = ''
host_name = ''

debug_config = []
debug_arp = []

def get_device_name():
    hostname = None
    interfaces = {}
    
    dev = Device(host=host_name, user=junos_username, passwd=junos_password)
    print('Connecting ', host_name)
    
    #==========================================================================
    dev.open()
    
    configuration = dev.rpc.get_config(extensive=True)
    arp = dev.rpc.get_arp_table_information()
    
    dev.close()
    #==========================================================================
    
    hostname = configuration.find('.//host-name').text
    print('Device name: '+hostname)
    
    for i in configuration:
      debug_config.append(etree.tounicode(i, pretty_print=True))
    
    for i in arp:
       debug_arp.append(etree.tounicode(i, pretty_print=True))
      
    xml_interfaces = arp.findall('.//arp-table-entry')
    
    for i in xml_interfaces:
       result = re.search('\n(.*)\n', i.find('.//interface-name').text)
       interface_name = result.group(1)
       
       if interface_name.startswith('ge'):
        interfaces.setdefault(hostname, [])
        interfaces[hostname].append(interface_name.split('.')[0])
    
    interfaces_new = {a:list(set(b)) for a, b in interfaces.items()}
    
    #pprint(interfaces)
    pprint(interfaces_new)
    #x = interfaces.items()
    #print(x)
       
    


def save_file_debug():
    with open('C:\\Users\\kronk\\Desktop\\debug_config.txt', 'w') as f:
       for x in debug_config:
           f.write(f"{x}\n")
    f.close()
    
    with open('C:\\Users\\kronk\\Desktop\\debug_arp.txt', 'w') as f:
       for x in debug_arp:
           f.write(f"{x}\n")
    f.close() 
                
get_device_name()
save_file_debug()
