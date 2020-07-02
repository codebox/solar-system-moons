import math
from orbit_box import OrbitBox

WIDTH=2000
X_MARGIN=50
TITLE_Y=70
ORBIT_BOX_Y=100
ORBIT_BOX_HEIGHT=400
BOX_Y_SEPARATION=30
BOX_X_MARGIN=40
BOX_Y_MARGIN=80

class SvgWrapper:
    def __init__(self, svg):
        self.svg = svg

    def render(self, data):
        planet_name = data['planet']['name']
        planet_radius = data['planet']['radius']
        moons = data['moons']
        self._render_title(planet_name)
        self._render_orbit_box(planet_name, planet_radius, moons)
        self._render_radius_box(data['moons'])

    def _render_title(self, planet_name):
        self.svg.add_text(TITLE_Y, planet_name)

    def _render_orbit_box(self, planet_name, planet_radius, moons):
        box_width = WIDTH - 2 * X_MARGIN
        box_height = ORBIT_BOX_HEIGHT
        box_x = X_MARGIN
        box_y = ORBIT_BOX_Y

        orbit_box = OrbitBox(planet_name, box_x, box_y, box_width, box_height, BOX_X_MARGIN, BOX_X_MARGIN, BOX_Y_MARGIN)

        orbit_box.set_planet_radius(planet_radius * box_width)
        for moon in moons:
            orbit_box.add_moon_orbit(moon['orbit'] * box_width)

        orbit_box.render(self.svg)

    def _render_radius_box(self, moons):
        pass

    def save(self, out_file):
        self.svg.add_substitutions({
            'width': WIDTH
        })

        self.svg.save(out_file)

