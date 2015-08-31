#!/usr/bin/python

import socket
import time
import os.path
from urllib2 import urlopen
from pygodaddy import GoDaddyClient
import logging
import sys

log = logging.getLogger('pygodaddy.client')
log.setLevel(logging.DEBUG)
format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(format)
log.addHandler(ch)


username = "YOURUSERNAME"
password = "YOURPASSWORD"
domains = ["@.domain1.net","@.domain2.com"]

wan_ip = urlopen('http://ip.42.pl/raw').read()

for domain in domains:
	realdomain = domain
	if realdomain.startswith("@."):
		realdomain = realdomain[2:]
	dom_ip = socket.gethostbyname(realdomain)
	if wan_ip != dom_ip:
		print '----------------------------------------------------'
		print 'GoDaddy A Record Update | ' + realdomain  + ' (' + domain + ') | ' + time.strftime("%a %d %B %I:%M %p")
		print 'WAN IP:\t\t' + wan_ip
		print 'Domain IP:\t' + dom_ip
		print 'IPs don\'t match, checking if already updated...'
		old_ip = '0'
		if os.path.isfile("/usr/local/etc/old_ips/" + realdomain):
			oipf = open("/usr/local/etc/old_ips/" + realdomain)
			old_ip = oipf.read()
			print 'Old IP:\t\t' + old_ip
		if wan_ip != old_ip:
			print 'Updating A Record...'
			client = GoDaddyClient()
			if client.login(username, password):
				client.update_dns_record(domain, wan_ip)
				nipf = open("/usr/local/etc/old_ip_" + realdomain, 'w+')
				nipf.write(wan_ip)
				nipf.close()
				print 'DNS has been updated.'
			else:
				print 'Failed to login, please check \'update-dns.py\''
		else:	
			print 'Already updated, dns not flushed.'	
