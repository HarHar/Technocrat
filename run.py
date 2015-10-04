#!/usr/bin/env python
# -*- encoding: utf8 -*-

########
# no ugly .pyc (hopefully)
import sys
sys.dont_write_bytecode = True
########

########
# clear subprocesses on exit
import os
os.setpgrp()

import signal
def cleanup(): os.killpg(0, signal.SIGTERM)

import atexit
atexit.register(cleanup)
#########

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
	time.sleep(3600)
#########