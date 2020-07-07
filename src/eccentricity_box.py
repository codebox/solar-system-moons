import math
from data_processor import build_rescale

MAX_RADIUS = 200

class EccentricityBox:
    def __init__(self, planet_data, w, h, x_margin, y_margin):
        self.title = planet_data['planet']['name']
        self.data = planet_data
        self.w = w
        self.h = h
        self.x_margin = x_margin
        self.y_margin = y_margin

    def render(self, svg, x, y):
        self.x = x
        self.y = y
        svg.add_rectangle(x + self.x_margin, y + self.y_margin, self.w - 2 * self.x_margin, self.h - 2 * self.y_margin, 'planetBox')

        all_orbit_values = [self._calc_orbit_values(moon) for moon in self.data['moons']]

        max_orbit_radius = max(map(lambda m: m['orbit'], self.data['moons']))
        rescale = build_rescale(0, max_orbit_radius, 0, MAX_RADIUS)

        cx = self.x + self.w/2
        cy = self.y + self.h/2
        angle = 0
        for orbit_values in all_orbit_values:
            orbit_scale = rescale(orbit_values['orbit'])
            svg.add_ellipse(cx + orbit_values['dx'] * orbit_scale, cy, orbit_values['rx'] * orbit_scale, orbit_values['ry'] * orbit_scale, orbit_values['angle'], 'eccentricityPath ' + self.title, False, cx, cy)

    # def _draw_orbit_shape(self, svg, name, ec, f_cx, f_cy, angle):
    #     rp_ra_ratio = (1 - ec) / (1 + ec)
    #
    #     ra = MAX_RADIUS
    #     rp = rp_ra_ratio * ra
    #
    #     radius_max = (ra + rp) / 2
    #     radius_min = math.sqrt(radius_max ** 2 - (radius_max - rp) ** 2)
    #
    #     cx = f_cx - radius_max + rp
    #     cy = f_cy
    #
    #     svg.add_ellipse(cx, cy, radius_max, radius_min, angle, 'eccentricityPath ' + self.title)
    #     svg.add_circle(f_cx, f_cy, 5, '', '')

    def _calc_orbit_values(self, moon):
        ec = moon['eccentricity']

        rp_ra_ratio = (1 - ec) / (1 + ec)
        ra = 1
        rp = rp_ra_ratio
        semi_major_axis = (ra + rp) / 2

        Ω = moon['longitudeOfAscendingNode']
        ω = moon['argumentOfPeriapsis']
        i = moon['inclination']

        # angle = math.atan(math.tan(ω - Ω) * math.cos(i)) + Ω
        angle = ω * math.cos(i) + Ω
        cos_i = 1#abs(math.cos(i))
        print(moon['name'],(angle * 180/math.pi) % 360)
        return {
            'orbit': moon['orbit'],
            'angle': angle,
            'dx': cos_i * (semi_major_axis - rp),
            'rx': cos_i * semi_major_axis,
            'ry': cos_i * math.sqrt(semi_major_axis ** 2 - (semi_major_axis - rp) ** 2)
        }



