import math

HEIGHT=400
WIDTH=1000
X_MARGIN=50
Y_MARGIN=100
PLANET_BOX_Y_SEPARATION=20
PLANET_DISC_OVERLAP=50


class SvgWrapper:
    def __init__(self, svg):
        self.svg = svg
        self.planet_boxes = []

    def render(self, data):
        planet_count = len(data)
        box_height = (HEIGHT - 2 * Y_MARGIN - (planet_count - 1) * PLANET_BOX_Y_SEPARATION) / planet_count
        box_width = WIDTH - 2 * X_MARGIN
        box_x = X_MARGIN

        for planet_index in range(planet_count):
            box_y = Y_MARGIN + planet_index * (box_height + PLANET_BOX_Y_SEPARATION)
            self._add_moon_orbits(box_x, box_y, box_width, box_height, data[planet_index])

        for planet_index in range(planet_count):
            box_y = Y_MARGIN + planet_index * (box_height + PLANET_BOX_Y_SEPARATION)
            self._add_planet_box(box_x, box_y, box_width, box_height)

        for planet_index in range(planet_count):
            box_y = Y_MARGIN + planet_index * (box_height + PLANET_BOX_Y_SEPARATION)
            self._add_planet_disc(box_x, box_y, box_height, data[planet_index]['planet']['radius'] * WIDTH)

        for planet_index in range(planet_count):
            box_y = Y_MARGIN + planet_index * (box_height + PLANET_BOX_Y_SEPARATION)
            self._add_moon_orbit_arcs(box_x, box_y, box_width, box_height, data[planet_index])

    def save(self, out_file):
        self.svg.add_substitutions({
            'height': HEIGHT,
            'width': WIDTH
        })

        self.svg.save(out_file)

    def _add_planet_box(self, x, y, w, h):
        self.svg.add_rectangle(x, y, w, h, 'planetBox')

    def _add_moon_orbits(self, x, y, w, h, planet_data):
        planet_radius = planet_data['planet']['radius'] * WIDTH
        for moon in planet_data['moons']:
            self._add_moon_orbit(moon, x + PLANET_DISC_OVERLAP - planet_radius, y + h/2, planet_radius)

    def _add_moon_orbit_arcs(self, x, y, w, h, planet_data):
        planet_radius = planet_data['planet']['radius'] * WIDTH
        for moon in planet_data['moons']:
            self._add_moon_orbit_arc(y, h, moon, x + PLANET_DISC_OVERLAP - planet_radius,planet_radius)

    def _add_planet_disc(self, x, y, h, radius):
        diameter = 2 * radius
        if diameter < PLANET_DISC_OVERLAP and diameter < h:
            '''
            ┌────
            │  +
            │ +++   Whole disc is visible
            │  +
            └────
            '''
            self.svg.add_circle(x + PLANET_DISC_OVERLAP - radius, y + h/2, radius, 'planetDisc')

        elif h > diameter >= PLANET_DISC_OVERLAP:
            '''
            ┌───
            │++
            │+++    Major segment of disc is visible
            │++
            └───
            '''
            arc_h = math.sqrt(radius * radius - (radius - (2 * radius - PLANET_DISC_OVERLAP)) ** 2)
            self.svg.add_circle_arc(x, y + h/2 - arc_h, x, y + h/2 + arc_h, radius, True, True, 'planetDisc')

        elif h <= diameter < PLANET_DISC_OVERLAP:
            '''
            ┌───────
            │  ++++
            │ ++++++ Top and bottom parts of disc are chopped off
            │  ++++
            └───────
            '''
            x1 = PLANET_DISC_OVERLAP - (radius - math.sqrt(radius ** 2 - (h**2)/4))
            x2 = PLANET_DISC_OVERLAP - diameter + math.sqrt(radius ** 2 - (h**2)/4)
            self.svg.add_circle_arc(x + x1, y, x + x1, y + h, radius, False, True, 'planetDisc')
            self.svg.add_circle_arc(x + x2, y, x + x2, y + h, radius, False, False, 'planetDisc')

        else:
            '''
            ┌──
            │+
            │++     Minor segment of disc is visible
            │+
            └──
            '''
            assert diameter >= PLANET_DISC_OVERLAP and diameter >= h
            arc_x = PLANET_DISC_OVERLAP - (radius - math.sqrt(radius * radius - h * h / 4))
            self.svg.add_circle_arc(x + arc_x, y, x + arc_x, y + h, radius, False, True, 'planetDisc')

    def _add_moon_orbit(self, moon, planet_center_x, planet_center_y, planet_radius):
        self.svg.add_circle(planet_center_x, planet_center_y, moon['x'] * WIDTH + planet_radius, 'moonOrbit')

    def _add_moon_orbit_arc(self, y, h, moon, planet_center_x, planet_radius):
        r = moon['x'] * WIDTH + planet_radius
        x = planet_center_x + math.sqrt(r ** 2 - h * h / 4)
        self.svg.add_circle_arc(x, y, x, y+h, r, False, True, 'moonOrbitArc')
