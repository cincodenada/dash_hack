# Fork of zippocage's modifications of Aaron Bell's script
# http://www.aaronbell.com/how-to-hack-amazons-wifi-button/

# improvement from forked script:
# Basic logging to file

# if you want to run this script as an ubuntu service, check out
# http://askubuntu.com/questions/175751/how-do-i-run-a-python-script-in-the-background-and-restart-it-after-a-crash

import socket
import struct
import binascii
import time
import json
import urllib.request, urllib.error, urllib.parse
import time
from dash_outputs import ifttt

# Implement Logging

import logging, sys

class LogFile(object):
    """File-like object to log text using the `logging` module."""

    def __init__(self, name=None):
        self.logger = logging.getLogger(name)

    def write(self, msg, level=logging.INFO):
        self.logger.log(level, msg)

    def flush(self):
        for handler in self.logger.handlers:
            handler.flush()

logging.basicConfig(level=logging.DEBUG, filename='/var/log/dash-command.log')

# Redirect stdout and stderr
sys.stdout = LogFile('stdout')
sys.stderr = LogFile('stderr')

# End Logging

amazon_prefixes = [
    b'\x44\x65\x0d',
]

oldtime = time.time() - 15
print("Dash Command 1.0 Started")

# Replace these fake MAC addresses and nicknames with your own
macs = {
    b'465855866979' : ('IFTTT', 'dash_dixie_goodnight_1'),
    b'235465768699' : ('IFTTT', 'arcade_on'),
    b'346586986069' : ('IFTTT', 'arcade_off'),
    b'1234deadbeef' : ('IFTTT', 'dash_pressed'),
}

rawSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))

outputs = {
    'IFTTT': ifttt.IFTTTOutput('YOUR MAKER API KEY HERE GET IT AT https://ifttt.com/maker')
}

while True:
    packet = rawSocket.recvfrom(2048)
    ethernet_header = packet[0][0:14]
    ethernet_detailed = struct.unpack("!6s3s3s2s", ethernet_header)
    arp_header = packet[0][14:42]
    arp_detailed = struct.unpack("2s2s1s1s2s6s4s6s4s", arp_header)
    # skip non-ARP packets
    ethertype = ethernet_detailed[3]
    ethersource = ethernet_detailed[1:2]
    if ethertype != b'\x08\x06':
        continue
    source_mac = binascii.hexlify(arp_detailed[5])
    source_ip = socket.inet_ntoa(arp_detailed[6])
    dest_ip = socket.inet_ntoa(arp_detailed[8])
    if source_mac in macs:
        #print "ARP from " + macs[source_mac] + " with IP " + source_ip
        if time.time() - oldtime > 15:
            (output, cmd) = macs[source_mac]
            outputs[output].trigger(cmd)
            oldtime = time.time()
        else:
            print("Shorcut Triggered Once")
    elif ethersource[0] in amazon_prefixes:
        print("Unknown dash button detected with MAC {}".format(source_mac))

