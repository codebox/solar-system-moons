LINE_HEIGHT = 20
YEAR_X = 40
MARKER_X = 50
EVENT_X = 60
MARKER_RADIUS = 5

class TimelineBox:
    def __init__(self, planet_data, w, h, x_margin, y_margin):
        self.data = planet_data
        self.title = planet_data['planet']['name']
        self.w = w
        self.h = h
        self.x_margin = x_margin
        self.y_margin = y_margin

    def render(self, svg, x, y):
        svg.add_rectangle(x + self.x_margin, y + self.y_margin, self.w - 2 * self.x_margin, self.h - 2 * self.y_margin, 'planetBox')

        svg.add_line(x + self.x_margin + MARKER_X, y + self.y_margin, x + self.x_margin + MARKER_X, y + self.h - self.y_margin, 'timelineBoxLine ' + self.title)

        event_count = len(self.data['timeline'])
        text_y = (self.h - (event_count - 1) * LINE_HEIGHT) / 2

        text_x = 100
        for event in self.data['timeline']:
            svg.add_right_aligned_text(x + self.x_margin + YEAR_X, y + text_y, event['year'] or '', '')
            svg.add_text(x + self.x_margin + EVENT_X, y + text_y, event['event'], '')
            svg.add_circle(x + self.x_margin + MARKER_X, y + text_y - MARKER_RADIUS, MARKER_RADIUS, 'timelineBoxMarker ' + self.title, '')
            text_y += LINE_HEIGHT

        # timeline = {}
        # for moon in self.data['moons']:
        #     name = moon['name']
        #     year = moon['year']
        #     if year not in timeline:
        #         timeline[year] = []
        #
        #     timeline[year].append(name)
        #
        # text_x = 100
        # text_y = 20
        # for moon_name in sorted(timeline.keys()):
        #     svg.add_text(x + self.x_margin + text_x, y + self.y_margin + text_y, '{} - {}'.format(moon_name, timeline[moon_name]), '')
        #     text_y += 20