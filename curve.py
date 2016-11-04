#   02/11/16 12:14  02/11/16 12:31
#   03/11/16 21:15  03/11/16
from Tkinter import *


# import globals #####

def linearSegment(x1, y1, x2, y2, n):
    x = [None] * (n + 1)
    y = [None] * (n + 1)
    x[0], y[0], x[n], y[n] = x1, y1, x2, y2
    for i in range(1, n):
        xp = (i * x2 + (n - i) * x1) / n
        yp = (i * y2 + (n - i) * y1) / n
        x[i] = xp
        y[i] = yp
    return x, y


class Curve:
    def __init__(self):
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        self.anchor1x = None
        self.anchor1y = None
        self.anchor2x = None
        self.anchor2y = None
        self.me = None
        self.point1 = None
        self.point2 = None
        self.anchor1L = None
        self.anchor2L = None
        self.anchor1H = None
        self.anchor2H = None
        self.locus = None
        #self.color = globals.fgColor  ##
        #self.width = globals.penWidth  ##

    def getPoint1(self):
        return self.x1, self.y1

    def getPoint2(self):
        return self.x2, self.y2

    def getAnchor1(self):
        return self.anchor1x, self.anchor1y

    def getAnchor2(self):
        return self.anchor2x, self.anchor2y

    def setPoint1(self, x, y):
        self.x1 = x
        self.y1 = y

    def setPoint2(self, x, y):
        self.x2 = x
        self.y2 = y

    def setAnchor1(self, x, y):
        self.anchor1x = x
        self.anchor1y = y

    def setAnchor2(self, x, y):
        self.anchor2x = x
        self.anchor2y = y

    def computeCurve(self):
        n = int(((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2) ** 0.5) / 2
        if (self.anchor1x == None and self.anchor1y == None and
                    self.anchor2x == None and self.anchor2y == None):
            points = linearSegment(self.x1, self.y1, self.x2, self.y2, n)
            self.locus = [None] * len(points[0]) * 2
            for i in range(len(points[0])):
                self.locus[i * 2] = points[0][i]
                self.locus[i * 2 + 1] = points[1][i]

        elif (self.anchor1x == None and self.anchor1y == None):
            sgm1 = linearSegment(self.x1, self.y1, self.anchor2x, self.anchor2y, n)
            sgm2 = linearSegment(self.anchor2x, self.anchor2y, self.x2, self.y2, n)
            x = [None] * (n + 1)
            y = [None] * (n + 1)
            x[0], y[0], x[n], y[n] = self.x1, self.y1, self.x2, self.y2
            for i in range(1, n):
                x[i] = (i * sgm2[0][i] + (n + 1 - i) * sgm1[0][i]) / (n + 1)
                y[i] = (i * sgm2[1][i] + (n + 1 - i) * sgm1[1][i]) / (n + 1)

            points = (x, y)
            self.locus = [None] * len(points[0]) * 2
            for i in range(len(points[0])):
                self.locus[i * 2] = points[0][i]
                self.locus[i * 2 + 1] = points[1][i]

        elif (self.anchor2x == None and self.anchor2y == None):
            sgm1 = linearSegment(self.x1, self.y1, self.anchor1x, self.anchor1y, n)
            sgm2 = linearSegment(self.anchor1x, self.anchor1y, self.x2, self.y2, n)
            x = [None] * (n + 1)
            y = [None] * (n + 1)
            x[0], y[0], x[n], y[n] = self.x1, self.y1, self.x2, self.y2
            for i in range(1, n):
                x[i] = (i * sgm2[0][i] + (n + 1 - i) * sgm1[0][i]) / (n + 1)
                y[i] = (i * sgm2[1][i] + (n + 1 - i) * sgm1[1][i]) / (n + 1)

            points = (x, y)
            self.locus = [None] * len(points[0]) * 2
            for i in range(len(points[0])):
                self.locus[i * 2] = points[0][i]
                self.locus[i * 2 + 1] = points[1][i]
        else:
            sgm1 = linearSegment(self.x1, self.y1, self.anchor1x, self.anchor1y, n)
            sgm2 = linearSegment(self.anchor1x, self.anchor1y, self.anchor2x, self.anchor2y, n)
            sgm3 = linearSegment(self.anchor2x, self.anchor2y, self.x2, self.y2, n)
            line1x1 = [None] * (n + 1)
            line1y1 = [None] * (n + 1)
            line1x2 = [None] * (n + 1)
            line1y2 = [None] * (n + 1)
            line2x1 = [None] * (n + 1)
            line2y1 = [None] * (n + 1)
            line2x2 = [None] * (n + 1)
            line2y2 = [None] * (n + 1)
            x = [None] * (n + 1)
            y = [None] * (n + 1)
            for i in range(1, n):
                line1x1[i] = sgm1[0][i]
                line1y1[i] = sgm1[1][i]
                line1x2[i] = sgm2[0][i]
                line1y2[i] = sgm2[1][i]
                line2x1[i] = sgm2[0][i]
                line2y1[i] = sgm2[1][i]
                line2x2[i] = sgm3[0][i]
                line2y2[i] = sgm3[1][i]
                segm4 = linearSegment(line1x1[i], line1y1[i], line2x1[i], line2y1[i], n)
                segm5 = linearSegment(line2x1[i], line2y1[i], line2x2[i], line2y2[i], n)
                line3 = linearSegment(segm4[0][i], segm4[1][i], segm5[0][i], segm5[1][i], n)
                x[i], y[i] = line3[0][i], line3[1][i]
            x[0], y[0], x[n], y[n] = self.x1, self.y1, self.x2, self.y2

            points = (x, y)
            self.locus = [None] * len(points[0]) * 2
            for i in range(len(points[0])):
                self.locus[i * 2] = points[0][i]
                self.locus[i * 2 + 1] = points[1][i]

    def drawCurve(self, c):
        self.computeCurve()
        # Potential bug
        if self.me != None:
            c.delete(self.me)

        self.me = c.create_line(self.locus, tags='curve')
        self.drawAnchor1(c)
        self.drawAnchor2(c)
        self.drawPoint1(c)
        self.drawAnchor2(c)

    def drawAnchor1(self, c):
        if self.anchor1x != None:
            c.delete(self.anchor1L)
            c.delete(self.anchor1H)
            self.anchor1L = c.create_line(self.x1, self.y1, self.anchor1x, self.anchor1y, tags='anchor_line')
            self.anchor1H = c.create_oval(self.anchor1x - 3, self.anchor1y - 3, self.anchor1x + 3, self.anchor1y + 3,
                                      fill='blue',
                                      activefill='red', tags='anchor')

    def drawAnchor2(self, c):
        if self.anchor2x != None:
            c.delete(self.anchor2H)
            c.delete(self.anchor2L)
            self.anchor2L = c.create_line(self.x2, self.y2, self.anchor2x, self.anchor2y, tags='anchor_line')
            self.anchor2H = c.create_oval(self.anchor2x - 3, self.anchor2y - 3, self.anchor2x + 3, self.anchor2y + 3,
                                          fill='blue',
                                          activefill='red', tags='anchor')

    def drawPoint1(self, c):
        if self.point1 != None:
            c.delete(self.point1)
        self.point1 = c.create_oval(self.x1 - 2, self.y1 - 2, self.x1 + 2, self.y1 + 2,
                                    fill='black',
                                    activefill='red', tags='point')

    def drawPoint2(self, c):
        if self.point2 != None:
            c.delete(self.point2)
        self.point2 = c.create_oval(self.x2 - 2, self.y2 - 2, self.x2 + 2, self.y2 + 2,
                                    fill='black',
                                    activefill='red', tags='point')

    def deleteCurve(self, c):
        c.delete(self.me)
        c.delete(self.point1)
        c.delete(self.point2)
        c.delete(self.anchor1L)
        c.delete(self.anchor1H)
        c.delete(self.anchor2L)
        c.delete(self.anchor2H)


class HelperObject:
    def __init__(self):
        self.x_point = None
        self.x_anchor = None
        self.y_point = None
        self.y_anchor = None
        self.state = 0
        self.curves = []
        self.object = None


def masterClick(x, y, helperObject, c):
    if helperObject.state == 0:
        helperObject.object = Curve()
        helperObject.curves.append(helperObject.object)
        helperObject.object.setPoint1(x, y)
        helperObject.object.drawPoint1(c)
        helperObject.state = 1

    elif helperObject.state == 2:
        if helperObject.object.x1 == x:
            helperObject.object.deleteCurve(c)
            helperObject.curves.pop()
            if helperObject.curves == []:
                helperObject.state = 0
            else:
                helperObject.state = 4
        else:
            helperObject.object.setPoint2(x, y)
            helperObject.object.drawPoint2(c)
            helperObject.curves.append(Curve())
            helperObject.x_point = x
            helperObject.y_point = y
            helperObject.state = 3



def masterRelease(x, y, helperObject, c):
    print 'released',helperObject.state
    if helperObject.state == 1:
        if helperObject.object.x1 == x and helperObject.object.y1 == y:
            helperObject.object.setAnchor1(None, None)
        else:
            helperObject.object.setAnchor1(x, y)
        helperObject.state = 2

    elif helperObject.state == 3:
        print 'finished'
        if helperObject.object.x2 == x and helperObject.object.y2 == y:
            helperObject.object.setAnchor2(None,None)
            helperObject.object.drawCurve(c)
            helperObject.x_anchor,helperObject.y_anchor = None,None
        else:
            helperObject.object.setAnchor2(helperObject.object.x2*2-x,helperObject.object.y2*2-y)
            helperObject.object.drawCurve(c)
            helperObject.x_anchor = x
            helperObject.y_anchor = y

        helperObject.object = helperObject.curves.pop()
        helperObject.curves.append(helperObject.object)
        helperObject.object.setPoint1(helperObject.x_point,helperObject.y_point)
        helperObject.object.setAnchor1(helperObject.x_anchor,helperObject.y_anchor)
        helperObject.state = 2



def masterPressedMotion(x, y, helperObject, c):
    if helperObject.state == 1:
        helperObject.object.setAnchor1(x,y)
        helperObject.object.drawAnchor1(c)

    elif helperObject.state == 3:
        helperObject.object.setAnchor2(helperObject.object.x2*2-x,helperObject.object.y2*2-y)
        helperObject.object.drawCurve(c)

def masterMotion(x, y, helperObject, c):
    if helperObject.state == 2:
        print 'moving'
        helperObject.object.setPoint2(x,y)
        helperObject.object.drawCurve(c)


def activate(c):
    helperObject = HelperObject()
    c.bind('<Button-1>', lambda e: masterClick(e.x, e.y, helperObject, c))
    c.bind('<B1-Motion>', lambda e: masterPressedMotion(e.x, e.y, helperObject, c))
    c.bind('<ButtonRelease-1>', lambda e: masterRelease(e.x, e.y, helperObject, c))
    c.bind('<Motion>',lambda e:masterMotion(e.x,e.y,helperObject,c))
    return helperObject


def deactivate(c, helperObject):
    c.unbind('<Button-1>')
    c.unbind('<B1-Motion>')
    c.unbind('<ButtonRelease-1>')
    del helperObject
