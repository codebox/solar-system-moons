import codecs

class Svg:
    def __init__(self):
        self.template = open('template.svg').read()
        self.styles = []
        self.content = []

    def add_circle(self, x, y, r, css_class):
        self.content.append(u'<circle cx="{}" cy="{}" r="{}" class="{}"/>'.format(x, y, r, css_class))

    def add_circle_arc(self, start_x, start_y, end_x, end_y, r, large_angle, sweep, css_class):
        self.content.append(u'<path d="M {} {} A {} {} 0 {} {} {} {}" class="{}"/>'.format(start_x, start_y, r, r, 1 if large_angle else 0, 1 if sweep else 0, end_x, end_y, css_class))

    def add_rectangle(self, x, y, w, h, css_class):
        self.content.append(u'<rect x="{}" y="{}" width="{}" height="{}" class="{}"/>'.format(x, y, w, h, css_class))

    def add_substitutions(self, substitutions):
        for key, value in substitutions.items():
            self.template = self.template.replace('%{}%'.format(key), str(value))

    def save(self, out_file):
        part1, tmp = self.template.split('%style%')
        part2, part3 = tmp.split('%substance%')

        with codecs.open(out_file, 'w', 'utf-8') as f:
            f.write(part1)
            for style in self.styles:
                f.write(style)
            f.write(part2)
            for content in self.content:
                f.write(content)
            f.write(part3)
