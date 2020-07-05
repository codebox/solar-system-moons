from orbit_box import OrbitBox
from radius_box import RadiusBox
from rotation_box import RotationBox
from ring_box import RingBox

OUTER_X_MARGIN = 50
OUTER_Y_MARGIN = 50
BORDER_THICKNESS = 15
INNER_X_MARGIN = 50
INNER_Y_MARGIN = 50

OUTER_BOX_WIDTH = 400
OUTER_BOX_X_MARGIN = 40
OUTER_BOX_Y_MARGIN = 80

INNER_BOX_X_MARGIN = 40
INNER_BOX_Y_MARGIN = 80

CONTENT_X = OUTER_X_MARGIN + BORDER_THICKNESS + INNER_X_MARGIN
CONTENT_Y = OUTER_Y_MARGIN + BORDER_THICKNESS + INNER_Y_MARGIN
CONTENT_HEIGHT = 1500

MOONS_PER_COLUMN_IN_CENTER = 10

TITLE_Y_OFFSET = 25


class SvgWrapper:
    def __init__(self, svg, data):
        self.svg = svg
        self.data = data
        self.content_width = 0

    def render(self):
        orbit_box = self._build_orbit_box()
        ring_box = self._build_ring_box()
        # rotation_box = self._build_rotation_box()
        radius_box = self._build_radius_box()

        self._render_border()
        self._render_title()
        orbit_box.render(self.svg)
        ring_box.render(self.svg)
        # rotation_box.render(self.svg)
        radius_box.render(self.svg)

    def _render_title(self):
        self.svg.add_text(OUTER_Y_MARGIN + BORDER_THICKNESS + INNER_Y_MARGIN + TITLE_Y_OFFSET, 'The Moons of {}'.format(self.data['planet']['name']))

    def _build_orbit_box(self):
        box_x = CONTENT_X + self.content_width
        box_y = CONTENT_Y
        box_width = OUTER_BOX_WIDTH
        box_height = CONTENT_HEIGHT

        orbit_box = OrbitBox(self.data, box_x, box_y, box_width, box_height, OUTER_BOX_Y_MARGIN, OUTER_BOX_X_MARGIN, OUTER_BOX_Y_MARGIN)
        self.content_width += orbit_box.get_width()

        return orbit_box

    def _build_ring_box(self):
        box_x = CONTENT_X + self.content_width
        box_y = CONTENT_Y
        box_width = OUTER_BOX_WIDTH * 2
        box_height = CONTENT_HEIGHT

        ring_box = RingBox(self.data, box_x, box_y, box_width, box_height, INNER_BOX_X_MARGIN, INNER_BOX_Y_MARGIN)
        self.content_width += ring_box.get_width()

        return ring_box

    def _build_rotation_box(self):
        box_x = CONTENT_X + self.content_width
        box_y = CONTENT_Y
        box_height = CONTENT_HEIGHT

        rotation_box = RotationBox(self.data, box_x, box_y, box_height, INNER_BOX_X_MARGIN, INNER_BOX_Y_MARGIN)
        self.content_width += rotation_box.get_width()

        return rotation_box

    def _build_radius_box(self):
        box_x = CONTENT_X + self.content_width
        box_y = CONTENT_Y
        box_width = OUTER_BOX_WIDTH
        box_height = CONTENT_HEIGHT

        radius_box = RadiusBox(self.data, box_x, box_y, box_width, box_height, OUTER_BOX_X_MARGIN, OUTER_BOX_Y_MARGIN)
        self.content_width += radius_box.get_width()

        return radius_box

    def save(self, out_file):
        self.svg.add_substitutions({
            'width': self.content_width + 2 * (OUTER_X_MARGIN + BORDER_THICKNESS + INNER_X_MARGIN),
            'height': CONTENT_HEIGHT + 2 * (OUTER_Y_MARGIN + BORDER_THICKNESS + INNER_Y_MARGIN)
        })

        self.svg.save(out_file)

    def _render_border(self):
        planet_name = self.data['planet']['name']
        self.svg.add_rectangle(OUTER_X_MARGIN, OUTER_Y_MARGIN, self.content_width + 2 * (BORDER_THICKNESS + INNER_X_MARGIN), CONTENT_HEIGHT + 2 * (BORDER_THICKNESS + INNER_Y_MARGIN), 'borderOuter ' + planet_name)
        self.svg.add_rectangle(OUTER_X_MARGIN + BORDER_THICKNESS, OUTER_Y_MARGIN + BORDER_THICKNESS, self.content_width + 2 * INNER_X_MARGIN, CONTENT_HEIGHT + 2 * INNER_Y_MARGIN, 'borderInner')

