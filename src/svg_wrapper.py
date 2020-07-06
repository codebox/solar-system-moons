from orbit_box import OrbitBox
from radius_box import RadiusBox
from rotation_box import RotationBox
from ring_box import RingBox
from info_box import InfoBox

WIDE_MARGIN = 50
NARROW_MARGIN = 30

WIDE_BORDER = 25
NARROW_BORDER = 15
OUTER_BOX_WIDTH = 400
LONG_CONTENT_HEIGHT = 2500
SHORT_CONTENT_HEIGHT = 1500
MIN_RING_BOX_HEIGHT = 800
LOTS_OF_MOONS_THRESHOLD = 40
TEXT_LINE_CENTER_OFFSET = 5

class SvgWrapper:
    def __init__(self, svg, data):
        self.svg = svg
        self.data = data
        self.content_width = 0

        self.lots_of_moons = len(data['moons']) > LOTS_OF_MOONS_THRESHOLD
        self.content_height = LONG_CONTENT_HEIGHT if self.lots_of_moons else SHORT_CONTENT_HEIGHT
        self.margin = WIDE_MARGIN if self.lots_of_moons else NARROW_MARGIN
        self.border_thickness = WIDE_BORDER if self.lots_of_moons else NARROW_BORDER
        self.content_x = 2 * self.margin + self.border_thickness
        self.content_y = 2 * self.margin + self.border_thickness
        self.orbit_box = self._build_orbit_box()
        self.rotation_box = self._build_rotation_box()
        self.ring_box = self._build_ring_box()
        self.radius_box = self._build_radius_box()
        self.info_box = self._build_info_box()

    def render(self):
        self._render_border()
        self._render_title()

        self.orbit_box.render(self.svg, self.content_x, self.content_y, self.margin)

        self.ring_box.render(self.svg, self.content_x + self.orbit_box.w, self.content_y + self.content_height - self.rotation_box.h - self.ring_box.h)
        self.rotation_box.render(self.svg, self.content_x + self.orbit_box.w, self.content_y + self.content_height - self.rotation_box.h)
        self.info_box.render(self.svg, self.content_x + self.orbit_box.w, self.content_y)

        self.radius_box.render(self.svg, self.rotation_box.x + self.rotation_box.w, self.content_y)

        self._render_footer()

    def _render_title(self):
        self.svg.add_text(self.margin + self.border_thickness + 2 * self.margin, 'The Moons of {}'.format(self.data['planet']['name']), 'boxTitle' + ('Large' if self.lots_of_moons else 'Small'))

    def _build_orbit_box(self):
        box_width = OUTER_BOX_WIDTH
        box_height = self.content_height

        orbit_box = OrbitBox(self.data, box_width, box_height, self.margin, self.margin)

        return orbit_box

    def _build_ring_box(self):
        box_width = self.rotation_box.w
        box_height = max(self.rotation_box.h, MIN_RING_BOX_HEIGHT)

        ring_box = RingBox(self.data, box_width, box_height, self.margin, self.margin)

        return ring_box

    def _build_info_box(self):
        box_width = self.rotation_box.w
        box_height = self.content_height - self.ring_box.h - self.rotation_box.h

        info_box = InfoBox(self.data, box_width, box_height, self.margin, self.margin)

        return info_box

    def _build_rotation_box(self):
        rotation_box = RotationBox(self.data, self.margin, self.margin)

        return rotation_box

    def _build_radius_box(self):
        box_width = OUTER_BOX_WIDTH
        box_height = self.content_height

        radius_box = RadiusBox(self.data, box_width, box_height, self.margin, self.margin)

        return radius_box

    def save(self, out_file):
        self.svg.add_substitutions({
            'width': self.content_width + 2 * (self.margin + self.border_thickness),
            'height': self.content_height + 2 * (self.margin + self.border_thickness + self.margin)
        })

        self.svg.save(out_file)

    def _render_border(self):
        planet_name = self.data['planet']['name']
        self.content_width = self.orbit_box.w + self.margin + self.rotation_box.w + self.margin + self.radius_box.w
        self.svg.add_rectangle(self.margin, self.margin, self.content_width + 2 * self.border_thickness, self.content_height + 2 * (self.border_thickness + self.margin), 'borderOuter ' + planet_name)
        self.svg.add_rectangle(self.margin + self.border_thickness, self.margin + self.border_thickness, self.content_width, self.content_height + 2 * self.margin, 'borderInner')

    def _render_footer(self):
        self.svg.add_text(self.content_y + self.content_height + TEXT_LINE_CENTER_OFFSET, 'https://codebox.net/gas-giants', 'footerText' )


