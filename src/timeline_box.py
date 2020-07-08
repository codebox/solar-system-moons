class TimelineBox:
    def __init__(self, planet_data, w, h, x_margin, y_margin):
        self.data = planet_data
        self.w = w
        self.h = h
        self.x_margin = x_margin
        self.y_margin = y_margin

    def render(self, svg, x, y):
        svg.add_rectangle(x + self.x_margin, y + self.y_margin, self.w - 2 * self.x_margin, self.h - 2 * self.y_margin, 'planetBox')
        timeline = {}
        for moon in self.data['moons']:
            name = moon['name']
            year = moon['year']
            if year not in timeline:
                timeline[year] = []

            timeline[year].append(name)

        for moon_name in sorted(timeline.keys()):
            # print(moon_name, timeline[moon_name])
            pass