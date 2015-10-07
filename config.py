#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True
import storage

configurables = {'irchost': {'default': '', 'forHumans': 'IRC host to connect to', 'required': True, 'type': 'string'},
				'ircport': {'default': 6667, 'forHumans': 'IRC port to connect to', 'required': True, 'type': 'integer'},
				'ircnick': {'default': 'TechBot', 'forHumans': 'IRC nick to use', 'required': True, 'type': 'string'},
				'ircpassword': {'default': '', 'forHumans': 'IRC server password', 'required': False, 'type': 'string'},
				'ircnickservpwd': {'default': '', 'forHumans': 'IRC NickServ password', 'required': False, 'type': 'string'},
				'ircbotchannel': {'default': '', 'forHumans': 'IRC bot-testing channel', 'required': False, 'type': 'string'},
				'ircchannel': {'default': '', 'forHumans': 'Main IRC channel', 'required': True, 'type': 'string'},
				'webport': {'default': 80, 'forHumans': 'Website listening port', 'required': True, 'type': 'integer'}}

toconfigure = []

for arg in sys.argv:
	arg = arg.replace('-', '')
	if arg.lower() in configurables:
		print('Configuring ' + arg)
		toconfigure.append(arg.lower())

if (len(storage.db.data) == 0) or ('--all' in sys.argv):
	print('Configuring all options')
	print('')
	toconfigure = configurables.keys()

if len(toconfigure) > 0:
	print('* = required')
	for configOption in configurables:
		valid = False
		while not valid:
			sc = configurables[configOption] #sc -> ShortCut

			aux = ' [default=' + str(sc['default']) + ']' if sc['default'] else ''
			read = input(('(*) ' if sc['required'] else '') + sc['forHumans'] + aux + '> ')
			read = read.strip()

			if len(read) == 0 and (sc['default']):
				read = str(sc['default'])

			if sc['required'] and not read:
				print('This field is required')
				print('')
				continue
			if (sc['type'] == 'integer') and (not read.isdigit()):
				print('Number required!')
				print('')
				continue

			write = read
			if sc['type'] == 'integer': write = int(read)
			storage.db.data[configOption] = write
			valid = True
else:
	print('Nothing to configure!')
	print('Pass me one of these options or --all')
	print('')
	print(' '.join(configurables.keys()))
	exit(2)

storage.db.save()