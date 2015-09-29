#!/usr/bin/env python2
# -*- encoding: utf8 -*-
import sys
import threading
import webstuff
sys.dont_write_bytecode = True

# start web stuff
webThread = threading.Thread(target=webstuff.start())
webThread.setDaemon(True)
webThread.start()

# start irc stuff
pass