
class OrbitBox:
    def __init__(self, title, x, y, w, h, cx, x_margin, y_margin):
        self.title = title
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.cx = cx
        self.x_margin = x_margin
        self.y_margin = y_margin
        self.moon_orbits = []
        self.planet_radius = 0

    def add_moon_orbit(self, radius):
        self.moon_orbits.append(radius)

    def set_planet_radius(self, radius):
        self.planet_radius = radius

    def render(self, svg):
        self._render_outer(svg)
        self._render_inner(svg)
        self._render_rectangle(svg)
        self._render_planet(svg)

    def _render_outer(self, svg):
        clip_path_id = self._get_outer_clip_path()
        svg.add_clip_path(self.x, self.y, self.w, self.h, clip_path_id)

        for radius in self.moon_orbits:
            svg.add_circle(self.x + self.cx, self.y + self.h/2, radius, 'moonOrbit moonOrbitOuter ' + self.title, clip_path_id)

    def _render_inner(self, svg):
        clip_path_id = self._get_inner_clip_path()
        svg.add_clip_path(self.x + self.x_margin, self.y + self.y_margin, self.w - 2 * self.x_margin, self.h - 2 * self.y_margin, clip_path_id)

        for radius in self.moon_orbits:
            svg.add_circle(self.x + self.cx, self.y + self.h/2, radius, 'moonOrbit moonOrbitInner ' + self.title, clip_path_id)

    def _render_rectangle(self, svg):
        clip_path_id = self._get_inner_clip_path()
        for i in range(int(self.w)):
            svg.add_circle(self.x + self.cx, self.y + self.h/2, i, 'moonOrbit moonOrbitFiller ' + self.title, clip_path_id, True)

        svg.add_rectangle(self.x + self.x_margin, self.y + self.y_margin, self.w - 2 * self.x_margin, self.h - 2 * self.y_margin, 'planetBox ' + self.title)

    def _render_planet(self, svg):
        clip_path_id = self._get_inner_clip_path()
        planet_radius = max(self.planet_radius, 2)
        svg.add_circle(self.x + self.cx, self.y + self.h/2, planet_radius, 'planetDiscOuter', clip_path_id)
        svg.add_circle(self.x + self.cx, self.y + self.h/2, planet_radius - 1, 'planetDiscInner', '')

    def _get_inner_clip_path(self):
        return 'clip_inner_' + self.title

    def _get_outer_clip_path(self):
        return 'clip_outer_' + self.title
