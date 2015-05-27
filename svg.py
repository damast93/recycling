# Q'n'D SVG file drawing support

class SVG:
    
    def __init__(self, fn):
        self.fo = open(fn,'w')
        self.fo.write('<svg xmlns="http://www.w3.org/2000/svg" version="1.1">'+"\n")

    def close(self):
        self.fo.write('</svg>')
        self.fo.close()

    def writeln(self, s, *args):
        self.fo.write((s % args) + "\n")

    def circle(self, x,y, r, fill):
        self.writeln('<circle cx="%f" cy="%f" r="%f" stroke="black" fill="%s"/>', x, y, r, fill)

    def line(self, x1, y1, x2, y2, col, width):
        self.writeln('<line x1="%f" y1="%f" x2="%f" y2="%f" stroke="%s" stroke-width="%i"/>',
                     x1, y1, x2, y2, col, width)
                     
    def dashline(self, x1, y1, x2, y2, col, width):
        self.writeln('<line x1="%f" y1="%f" x2="%f" y2="%f" stroke="%s" stroke-width="%i" stroke-dasharray="2,3"/>',
                     x1, y1, x2, y2, col, width)

        