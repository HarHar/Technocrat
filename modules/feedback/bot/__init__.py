if __name__ == '__main__': exit()

import traceback
import cgi
import threading
import time

class BotModule(object):
	def __init__(self):
		pass
	def onMessage(self, message, source, target):
		pass

def getModule():
	return {'name': 'feedback module', 'object': BotModule()}