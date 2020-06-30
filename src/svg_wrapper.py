import math

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

    def _add_planet_box(self, x, y, w, h, planet_data):
        self.svg.add_rectangle(x, y, w, h, 'planetBox')

        self._add_planet_disc(x, y, h, planet_data['planet']['radius'] * WIDTH)

    def _add_planet_disc(self, x, y, h, radius):
        if 2 * radius < PLANET_DISC_OVERLAP and 2 * radius < h:
            '''
            ┌────
            │  +
            │ +++   Whole disc is visible
            │  +
            └────
            '''
            self.svg.add_circle(x + PLANET_DISC_OVERLAP - radius, y + h/2, radius, 'planetDisc')

        elif 2 * radius >= PLANET_DISC_OVERLAP and 2 * radius < h:
            '''
            ┌───
            │++
            │+++    Major segment of disc is visible
            │++
            └───
            '''
            arc_h = math.sqrt(radius * radius - (radius - (2 * radius - PLANET_DISC_OVERLAP)) ** 2)
            self.svg.add_circle_arc(x, y + h/2 - arc_h, x, y + h/2 + arc_h, radius, True, True, 'planetDisc')

        elif 2 * radius < PLANET_DISC_OVERLAP and 2 * radius >= h:
            '''
            ┌───────
            │  ++++
            │ ++++++ Top and bottom parts of disc are chopped off
            │  ++++
            └───────
            '''
            x1 = PLANET_DISC_OVERLAP - (radius - math.sqrt(radius ** 2 - (h**2)/4))
            x2 = PLANET_DISC_OVERLAP - 2 * radius + math.sqrt(radius ** 2 - (h**2)/4)
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
            assert 2 * radius >= PLANET_DISC_OVERLAP and 2 * radius >= h
            arc_x = PLANET_DISC_OVERLAP - (radius - math.sqrt(radius * radius - h * h / 4))
            self.svg.add_circle_arc(x + arc_x, y, x + arc_x, y + h, radius, False, True, 'planetDisc')

