from data_processor import build_rescale

PLANET_DISC_SEGMENT_WIDTH=40
INNER_CLIP_PATH_ID = 'radiusBoxClipInner'
OUTER_CLIP_PATH_ID = 'radiusBoxClipOuter'
DISC_SEPARATION = 20
TEXT_CENTERING_OFFSET = 3
TEXT_TO_DISC_SEPARATION = 5


class RadiusBox:
    def __init__(self, planet_data, x, y, w, h, x_margin, y_margin):
        self.title = planet_data['planet']['name']
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.x_margin = x_margin
        self.y_margin = y_margin
        self.moons = planet_data['moons']
        self.planet_radius = planet_data['planet']['radius']

    def get_width(self):
        return self.w

    def render(self, svg):
        total_moon_diameters = sum(map(lambda m: m['radius'] * 2, self.moons))
        space_for_moons = self.h - 2 * self.y_margin - PLANET_DISC_SEGMENT_WIDTH - (1 + len(self.moons)) * DISC_SEPARATION

        rescale = build_rescale(0, 1, 0, space_for_moons / total_moon_diameters)

        svg.add_clip_path_rect(self.x + self.x_margin, self.y + self.y_margin, self.w - 2 * self.x_margin, self.h - 2 * self.y_margin, INNER_CLIP_PATH_ID)
        svg.add_clip_path_rect(self.x, self.y, self.w, self.h, OUTER_CLIP_PATH_ID)

        self._render_planet(svg, rescale)
        self._render_box_filler(svg, rescale)
        self._render_moons(svg, rescale)
        self._render_box(svg)

    def _render_planet(self, svg, rescale):
        scaled_planet_radius = rescale(self.planet_radius)
        planet_cx = self.x + self.w/2
        planet_cy = self.y + self.y_margin + PLANET_DISC_SEGMENT_WIDTH - scaled_planet_radius
        svg.add_circle(planet_cx, planet_cy, scaled_planet_radius, 'radiusBoxPlanetDisc radiusBoxPlanetDiscInner ' + self.title, INNER_CLIP_PATH_ID)
        svg.add_circle(planet_cx, planet_cy, scaled_planet_radius, 'radiusBoxPlanetDisc radiusBoxPlanetDiscOuter ' + self.title, OUTER_CLIP_PATH_ID)

    def _render_moons(self, svg, rescale):
        SPACE_NEEDED_FOR_NAME_OUTSIDE_DISC = 40
        current_y = self.y + self.y_margin + PLANET_DISC_SEGMENT_WIDTH
        cx = self.x + self.w/2
        for moon in self.moons:
            radius = max(1, rescale(moon['radius']))
            cy = current_y + DISC_SEPARATION + radius
            svg.add_circle(cx, cy, radius, 'radiusBoxMoon radiusBoxMoonInner ' + self.title, INNER_CLIP_PATH_ID)
            svg.add_circle(cx, cy, radius, 'radiusBoxMoon radiusBoxMoonOuter ' + self.title, OUTER_CLIP_PATH_ID)
            moon_radius = '{:,} km'.format(int(moon['original']['radius']))
            if self.w/2 - self.x_margin - radius > SPACE_NEEDED_FOR_NAME_OUTSIDE_DISC:
                svg.add_line_text(self.x + self.x_margin, cy + TEXT_CENTERING_OFFSET, self.x + self.w/2 - radius - TEXT_TO_DISC_SEPARATION, cy + TEXT_CENTERING_OFFSET, 'radiusBoxMoonName ' + self.title, moon['name'])
                svg.add_line_text(self.x + self.w/2 + radius + TEXT_TO_DISC_SEPARATION, cy + TEXT_CENTERING_OFFSET, self.x + self.w - self.x_margin, cy + TEXT_CENTERING_OFFSET, 'radiusBoxMoonName ' + self.title, moon_radius, 'start', '0%')
            else:
                svg.add_line_text(self.x + self.x_margin, cy + TEXT_CENTERING_OFFSET, self.x + self.w - self.x_margin, cy + TEXT_CENTERING_OFFSET, 'radiusBoxMoonName ' + self.title, '{} - {}'.format(moon['name'], moon_radius), 'middle', '50%')
            current_y = cy + radius - 2

    def _render_box(self, svg):
        svg.add_rectangle(self.x + self.x_margin, self.y + self.y_margin, self.w - 2 * self.x_margin, self.h - 2 * self.y_margin, 'radiusBox')

    def _render_box_filler(self, svg, rescale):
        scaled_planet_radius = rescale(self.planet_radius)
        planet_cx = self.x + self.w/2
        planet_cy = self.y + self.y_margin + PLANET_DISC_SEGMENT_WIDTH - scaled_planet_radius
        for i in range(int(self.h)):
            svg.add_circle(planet_cx, planet_cy, i + scaled_planet_radius, 'planetRadiusFiller ' + self.title, INNER_CLIP_PATH_ID, True)

