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
client = Client('irc.broke-it.com', nick=nick)
for channel in channels: client.channel(channel).join()

import storage
import modules

# good things to remember:
# client.msg(target, msg)
# client._channels = list of channels
# client._channels['#/g/bots'].users['@'] = list of operators on #/g/bots (includes @ and up)
# client._channels['#/g/bots'].only('@') = list of operators on #/g/bots (ONLY @)

@client.handler(command='PRIVMSG')
def handle_privmsg(client, payload):
	"""
		Handles messages

		payload properties:	
			sender = who sent "harhar"
			target = who received (chan/user) "#/g/bots"
			host = sender's host "my.vhost"
			user = username part of host "~harhar" from "~harhar@my.vhost"
			params[1] = message
	"""
	pass

@client.handler(command='KICK')
def handle_kick(client, payload):
	"""
		Handles kicks
			- payload.params == ['#channel', 'kickednick', 'reason']

	"""
	pass

@client.handler(command='INVITE')
def handle_invite(client, payload):
	print 'invite ' + repr(payload.params)

@client.handler(command='JOIN')
def handle_join(client, payload):
	""" Handles joins:

		payload properties:
			- nick = 'nick'
			- host = 'host.name'
			- user = '~user'
			- params[0] = '#channel'
	"""
	pass

@client.handler(command='PART')
def handle_part(client, payload):
	print 'part ' + repr(payload.params)
	print payload.nick

@client.handler(command='QUIT')
def handle_quit(client, payload):
	""" Handles quit messages from other users

		payload properties:
			- message: quit message
	"""
	print 'quit ' + repr(payload.params)

@client.handler(command='NICK')
def handle_nick(client, payload):
	""" Handles own nick change

		payload properties:
			- nickname: new nick
	"""
	print 'nick ' + repr(payload.params)

@client.handler(command='MODE')
def handle_mode(client, payload):
	""" Handles mode changes

		Can be mode change of our own nick (2 params)
		Can be mode change of a channel (3+ params)

		Example:
			payload.params == ['OurBot', '+ix']
			payload.params == ['#channel', '+o', 'nickname']
	"""
	pass

@client.handler(command='WHOIS')
def handle_whois(client, payload):
	print 'whois ' + repr(payload.params)

client.start()
client.join()