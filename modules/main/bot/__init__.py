if __name__ == '__main__': exit()

import traceback

class BotModule(object):
	def __init__(self):
		pass
	def onMessage(self, message, source, target):
		print('<' + source + ' on ' + target + '> ' + message)

def getModule():
	return {'name': 'main module', 'object': BotModule()}