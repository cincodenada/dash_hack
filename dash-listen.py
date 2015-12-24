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
import urllib2
import time

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

oldtime = time.time()
print "Dash Command 1.0 Started"

# Use your own IFTTT key, not this fake one
ifttt_key = 'YOUR MAKER API KEY HERE GET IT AT https://ifttt.com/maker'
# Set these up at https://ifttt.com/maker
ifttt_url_goodnight_1 = 'https://maker.ifttt.com/trigger/goodnight_dash_1/with/key/' + ifttt_key
ifttt_url_arcade_on = 'https://maker.ifttt.com/trigger/arcade_on/with/key/' + ifttt_key
ifttt_url_arcade_off = 'https://maker.ifttt.com/trigger/arcade_off/with/key/' + ifttt_key

# Replace these fake MAC addresses and nicknames with your own
macs = {
    '465855866979' : 'dash_dixie_goodnight_1',
    '235465768699' : 'arcade_on',
    '346586986069' : 'arcade_off'

}

# Trigger a IFTTT URL. Body includes JSON with timestamp values.
def trigger_url(url):
    data = '{ "value1" : "' + time.strftime("%Y-%m-%d") + '", "value2" : "' + time.strftime("%H:%M") + '" }'
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()
    return response

def do_goodnight():
    print 'Shortcut Goodnight Triggered: ' + trigger_url(ifttt_url_goodnight_1)

def arcade_on():
    print 'Firing up the Arcade: ' + trigger_url(ifttt_url_arcade_on)

def arcade_off():
    print 'Shutting down the Arcade: ' + trigger_url(ifttt_url_arcade_off)

rawSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))

while True:
    packet = rawSocket.recvfrom(2048)
    ethernet_header = packet[0][0:14]
    ethernet_detailed = struct.unpack("!6s6s2s", ethernet_header)
    arp_header = packet[0][14:42]
    arp_detailed = struct.unpack("2s2s1s1s2s6s4s6s4s", arp_header)
    # skip non-ARP packets
    ethertype = ethernet_detailed[2]
    if ethertype != '\x08\x06':
        continue
    source_mac = binascii.hexlify(arp_detailed[5])
    source_ip = socket.inet_ntoa(arp_detailed[6])
    dest_ip = socket.inet_ntoa(arp_detailed[8])
    if source_mac in macs:
        #print "ARP from " + macs[source_mac] + " with IP " + source_ip
        if macs[source_mac] == 'dash_dixie_goodnight_1':
           if time.time() - oldtime > 15:
              do_goodnight()
              oldtime = time.time()
           else:
              print "Shorcut Triggered Once"
              
        if macs[source_mac] == 'arcade_on':
           if time.time() - oldtime > 15:
              arcade_on()
              oldtime = time.time()
           else:
              print "Shortcut Triggered Once"

        if macs[source_mac] == 'arcade_off':
           if time.time() - oldtime > 15:
              arcade_off()
              oldtime = time.time()
           else:
              print "Shortcut Triggered Once"

