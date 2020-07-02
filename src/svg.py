import codecs, random

class Svg:
    def __init__(self):
        self.template = open('template.svg').read()
        self.styles = []
        self.content = []

    def add_circle(self, x, y, r, css_class, clip_path, randomise_opacity=False):
        self.content.append(u'<circle cx="{}" cy="{}" r="{}" class="{}" clip-path="url(#{})" {}/>'.format(
            x, y, r, css_class, clip_path, 'style="stroke-opacity: {}"'.format(0.1 + random.random()/10) if randomise_opacity else ''
        ))

    def add_rectangle(self, x, y, w, h, css_class):
        self.content.append(u'<rect x="{}" y="{}" width="{}" height="{}" class="{}"/>'.format(x, y, w, h, css_class))

    def add_clip_path(self, x, y, w, h, id):
        self.content.append(u'<clipPath id="{}"><rect x="{}" y="{}" width="{}" height="{}"/></clipPath>'.format(id, x, y, w, h))

    def add_text(self, y, text):
        self.content.append(u'<text x="50%" y="{}" text-anchor="middle" class="boxTitle">{}</text>'.format(y, text))

    def add_substitutions(self, substitutions):
        for key, value in substitutions.items():
            self.template = self.template.replace('%{}%'.format(key), str(value))

    def save(self, out_file):
        part1, tmp = self.template.split('%style%')
        part2, part3 = tmp.split('%substance%')

        with codecs.open(out_file, 'w', 'utf-8') as f:
            f.write(part1)
            for style in self.styles:
                f.write(style + '\n')
            f.write(part2)
            for content in self.content:
                f.write(content + '\n')
            f.write(part3)
