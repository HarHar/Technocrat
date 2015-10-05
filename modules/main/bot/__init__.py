if __name__ == '__main__': exit()

class BotModule(object):
	def __init__(self):
		pass
	def onMessage(self, message, source):
		print('AYY MESSAGE: ' + repr(message) + ' from ' + repr(source))

def getModule():
	return {'name': 'main module', 'object': BotModule()}