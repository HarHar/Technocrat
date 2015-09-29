from girc import Client

nick = 'Technocrat'
client = Client('irc.rizon.net', nick=nick)
channel = client.channel('#/g/bots')

channel.join()
channel.msg('First message from this bot. Moment to stay on history')

@client.handler(command='PRIVMSG', payload=lambda value: nick in value.lower())
def mentioned(client, msg):
	channel.msg("Hello, {}".format(msg.sender))

def start():
	client.start()
	client.join()