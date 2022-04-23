class Planet:
	AU = 149.6e6 * 1000
	G = 6.7428e-11
	EM = 5.9742e24

	def __init__(self, x=0, y=0, radius=0, mass=0, color=()):
		self.x = x * self.AU
		self.y = y * self.AU
		self.radius = radius * self.AU
		self.mass = mass * self.EM
		self.color = color

		self.orbit = []
		self.division_cooldown = 5

		self.x_vel = 0
		self.y_vel = 0
