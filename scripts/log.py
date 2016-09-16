import os, sys

class Tee:
	def __init__(self, name, mode):
		self.file = open(name, mode)
	def __del__(self):
		self.file.close()
	def write(self, data):
		sys.stdout.write(data)
		self.file.write(data)
		self.file.flush()

log_file = os.getenv("log_file","install.log")
log = Tee(log_file, "a")