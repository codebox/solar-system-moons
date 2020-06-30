HEIGHT=600
WIDTH=800
MARGIN=50
PLANET_BOX_Y_SEPARATION=20
PLANET_DISC_OVERLAP=50

class SvgWrapper:
    def __init__(self, svg):
        self.svg = svg
        self.planet_boxes = []

    def render(self, data):
        planet_count = len(data)
        box_height = (HEIGHT - 2 * MARGIN - (planet_count - 1) * PLANET_BOX_Y_SEPARATION) / planet_count
        box_width = WIDTH - 2 * MARGIN
        box_x = MARGIN

        for planet_index in range(planet_count):
            box_y = MARGIN + planet_index * (box_height + PLANET_BOX_Y_SEPARATION)
            self._add_planet_box(box_x, box_y, box_width, box_height, data[planet_index])

    def save(self, out_file):
        self.svg.add_substitutions({
            'height': HEIGHT,
            'width': WIDTH
        })

        self.svg.save(out_file)

    def _add_planet_box(self, x, y, w, h, planet):
        self.svg.add_rectangle(x, y, w, h, 'planetBox')