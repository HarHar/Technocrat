#!/usr/bin/env python
# -*- encoding: utf8 -*-

########
# no ugly .pyc (hopefully)
import sys
sys.dont_write_bytecode = True
########

#########
# start stuff and go into idling
import time
import ircstuff
import webstuff
import threading

ircThread = threading.Thread(target=ircstuff.main)
ircThread.setDaemon(True)
ircThread.start()

webThread = threading.Thread(target=webstuff.main)
webThread.setDaemon(True)
webThread.start()

while True:
	try:
		time.sleep(3600)
	except:
		import os
		os.kill(os.getpid(), 9) #typical of a harhar
#########