#!/usr/bin/env python2
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
import subprocess

# start web stuff
subprocess.Popen(['./webstuff.py'])

# start irc stuff
subprocess.Popen(['./ircstuff.py'])

while True:
	time.sleep(3600)
#########