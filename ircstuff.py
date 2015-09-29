#!/usr/bin/env python2
# -*- encoding: utf8 -*-
import sys
sys.dont_write_bytecode = True

from girc import Client

nick = 'Technocrat'
client = Client('irc.cyberdynesystems.net', nick=nick)
channel = client.channel('#/g/bots')

channel.join()
channel.msg('Hello')

@client.handler(command='PRIVMSG', payload=lambda value: nick in value.lower())
def mentioned(client, msg):
	channel.msg("Hello, {}".format(msg.sender))

client.start()
client.join()