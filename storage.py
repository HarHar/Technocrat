from lockfile import LockFile
import json
import os.path
class Database(object):
	dbfile = 'database.json'
	lockfile = '/tmp/technocrat_db.lock'
	def __init__(self, dbfile=None, lockfile=None):
		if dbfile: self.dbfile = dbfile
		if lockfile: self.lockfile = lockfile

		self.lock = LockFile(self.lockfile)
		self.data = {}

		self.load()
	def save(self):
		with self.lock:
			f = open(self.dbfile, 'w')
			f.write(json.dumps(self.data))
			f.close()
	def load(self):
		with self.lock:
			if os.path.exists(self.dbfile):
				f = open(self.dbfile, 'r')
				self.data = json.loads(f.read())
				f.close()
		self.save()

db = Database()