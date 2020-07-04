import math

DISC_SEPARATION = 50
DISC_RADIUS=30
MOONS_PER_COLUMN=10

class RotationBox:
    def __init__(self, planet_data, x, y, h, x_margin, y_margin):
        self.title = planet_data['planet']['name']
        self.x = x
        self.y = y
        self.moons_per_row = (int(len(planet_data['moons']) / MOONS_PER_COLUMN) + 1)
        self.w = 2 * x_margin + self.moons_per_row * (2 * DISC_RADIUS + DISC_SEPARATION) + DISC_SEPARATION
        self.h = h
        self.x_margin = x_margin
        self.y_margin = y_margin
        self.moons = planet_data['moons']

    def get_width(self):
        return self.w

    def render(self, svg):
        self._render_rectangle(svg)
        self._render_inner(svg)

    def _render_inner(self, svg):
        init_x = self.x + self.x_margin + DISC_SEPARATION + DISC_RADIUS
        x = init_x
        y = self.y + self.y_margin + DISC_SEPARATION + DISC_RADIUS

        for (i, moon) in enumerate(self.moons):
            self._render_disc(svg, x, y, DISC_RADIUS, math.pi * moon['inclination'] / 180, moon['name'])
            x += DISC_SEPARATION + 2 * DISC_RADIUS
            if (i+1) % self.moons_per_row == 0:
                x = init_x
                y += DISC_SEPARATION + 2 * DISC_RADIUS

    def _render_disc(self, svg, cx, cy, r, angle, title):
        line_length = r * 3
        line_overlap = r / 5
        ellipse_major_axis = r * 0.4
        ellipse_minor_axis = ellipse_major_axis * line_overlap / r

        # draw surface ellipses
        for offset in range(-r, r, 1):
            major_axis = math.sqrt(r * r - offset * offset)
            minor_axis = major_axis * line_overlap / r
            svg.add_ellipse(
                cx + math.sin(angle) * offset,
                cy - math.cos(angle) * offset,
                major_axis,
                minor_axis,
                angle,
                'rotationAxisEquator' if int(offset) == 0 else 'rotationAxisLatitude', int(offset) != 0
            )

        # draw equatorial arrow head
        x_head = cx - line_overlap * math.sin(angle)
        y_head = cy + line_overlap * math.cos(angle)
        arrow_line_length = r/4
        arrow_line_angle = math.pi/6
        x2_upper = x_head + arrow_line_length * math.cos(angle + arrow_line_angle)
        y2_upper = y_head + arrow_line_length * math.sin(angle + arrow_line_angle)
        x2_lower = x_head + arrow_line_length * math.cos(angle - arrow_line_angle)
        y2_lower = y_head + arrow_line_length * math.sin(angle - arrow_line_angle)
        svg.add_line(x_head, y_head, x2_upper, y2_upper, 'rotationArrowHead')
        svg.add_line(x_head, y_head, x2_lower, y2_lower, 'rotationArrowHead')

        # draw upper polar line
        svg.add_line(
            cx + math.sin(angle) * line_length / 2,
            cy - math.cos(angle) * line_length / 2,
            cx + math.sin(angle) * (r - line_overlap/2),
            cy - math.cos(angle) * (r - line_overlap/2),
            'rotationAxisLineTop ' + self.title)

        # draw lower polar line
        svg.add_line(
            cx - math.sin(angle) * r,
            cy + math.cos(angle) * r,
            cx - math.sin(angle) * line_length / 2,
            cy + math.cos(angle) * line_length / 2,
            'rotationAxisLineBottom ' + self.title)

        # draw outer circle
        svg.add_circle(cx, cy, r, 'rotationDisc ' + self.title, '')

        svg.add_circle_text(cx, cy, r + 30, 'rotationDiscText', title, 3 * math.pi / 2, math.pi/2)

        # draw upper polar ellipse
        svg.add_ellipse(
            cx + math.sin(angle) * 0.9 * line_length / 2,
            cy - math.cos(angle) * 0.9 * line_length / 2,
            ellipse_major_axis, ellipse_minor_axis, angle, 'rotationAxisEllipse'
        )


    def _render_rectangle(self, svg):
        svg.add_rectangle(self.x + self.x_margin, self.y + self.y_margin, self.w - 2 * self.x_margin, self.h - 2 * self.y_margin, 'planetBox ' + self.title)

    def _get_inner_clip_path(self):
        return 'rotation_clip_inner_' + self.title

    def _get_outer_clip_path(self):
        return 'rotation_clip_outer_' + self.title

