import math
from data_processor import build_rescale

MIN_ORBIT_SIZE_FOR_MOON_DISPLAY = 5

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

        self._render_inner(svg)
        self._render_outer(svg)
        svg.add_rectangle(self.x + self.x_margin, self.y + self.y_margin, self.w - 2 * self.x_margin, self.h - 2 * self.y_margin).with_class('planetBox')


    def _render_inner(self, svg):
        clip_path_id = self._get_inner_clip_path()
        svg.add_clip_path_rect(self.x + self.x_margin, self.y + self.y_margin, self.w - 2 * self.x_margin, self.h - 2 * self.y_margin, clip_path_id)

        max_orbit_radius = max(map(lambda m: m['orbit'], self.data['moons']))
        moon_count = len(self.data['moons'])
        max_opacity = 1 if moon_count < 40 else 0.5
        min_opacity = 0.2 if moon_count < 40 else 0
        rescale_opacity = build_rescale(0, max_orbit_radius, max_opacity, min_opacity)

        self._render_with_params(svg, clip_path_id, rescale_opacity, True)

    def _render_outer(self, svg):
        clip_path_id = self._get_outer_clip_path()
        svg.add_clip_path_rect(self.x, self.y, self.w, self.h, clip_path_id)

        max_orbit_radius = max(map(lambda m: m['orbit'], self.data['moons']))
        moon_count = len(self.data['moons'])
        max_opacity = 0.5 if moon_count < 40 else 0.4
        min_opacity = 0.1 if moon_count < 40 else 0
        rescale_opacity = build_rescale(0, max_orbit_radius, max_opacity, min_opacity)

        self._render_with_params(svg, clip_path_id, rescale_opacity, False)

    def _render_with_params(self, svg, clip_path_id, rescale_opacity, draw_moons):
        all_orbit_values = [self._calc_orbit_values(moon) for moon in self.data['moons']]

        max_orbit_radius = max(map(lambda m: m['orbit'], self.data['moons']))
        rescale_distance = build_rescale(0, max_orbit_radius, 0, min(self.w, self.h)/2 + 50)

        focus_x = self.x + self.w/2
        focus_y = self.y + self.h/2

        offset_angle = 0
        for orbit_values in all_orbit_values:
            orbit_scale = rescale_distance(orbit_values['orbit'])
            opacity = rescale_opacity(orbit_values['orbit'])

            cx = focus_x + orbit_values['dx'] * orbit_scale
            cy = focus_y
            rx = orbit_values['rx'] * orbit_scale
            ry = orbit_values['ry'] * orbit_scale
            rotation_angle = orbit_values['angle']

            svg.add_ellipse(cx, cy, rx, ry).with_rotation(focus_x, focus_y, rotation_angle).with_class('eccentricityPath ' + self.title).with_clip_path(clip_path_id).with_opacity(opacity)

            if draw_moons:
                moon_x_pre = cx + rx * math.cos(offset_angle)
                moon_y_pre = cy + ry * math.sin(offset_angle)

                moon_x = math.cos(rotation_angle) * (moon_x_pre-focus_x) - math.sin(rotation_angle) * (moon_y_pre-focus_y) + focus_x
                moon_y = math.sin(rotation_angle) * (moon_x_pre-focus_x) + math.cos(rotation_angle) * (moon_y_pre-focus_y) + focus_y

                if rx ** 2 + ry ** 2 > MIN_ORBIT_SIZE_FOR_MOON_DISPLAY:
                    svg.add_circle(moon_x, moon_y, 2).with_class('eccentricityMoon ' + self.title).with_clip_path(clip_path_id).with_opacity(opacity + 0.2)

            offset_angle += math.pi * 2 / len(all_orbit_values)

    def _calc_orbit_values(self, moon):
        ec = moon['eccentricity']

        rp_ra_ratio = (1 - ec) / (1 + ec)
        ra = 1
        rp = rp_ra_ratio
        semi_major_axis = (ra + rp) / 2

        Ω = moon['longitudeOfAscendingNode']
        ω = moon['argumentOfPeriapsis']
        i = moon['inclination']

        angle = ω * math.cos(i) + Ω

        return {
            'orbit': moon['orbit'],
            'angle': angle,
            'dx': semi_major_axis - rp,
            'rx': semi_major_axis,
            'ry': math.sqrt(semi_major_axis ** 2 - (semi_major_axis - rp) ** 2)
        }

    def _get_inner_clip_path(self):
        return 'eccentricity_clip_inner_' + self.title

    def _get_outer_clip_path(self):
        return 'eccentricity_clip_outer_' + self.title



