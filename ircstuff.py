#!/usr/bin/env python2
# -*- encoding: utf8 -*-
import sys
sys.dont_write_bytecode = True

from girc import Client
# db still not made, need to 
# load these things up from the bd
# when it's done
nick = 'Technocrat'
channels = ['#Technocrat']
client = Client('irc.broke-it.com', nick=nick)
for channel in channels: client.channel(channel).join()

import modules

# good things to remember:
#  msg.sender = who sent "harhar"
#  msg.target = who received (chan/user) "#/g/bots"
#  msg.host = sender's host "my.vhost"
#  msg.user = username part of host "~harhar" from "~harhar@my.vhost"

@client.handler(command='PRIVMSG')
def handle_privmsg(client, msg):
	pass

client.start()
client.join()