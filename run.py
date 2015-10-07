#!/usr/bin/env python
# -*- encoding: utf8 -*-

########
# no ugly .pyc (hopefully)
import sys
sys.dont_write_bytecode = True
########

########
# check for first time user
import storage
if len(storage.db.data) == 0:
	print('Systems not configured!')
	print('Please use ./config.py')
	exit(1)
########

#########
# start stuff and go into idling
import time
import ircstuff
import webstuff
import threading

link = {'web': {}, 'irc': {}, 'common': {}}

ircThread = threading.Thread(target=ircstuff.main, args=(link,))
ircThread.setDaemon(True)
ircThread.start()

webThread = threading.Thread(target=webstuff.main, args=(link,))
webThread.setDaemon(True)
webThread.start()

while True:
	try:
		time.sleep(3600)
	except:
		import os
		os.kill(os.getpid(), 9) #typical of a harhar
#########