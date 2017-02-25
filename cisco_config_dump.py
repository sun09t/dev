#!/usr/bin/env python2.7
import Exscript.util.file as euf
import Exscript.util.start as eus    
import Exscript.util.match as eum     
import os
import time
import datetime
import re
hosts = euf.get_hosts_from_file('hosts.cfg')
accounts = euf.get_accounts_from_file('accounts.cfg')
def dump_config(job, host, conn):
		conn.execute('term len 0')       
		conn.execute('show run')
		config = conn.response.splitlines()
		hostname = eum.first_match(conn, r'^hostname\s(.+)$')
		if not hostname:
			m = re.search(r"([\w-]+)", config[-1])
			hostname = m.group(0)
		cfg_file = 'network_configs/' + hostname.strip() + '.cfg'
		for i in range(3):
				config.pop(i)
		config.pop(-0)
		config.pop(-1)
		with open(cfg_file, 'w') as f:
				for line in config:
						f.write(line + '\n')

eus.start(accounts, hosts, dump_config, max_threads=5) 
