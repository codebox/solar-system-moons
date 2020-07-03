from orbit_box import OrbitBox
from radius_box import RadiusBox

WIDTH=2000
Y_MARGIN=50
X_MARGIN=50
TITLE_Y=70
ORBIT_BOX_Y=100
ORBIT_BOX_HEIGHT=400
RADIUS_BOX_Y=550
RADIUS_BOX_HEIGHT=400
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

        self._render_title('The Moons of {}'.format(planet_name))
        self._render_orbit_box(planet_name, planet_radius, moons)
        self._render_radius_box(planet_name, planet_radius, data['moons'])

    def _render_title(self, planet_name):
        self.svg.add_text(TITLE_Y, planet_name)

    def _render_orbit_box(self, planet_name, planet_radius, moons):
        box_x = X_MARGIN
        box_y = ORBIT_BOX_Y
        box_width = WIDTH - 2 * X_MARGIN
        box_height = ORBIT_BOX_HEIGHT

        orbit_box = OrbitBox(planet_name, box_x, box_y, box_width, box_height, BOX_X_MARGIN, BOX_X_MARGIN, BOX_Y_MARGIN)

        orbit_box.set_planet_radius(planet_radius)
        orbit_box.add_moons(moons)

        orbit_box.render(self.svg)

    def _render_radius_box(self, planet_name, planet_radius, moons):
        box_x = X_MARGIN
        box_y = RADIUS_BOX_Y
        box_width = WIDTH - 2 * X_MARGIN
        box_height = RADIUS_BOX_HEIGHT

        radius_box = RadiusBox(planet_name, box_x, box_y, box_width, box_height, BOX_X_MARGIN, BOX_Y_MARGIN)
        radius_box.set_planet_radius(planet_radius)
        radius_box.add_moons(moons)

        radius_box.render(self.svg)

    def save(self, out_file):
        self.svg.add_substitutions({
            'width': WIDTH,
            'height': RADIUS_BOX_Y + RADIUS_BOX_HEIGHT + Y_MARGIN
        })

        self.svg.save(out_file)
