import math

DISC_SEPARATION = 50
DISC_RADIUS=30
WIDE_MOONS_PER_ROW=9
NARROW_MOONS_PER_ROW=7
BOTTOM_PADDING = 10

class RotationBox:
    def __init__(self, planet_data, x_margin, y_margin):
        self.title = planet_data['planet']['name']
        self.x = 0
        self.y = 0
        self.moons = planet_data['moons']
        self.moons_per_row = WIDE_MOONS_PER_ROW if len(self.moons) > 40 else NARROW_MOONS_PER_ROW
        self.w = 2 * x_margin + self.moons_per_row * (2 * DISC_RADIUS + DISC_SEPARATION) + DISC_SEPARATION
        self.h = 2 * y_margin + math.ceil(len(self.moons) / self.moons_per_row) * (2 * DISC_RADIUS + DISC_SEPARATION) + DISC_SEPARATION + BOTTOM_PADDING
        self.x_margin = x_margin
        self.y_margin = y_margin

    def get_height(self):
        return self.h

    def render(self, svg, x, y):
        self.x = x
        self.y = y
        self._render_rectangle(svg)
        self._render_inner(svg)

    def _render_inner(self, svg):
        init_x = self.x + self.x_margin + DISC_SEPARATION + DISC_RADIUS
        x = init_x
        y = self.y + self.y_margin + DISC_SEPARATION + DISC_RADIUS

        for (i, moon) in enumerate(self.moons):
            self._render_disc(svg, x, y, DISC_RADIUS, moon['inclination'], moon['name'])
            x += DISC_SEPARATION + 2 * DISC_RADIUS
            if (i+1) % self.moons_per_row == 0:
                x = init_x

                moons_remaining = len(self.moons) - i - 1
                if moons_remaining < self.moons_per_row:
                    x += (self.moons_per_row - moons_remaining) * (DISC_SEPARATION + 2 * DISC_RADIUS) / 2

                y += DISC_SEPARATION + 2 * DISC_RADIUS

    def _render_disc(self, svg, cx, cy, r, angle, title):
        line_length = r * 3
        line_overlap = r / 5
        ellipse_major_axis = r * 0.4

        # draw surface ellipses
        for offset in range(-r, r, 1):
            major_axis = math.sqrt(r * r - offset * offset)
            minor_axis = major_axis * line_overlap / r
            ellipse_cx = cx + math.sin(angle) * offset
            ellipse_cy = cy - math.cos(angle) * offset
            svg.add_ellipse(ellipse_cx, ellipse_cy, major_axis, minor_axis)\
                .with_rotation(ellipse_cx, ellipse_cy, angle)\
                .with_class('rotationAxisEquator' if int(offset) == 0 else 'rotationAxisLatitude')\
                .with_random_lightness(int(offset) != 0)

        # draw equatorial arrow head
        x_head = cx - line_overlap * math.sin(angle)
        y_head = cy + line_overlap * math.cos(angle)
        arrow_line_length = r/4
        arrow_line_angle = math.pi/6
        x2_upper = x_head + arrow_line_length * math.cos(angle + arrow_line_angle)
        y2_upper = y_head + arrow_line_length * math.sin(angle + arrow_line_angle)
        x2_lower = x_head + arrow_line_length * math.cos(angle - arrow_line_angle)
        y2_lower = y_head + arrow_line_length * math.sin(angle - arrow_line_angle)
        svg.add_line(x_head, y_head, x2_upper, y2_upper).with_class('rotationArrowHead')
        svg.add_line(x_head, y_head, x2_lower, y2_lower).with_class('rotationArrowHead')

        # draw upper polar line
        svg.add_line(
            cx + math.sin(angle) * line_length / 2,
            cy - math.cos(angle) * line_length / 2,
            cx + math.sin(angle) * (r - line_overlap/2),
            cy - math.cos(angle) * (r - line_overlap/2)
        ).with_class('rotationAxisLineTop ' + self.title)

        # draw lower polar line
        svg.add_line(
            cx - math.sin(angle) * r,
            cy + math.cos(angle) * r,
            cx - math.sin(angle) * line_length / 2,
            cy + math.cos(angle) * line_length / 2
        ).with_class('rotationAxisLineBottom ' + self.title)

        # draw outer circle
        svg.add_circle(cx, cy, r).with_class('rotationDisc ' + self.title)

        svg.add_circle_text(cx, cy, r + 30, title).with_class('rotationDiscText').with_angle(3 * math.pi / 2, math.pi/2).align_middle()

    def _render_rectangle(self, svg):
        svg.add_rectangle(self.x + self.x_margin, self.y + self.y_margin, self.w - 2 * self.x_margin, self.h - 2 * self.y_margin).with_class('planetBox ' + self.title)

    def _get_inner_clip_path(self):
        return 'rotation_clip_inner_' + self.title

    def _get_outer_clip_path(self):
        return 'rotation_clip_outer_' + self.title

