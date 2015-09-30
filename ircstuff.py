#!/usr/bin/env python2
# -*- encoding: utf8 -*-
import sys
sys.dont_write_bytecode = True

import logging
logging.basicConfig()

from girc import Client
# db still not made, need to 
# load these things up from the bd
# when it's done
nick = 'TechBot'
channels = ['#Technocrat']
client = Client('localhost', nick=nick)
for channel in channels: client.channel(channel).join()

import modules

# good things to remember:
#  msg.sender = who sent "harhar"
#  msg.target = who received (chan/user) "#/g/bots"
#  msg.host = sender's host "my.vhost"
#  msg.user = username part of host "~harhar" from "~harhar@my.vhost"
#
# client._channels = list of channels
# client._channels['#/g/bots'].users['@'] = list of operators on #/g/bots (includes @ and up)
# client._channels['#/g/bots'].only('@') = list of operators on #/g/bots (ONLY @)

@client.handler(command='PRIVMSG')
def handle_privmsg(client, msg):
	pass
	#debugging:
	#print repr(msg)
	#if msg.sender == 'ne':
	#	client.msg(msg.target, repr(eval(msg.params[1])))

client.start()
client.join()