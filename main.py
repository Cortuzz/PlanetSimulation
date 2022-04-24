import math
import random
import pygame
from planet import Planet

random.seed(765)
pygame.init()
WIDTH, HEIGHT = 2000, 1200
SCALE = 0.1 / Planet.AU
RADIUS_SCALE = 500
TIMESTEP = 3600 * 24 * 500
MAX_ORBIT = 1000
BOUNCING = False
DIVIDING = False
SMART = False
DESTROYING = True

surface = pygame.display.set_mode((WIDTH, HEIGHT))


def smart_destroying(planet, destroyed_planet):
	if planet.mass / destroyed_planet.mass >= 100:
		return absorb_planet(planet, destroyed_planet)
	return divide_planet(planet, destroyed_planet)


def absorb_planet(planet, absorbed_planet):
	planet.mass += absorbed_planet.mass
	planet.radius += absorbed_planet.radius

	force = get_force(planet, absorbed_planet)
	planet.x_vel += TIMESTEP * force[0] / planet.mass
	planet.y_vel += TIMESTEP * force[1] / planet.mass

	planets.remove(absorbed_planet)


def divide_planet(planet, divided_planet):
	if divided_planet.division_cooldown > 0:
		return False

	new_planet1 = Planet(color=divided_planet.color)
	new_planet2 = Planet(color=divided_planet.color)

	new_planet1.x = 1.0001 * divided_planet.x
	new_planet1.y = divided_planet.y
	new_planet2.x = divided_planet.x
	new_planet2.y = 1.0001 * divided_planet.y

	new_planet1.mass = divided_planet.mass / 4
	new_planet2.mass = divided_planet.mass / 4

	new_planet1.radius = 2 * divided_planet.radius / 3
	new_planet2.radius = 2 * divided_planet.radius / 3

	new_planet1.x_vel = -divided_planet.x_vel / 4
	new_planet1.y_vel = divided_planet.y_vel / 4

	new_planet2.x_vel = divided_planet.x_vel / 4
	new_planet2.y_vel = -divided_planet.y_vel / 4

	planets.remove(divided_planet)
	planets.append(new_planet1)
	planets.append(new_planet2)

	return True


def get_random_color():
	return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def check_in(planet1, planet2):
	x1, y1, x2, y2 = planet1.x, planet1.y, planet2.x, planet2.y

	x_dist = x1 - x2
	y_dist = y1 - y2
	distance = math.sqrt(x_dist**2 + y_dist**2)

	if distance < RADIUS_SCALE * max(planet1.radius, planet2.radius):
		return True

	return False


def update_planet(planet):
	fx, fy = 0, 0

	for pl in planets:
		if pl == planet:
			continue

		if DESTROYING and check_in(pl, planet):
			if SMART:
				func = smart_destroying
			elif DIVIDING:
				func = divide_planet
			else:
				func = absorb_planet

			if planet.mass > pl.mass:
				if func(planet, pl):
					return
			else:
				if func(pl, planet):
					return

		force = get_force(planet, pl)
		fx += force[0]
		fy += force[1]

	planet.x_vel += TIMESTEP * fx / planet.mass
	planet.y_vel += TIMESTEP * fy / planet.mass

	if BOUNCING:
		normalized = normalize_coords(planet.x, planet.y)
		if not (0 < normalized[0] < WIDTH):
			planet.x_vel *= -1
		if not (0 < normalized[1] < HEIGHT):
			planet.y_vel *= -1

	planet.x += TIMESTEP * planet.x_vel
	planet.y += TIMESTEP * planet.y_vel

	planet.orbit.append([planet.x, planet.y])
	planet.division_cooldown -= 1

	if len(planet.orbit) > MAX_ORBIT:
		planet.orbit.pop(0)


def get_force(planet1, planet2):
	x1, y1, x2, y2 = planet1.x, planet1.y, planet2.x, planet2.y

	x_dist = x2 - x1
	y_dist = y2 - y1
	distance = math.sqrt(x_dist**2 + y_dist**2)

	force = Planet.G * planet1.mass * planet2.mass / distance**2
	angle = math.atan2(y_dist, x_dist)

	force_x = force * math.cos(angle)
	force_y = force * math.sin(angle)

	return force_x, force_y


def init_planets():
	_planets = [
		#Planet(1000, 1000, 0.3, 1e9, (255, 255, 0)),
		Planet(1300, 1400, 0.2, 1e1, (255, 60, 60)),
		Planet(-1000, -1000, 1, 1e10, (get_random_color())),
		Planet(-1000, -240, 0.2, 1e1, (get_random_color()))
	]

	#_planets[1].y_vel = 10 * 1000

	_planets[0].x_vel = -80 * 1000
	_planets[2].x_vel = -185 * 1000
	#_planets[1].x_vel = -230 * 1000

	return _planets


def normalize_coords(x, y):
	return int(x * SCALE + WIDTH / 2), int(y * SCALE + HEIGHT / 2)


def draw_planet(planet):
	normalized_coords = normalize_coords(planet.x, planet.y)
	normalized_radius = int(RADIUS_SCALE * planet.radius * SCALE)

	pygame.draw.circle(surface, planet.color, normalized_coords, normalized_radius)

	for i in range(len(planet.orbit) - 1):
		o1 = planet.orbit[i]
		o2 = planet.orbit[i + 1]

		pygame.draw.line(surface, (255, 255, 255), normalize_coords(o1[0], o1[1]), normalize_coords(o2[0], o2[1]))


def main_loop(_planets):
	for pl in _planets:
		update_planet(pl)
		draw_planet(pl)


if __name__ == "__main__":
	running = True
	clock = pygame.time.Clock()
	planets = init_planets()

	while running:
		clock.tick(60)
		main_loop(planets)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		pygame.display.update()
		surface.fill((0, 0, 0))

	pygame.quit()
