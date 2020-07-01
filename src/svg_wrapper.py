import math
from arc_box import ArcBox

HEIGHT=2500
WIDTH=1000
X_MARGIN=50
Y_MARGIN=100
BOX_Y_SEPARATION=30
BOX_X_MARGIN=30
BOX_Y_MARGIN=100

class SvgWrapper:
    def __init__(self, svg):
        self.svg = svg

    def render(self, data):
        planet_count = len(data)
        box_height = (HEIGHT - 2 * Y_MARGIN - (planet_count - 1) * BOX_Y_SEPARATION) / planet_count
        box_width = WIDTH - 2 * X_MARGIN
        box_x = X_MARGIN

        arc_boxes = []
        for planet_index in range(planet_count):
            box_y = Y_MARGIN + planet_index * (box_height + BOX_Y_SEPARATION)
            arc_box = ArcBox(data[planet_index]['planet']['name'], box_x, box_y, box_width, box_height, BOX_X_MARGIN, BOX_X_MARGIN, BOX_Y_MARGIN)

            for moon in data[planet_index]['moons']:
                arc_box.add_arc(moon['x'] * box_width)

            arc_boxes.append(arc_box)

        [arc_box.render(self.svg) for arc_box in arc_boxes]

    def save(self, out_file):
        self.svg.add_substitutions({
            'height': HEIGHT,
            'width': WIDTH
        })

        self.svg.save(out_file)

