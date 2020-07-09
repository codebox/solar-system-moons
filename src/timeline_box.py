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
        svg.add_rectangle(x + self.x_margin, y + self.y_margin, self.w - 2 * self.x_margin, self.h - 2 * self.y_margin).with_class('planetBox')

        svg.add_line(x + self.x_margin + MARKER_X, y + self.y_margin, x + self.x_margin + MARKER_X, y + self.h - self.y_margin).with_class('timelineBoxLine ' + self.title)

        event_count = len(self.data['timeline'])
        text_y = (self.h - (event_count - 1) * LINE_HEIGHT) / 2

        for event in self.data['timeline']:
            svg.add_text(x + self.x_margin + YEAR_X, y + text_y, event['year'] or '').align_end()
            svg.add_text(x + self.x_margin + EVENT_X, y + text_y, event['event'])
            svg.add_circle(x + self.x_margin + MARKER_X, y + text_y - MARKER_RADIUS, MARKER_RADIUS).with_class('timelineBoxMarker ' + self.title)
            text_y += LINE_HEIGHT
