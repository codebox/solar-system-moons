
class InfoBox:
    def __init__(self, planet_data, w, h, x_margin, y_margin):
        self.text = '' #planet_data['planet']['info']
        self.x = 0
        self.y = 0
        self.w = w
        self.h = h
        self.x_margin = x_margin
        self.y_margin = y_margin

    def get_width(self):
        return self.w

    def render(self, svg, x, y):
        self.x = x
        self.y = y
        # svg.add_rectangle(self.x + self.x_margin, self.y + self.y_margin, self.w - 2 * self.x_margin, self.h - self.y_margin, 'planetBox')
        svg.add_text(self.y + self.y_margin + self.h/2, 'here is some text', 'infoBoxText')

