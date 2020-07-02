from data_processor import build_rescale

PLANET_DISC_SEGMENT_WIDTH=40
CLIP_PATH_ID = 'radiusBoxClip'
DISC_SEPARATION=20

class RadiusBox:
    def __init__(self, title, x, y, w, h, x_margin, y_margin):
        self.title = title
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.x_margin = x_margin
        self.y_margin = y_margin
        self.moons = []
        self.planet_radius = 0

    def add_moons(self, moons):
        self.moons = moons

    def set_planet_radius(self, radius):
        self.planet_radius = radius

    def render(self, svg):
        total_moon_radii = sum(map(lambda m: m['radius'], self.moons))
        space_for_moons = self.w - 2 * self.x_margin - PLANET_DISC_SEGMENT_WIDTH - (1 + len(self.moons)) * DISC_SEPARATION

        rescale = build_rescale(0, 1, 0, space_for_moons / total_moon_radii)

        svg.add_clip_path(self.x + self.x_margin, self.y + self.y_margin, self.w - 2 * self.x_margin, self.h - 2 * self.y_margin, CLIP_PATH_ID)

        self._render_planet(svg, rescale)
        self._render_moons(svg, rescale)
        self._render_names(svg)
        self._render_radius_values(svg)
        self._render_box(svg)

    def _render_planet(self, svg, rescale):
        scaled_planet_radius = rescale(self.planet_radius)
        planet_cx = self.x + self.x_margin + PLANET_DISC_SEGMENT_WIDTH - scaled_planet_radius
        planet_cy = self.y + self.y_margin + self.h / 2
        svg.add_circle(planet_cx, planet_cy, scaled_planet_radius, 'radiusBoxPlanetDisc ' + self.title, CLIP_PATH_ID)

    def _render_moons(self, svg, rescale):
        pass

    def _render_names(self, svg):
        pass

    def _render_radius_values(self, svg):
        pass

    def _render_box(self, svg):
        svg.add_rectangle(self.x + self.x_margin, self.y + self.y_margin, self.w - 2 * self.x_margin, self.h - 2 * self.y_margin, 'radiusBox')
