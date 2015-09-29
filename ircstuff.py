#!/usr/bin/env python2
# -*- encoding: utf8 -*-
import sys
sys.dont_write_bytecode = True

from girc import Client

nick = 'Technocrat'
client = Client('irc.broke-it.com', nick=nick)
channel = client.channel('#/g/bots')

channel.join()
#channel.msg('Hello')

@client.handler(command='PRIVMSG')
def mentioned(client, msg):
	channel.msg("Hello, {}".format(msg.sender))

client.start()
client.join()