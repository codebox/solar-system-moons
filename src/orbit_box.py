import math

class OrbitBox:
    def __init__(self, planet_data, w, h, x_margin, y_margin):
        self.title = planet_data['planet']['name']
        self.x = 0
        self.y = 0
        self.cy = 0
        self.w = w
        self.h = h
        self.x_margin = x_margin
        self.y_margin = y_margin
        self.moons = planet_data['moons']
        self.planet_radius = planet_data['planet']['radius'] * self.w

    def _scale_radius(self, radius):
        return radius * (self.h - 2 * self.y_margin)

    def render(self, svg, x, y, cy):
        self.x = x
        self.y = y
        self.cy = cy
        self._render_outer(svg)
        self._render_inner(svg)
        self._render_rectangle(svg)
        self._render_planet(svg)
        self._render_labels(svg)

    def _render_outer(self, svg):
        clip_path_id = self._get_outer_clip_path()
        svg.add_clip_path_rect(self.x, self.y, self.w, self.h, clip_path_id)

        for moon in self.moons:
            svg.add_circle(self.x + self.w/2, self.y + self.cy, self._scale_radius(moon['orbit']), 'moonOrbit moonOrbitOuter ' + self.title, clip_path_id)

    def _render_inner(self, svg):
        clip_path_id = self._get_inner_clip_path()
        svg.add_clip_path_rect(self.x + self.x_margin, self.y + self.y_margin, self.w - 2 * self.x_margin, self.h - 2 * self.y_margin, clip_path_id)

        for moon in self.moons:
            svg.add_circle(self.x + self.w/2, self.y + self.cy, self._scale_radius(moon['orbit']), 'moonOrbit moonOrbitInner ' + self.title, clip_path_id)

    def _render_rectangle(self, svg):
        clip_path_id = self._get_inner_clip_path()
        for i in range(int(self.h)):
            svg.add_circle(self.x + self.w/2, self.y + self.cy, i, 'moonOrbit moonOrbitFiller ' + self.title, clip_path_id, True)

        svg.add_rectangle(self.x + self.x_margin, self.y + self.y_margin, self.w - 2 * self.x_margin, self.h - 2 * self.y_margin, 'planetBox ' + self.title)

    def _render_planet(self, svg):
        clip_path_id = self._get_inner_clip_path()
        planet_radius = max(self.planet_radius, 2)
        svg.add_circle(self.x + self.w/2, self.y + self.cy, planet_radius, 'planetDiscOuter', clip_path_id)
        svg.add_circle(self.x + self.w/2, self.y + self.cy, planet_radius - 1, 'planetDiscInner', '')

    def _get_inner_clip_path(self):
        return 'orbit_clip_inner_' + self.title

    def _get_outer_clip_path(self):
        return 'orbit_clip_outer_' + self.title

    def _render_labels(self, svg):
        MIN_SEPARATION = 15
        LABEL_ORBIT_SEPARATION = 12
        for (i, moon) in enumerate(self.moons):
            prev_r = self._scale_radius(self.moons[i-1]['orbit']) if i > 0 else 0
            this_r = self._scale_radius(self.moons[i]['orbit'])
            next_r = self._scale_radius(self.moons[i+1]['orbit']) if i < len(self.moons) - 1 else math.inf

            if next_r - this_r > MIN_SEPARATION:
                svg.add_circle_text(self.x + self.w/2, self.y + self.cy, this_r + LABEL_ORBIT_SEPARATION, 'moonOrbitLabel ' + self.title, '{}'.format(moon['name']))

