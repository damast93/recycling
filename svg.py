# Q'n'D SVG file drawing support

class SVG:
    
    def __init__(self, fn):
        self.fo = open(fn,'w')
        self.fo.write('<svg xmlns="http://www.w3.org/2000/svg" version="1.1">'+"\n")
        #self.fo.write('<marker id="triangle" viewBox="0 0 10 10" refX="0" refY="5" markerUnits="strokeWidth" markerWidth="4" markerHeight="3" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" /></marker>')

    def close(self):
        self.fo.write('</svg>')
        self.fo.close()

    def writeln(self, s, *args):
        self.fo.write((s % args) + "\n")

    def circle(self, x,y, r, fill, stroke='black', width=1):
        self.writeln('<circle cx="%f" cy="%f" r="%f" stroke="%s" stroke-width="%f" fill="%s"/>', x, y, r, stroke, width, fill)

    def line(self, x1, y1, x2, y2, col, width):
        self.writeln('<line x1="%f" y1="%f" x2="%f" y2="%f" stroke="%s" stroke-width="%f"/>',
                     x1, y1, x2, y2, col, width)
                     
    def dashline(self, x1, y1, x2, y2, col, width):
        self.writeln('<line x1="%f" y1="%f" x2="%f" y2="%f" stroke="%s" stroke-width="%f" stroke-dasharray="2,3"/>',
                     x1, y1, x2, y2, col, width)
                     
    def rect(self, cx, cy, wx, wy, fill, stroke, width):
        self.writeln('<rect x="%f" y="%f" width="%f" height="%f" fill="%s" stroke="%s" stroke-width="%f"/>',
                     cx-wx/2, cy-wy/2, wx, wy, fill, stroke, width)
    
    def roundrect(self, cx, cy, wx, wy, fill, stroke, width):
        self.writeln('<rect x="%f" y="%f" width="%f" height="%f" fill="%s" stroke="%s" stroke-width="%f" transform="rotate(45,%f,%f)"/>',
                     cx-wx/2, cy-wy/2, wx, wy, fill, stroke, width, cx-wx/2, cy-wy/2)

    def roundsquare(self, x, y, r, fill, stroke, width):
        self.roundrect(x, y, r, r, fill, stroke, width)
                     
    def square(self, x, y, r, fill, stroke, width):
        self.rect(x, y, r, r, fill, stroke, width)

    def text(self, x, y, t, sz, col='black', width=1):
        self.writeln('<text x="%f" y="%f" fill="%s" font-size="%spx" font-weight="%f">%s</text>', x, y, col, sz, width, t)