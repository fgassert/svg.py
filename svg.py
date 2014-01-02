"""
svg.py 

A simple library for generating svgs in Python

Example usage:
    
    from svg import *        
    mysvg = svg(100,100)
    mysvg.add( rect(10,10,80,80,"black",1,"red") )
    gen(svg,"mysvg.svg")


The MIT License (MIT)

Copyright (c) 2011 Francis Gassert

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import string, webbrowser, os

#######################################
def gen(svgobj, filename, open_in_browser=True):
    """Saves the svg and opens it in a web browser, overwrites existing files, autoappends extension"""
    
    tout = """<?xml version="1.0" standalone="no"?>
    <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd" >
    """
    tout = '%s%s' % (tout, svgobj.get())
    
    if filename[-4:] != ".svg":
        filename = "%s.svg" % filename
    
    f = open(filename, 'w')
    f.write(tout)
    f.close()
    
    if open_in_browser:
        url = "file://%s/%s" % (os.getcwd(), filename)
        print url
        webbrowser.open(url)

#######################################
class SvgSuper(object):
    """Superclass"""
    def __init__(self):
        self._components = []
        
    def add(self, obj):
        self._components.append(obj)
    
    def insert(self, insert, obj):
        self._components.insert(insert, obj)
        
    def get(self, indent=0):
        """call to get XML text of this object and all internal objects"""
        tabs = "\t"*indent
        if len(self._components) < 1:
            return tabs + self._getstring(1)
        else:
            getlist = [obj.get(indent+1) for obj in self._components]
            components = string.join(getlist,"\n")
            openstring = tabs + self._getstring(0)
            closestring = tabs + self._closestring()
            return "\n%s%s\n%s" % (openstring, components, closestring)
    
    def _getstring(self, close=True):
        """Define XML output of object; close determines if tag closes itself"""
        
    def _closestring(self):
        """Define objects close tag"""

class svg(SvgSuper):
    """A class for building <svg> tags"""
    def __init__(self, width='100%', height='100%', viewbox='0 0 1000 1000', preserveaspectratio='xMidYMid meet', p=''):
        super(svg, self).__init__()
        
        self.width = width
        self.height = height
        self.viewbox = viewbox
        self.preserveaspectratio = preserveaspectratio
        self.p = p
    
    def _getstring(self, close=True):
        if close:
            closestr = "/"
        else:
            closestr = ""
        return '<svg width="%s" height="%s" viewBox="%s" preserveAspectRatio="%s" %s version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"%s>' % (self.width, self.height, self.viewbox, self.preserveaspectratio, self.p, closestr)
    
    def _closestring(self):
        return '</svg>'
    
class g(SvgSuper):
    def __init__(self, p = ''):
        super(g, self).__init__()
        self.p = p

    def _getstring(self, close=True):
        if close:
            closestr = "/"
        else:
            closestr = ""
        return '<g %s %s>' % (self.p, closestr)

    def _closestring(self):
        return '</g>'

class generic(SvgSuper):
    def __init__(self, name, p=''):
        super(generic, self).__init__()
        self.name = name
        self.p = p

    def _getstring(self, close=True):
        if close:
            closestr = "/"
        else:
            closestr = ""
        return '<%s %s %s>' % (self.name, self.p, closestr)

    def _closestring(self):
        return '</%s>' % (self.name)  

class rawtext(object):
    def __init__(self, text):
        self.text = text
    
    def get(self, indent=0):
        lines = self.text.split('\n')
        tabs = "\t"*indent
        lines = [tabs + line for line in lines]
        return '\n'.join(lines)

class circle(SvgSuper):
    def __init__(self, cx, cy, r, stroke='none', strokewidth='1', fill='none', p=''):
        super(circle, self).__init__()
        self.cx = cx
        self.cy = cy
        self.r = r
        self.stroke = stroke
        self.strokewidth = strokewidth
        self.fill = fill
        self.p = p

    def _getstring(self, close=True):
        if close:
            closestr = "/"
        else:
            closestr = ""
        return '<circle cx="%s" cy="%s" r="%s" stroke="%s" stroke-width="%s" fill="%s" %s %s>' % (self.cx, self.cy, self.r, self.stroke, self.strokewidth, self.fill, self.p, closestr)

    def _closestring(self):
        return '</circle>'
        
class rect(SvgSuper):
    def __init__(self, x, y, width, height, stroke='none', strokewidth='1', fill='none', p=''):
        super(rect, self).__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.stroke = stroke
        self.strokewidth = strokewidth
        self.fill = fill
        self.p = p

    def _getstring(self, close=True):
        if close:
            closestr = "/"
        else:
            closestr = ""
        return '<rect x="%s" y="%s" width="%s" height="%s" stroke="%s" stroke-width="%s" fill="%s" %s %s>' % (self.x, self.y, self.width, self.height, self.stroke, self.strokewidth, self.fill, self.p, closestr)

    def _closestring(self):
        return '</rect>'
    
class path(SvgSuper):
    def __init__(self, d, stroke='none', strokewidth='1', fill='none', p=''):
        super(path, self).__init__()
        self.d = d
        self.stroke = stroke
        self.strokewidth = strokewidth
        self.fill = fill
        self.p = p

    def _getstring(self, close=True):
        if close:
            closestr = "/"
        else:
            closestr = ""
        return '<path d="%s" stroke="%s" stroke-width="%s" fill="%s" %s %s>' % (self.d, self.stroke, self.strokewidth, self.fill, self.p, closestr)

    def _closestring(self):
        return '</path>'

        
class line(SvgSuper):
    def __init__(self, x1, y1, x2, y2, stroke='black', strokewidth='1', p=''):
        super(line, self).__init__()
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.stroke = stroke
        self.strokewidth = strokewidth
        self.p = p

    def _getstring(self, close=True):
        if close:
            closestr = "/"
        else:
            closestr = ""
        return '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s" %s %s>' % (self.x1, self.y1, self.x2, self.y2, self.stroke, self.strokewidth, self.p, closestr)

    def _closestring(self):
        return '</line>'

class text(SvgSuper):
    def __init__(self, t, x, y, fontfamily='Arial', fontsize='10', fill='black', p=''):
        super(text, self).__init__()
        self.x = x
        self.y = y
        self.t = t
        self.fontfamily = fontfamily
        self.fontsize = fontsize
        self.fill = fill
        self.p = p

    def _getstring(self, close=True):
        if close:
            closestr = "</text>"
        else:
            closestr = ""
        return '<text x="%s" y="%s" font-family="%s" font-size="%s" fill="%s" %s>%s%s' % (self.x, self.y, self.fontfamily, self.fontsize, self.fill, self.p, self.t, closestr)

    def _closestring(self):
        return '</text>'
        
class title(SvgSuper):
    def __init__(self, t):
        super(title, self).__init__()
        self.t = t

    def _getstring(self, close=True):
        if close:
            closestr = "</title>"
        else:
            closestr = ""
        return '<title>%s%s' % (self.t, closestr)

    def _closestring(self):
        return '</title>'