#!/usr/bin/env python2
# -*- encoding: utf8 -*-
import sys
import eventlet
import webstuff
import ircstuff
import time
sys.dont_write_bytecode = True

# start web stuff
eventlet.spawn(webstuff.start)

# start irc stuff
eventlet.spawn(ircstuff.start)

while True:
	eventlet.sleep(3600)