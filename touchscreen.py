class TouchScreen():

	MULTITOUCH = (47, 53, 54, 57)

	TOUCHSTART = 1
	TOUCHEND = 2
	TOUCHMOVE = 3

	def __init__(self, device='/dev/input/touchscreen'):
		from evdev import InputDevice
		self.ts = InputDevice(device)
		self.raw_pos = [-1,-1]
		self.d_pos = [-1,-1]
		self.pos = (-1,-1)
		self.button = None

		self.mt_slot = 0 
		self.raw_mt = [[-1,-1],[-1,-1]]

	def multitouch(self, e):
		if e.code == 47:
			self.mt_slot = e.value
		elif e.code == 57:
			if e.value == -1:
				self.raw_mt[self.mt_slot] = [-1,-1]
		else:
			self.raw_mt[self.mt_slot][e.code-53] = e.value

	def get_events(self):
		try:
			for e in self.ts.read():
				if e.type == 0:
					pass
				elif e.type == 1:
					self.button = e.value
					yield self.TOUCHSTART if self.button else self.TOUCHEND, self.pos
				elif e.code in self.MULTITOUCH:
					self.multitouch(e)
				elif e.code in (0, 1):
					self.d_pos[e.code] = self.raw_pos[e.code] - e.value
					yield self.TOUCHMOVE, tuple( self.d_pos )
					self.raw_pos[e.code] = e.value

			self.pos = ( self.raw_pos[1], self.raw_pos[0] )

		except BlockingIOError:
			pass

	def __repr__(self):
		return "<Pos: %s, Button: %s>" % ( self.pos, self.button )

if __name__ == "__main__":
	ts = TouchScreen()

	try:
		while True:
			for type, value in ts.get_events():
				if type == ts.TOUCHEND:
					print( ts )
	except KeyboardInterrupt:
		pass
