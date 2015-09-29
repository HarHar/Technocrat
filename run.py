#!/usr/bin/env python2
# -*- encoding: utf8 -*-
import sys
sys.dont_write_bytecode = True

import time
import subprocess

# start web stuff
subprocess.Popen(['./webstuff.py'])

# start irc stuff
subprocess.Popen(['./ircstuff.py'])

while True:
	time.sleep(3600)