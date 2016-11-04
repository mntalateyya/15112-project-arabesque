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
        self.anchor1L = None
        self.anchor2L = None
        self.anchor1H = None
        self.anchor2H = None
        self.locus = None
        self.color = globals.fgColor  ##
        self.width = globals.penWidth  ##

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
        n = int(((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2) ** 0.5)/2
        if (self.anchor1x == None and self.anchor1y == None and
                    self.anchor2x == None and self.anchor2y == None):
            self.locus = linearSegment(self.x1, self.y1, self.x2, self.y2, n)
        elif (self.anchor1x == None and self.anchor1y == None):
            sgm1 = linearSegment(self.x1, self.y1, self.anchor2x, self.anchor2y, n)
            sgm2 = linearSegment(self.anchor2x, self.anchor2y, self.x2, self.y2, n)
            x = [None] * (n + 1)
            y = [None] * (n + 1)
            x[0], y[0], x[n], y[n] = self.x1, self.y1, self.x2, self.y2
            for i in range(1, n):
                x[i] = (i * sgm2[0][i] + (n + 1 - i) * sgm1[0][i]) / (n + 1)
                y[i] = (i * sgm2[1][i] + (n + 1 - i) * sgm1[1][i]) / (n + 1)
            self.locus = (x, y)
        elif (self.anchor2x == None and self.anchor2y == None):
            sgm1 = linearSegment(self.x1, self.y1, self.anchor1x, self.anchor1y, n)
            sgm2 = linearSegment(self.anchor1x, self.anchor1y, self.x2, self.y2, n)
            x = [None] * (n + 1)
            y = [None] * (n + 1)
            x[0], y[0], x[n], y[n] = self.x1, self.y1, self.x2, self.y2
            for i in range(1, n):
                x[i] = (i * sgm2[0][i] + (n + 1 - i) * sgm1[0][i]) / (n + 1)
                y[i] = (i * sgm2[1][i] + (n + 1 - i) * sgm1[1][i]) / (n + 1)
            self.locus = (x, y)
        else:
            sgm1 = linearSegment(self.x1, self.y1, self.anchor1x, self.anchor1y, n)
            sgm2 = linearSegment(self.anchor1x, self.anchor1y, self.anchor2x, self.anchor2y, n)
            sgm3 = linearSegment(self.anchor2x, self.anchor2y, self.x2, self.y2,n)
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
                segm4 = linearSegment(line1x1[i], line1y1[i], line2x1[i], line2y1[i],n)
                segm5 = linearSegment(line2x1[i], line2y1[i], line2x2[i], line2y2[i],n)
                line3 = linearSegment(segm4[0][i],segm4[1][i],segm5[0][i],segm5[1][i],n)
                x[i], y[i] = line3[0][i], line3[1][i]
            x[0], y[0], x[n], y[n] = self.x1, self.y1, self.x2, self.y2
            self.locus = (x, y)
            '''line1x[i] = (i * sgm2[0][i] + (n + 1 - i) * sgm1[0][i]) / (n + 1)
            line1y[i] = (i * sgm2[1][i] + (n + 1 - i) * sgm1[1][i]) / (n + 1)
            xq[0], yq[0], xq[n], yq[n] = self.x1, self.y1, self.x2, self.y2
            self.locus = (xq, yq)'''

    def drawCurve(self, c):
        # Potential bug
        c.delete(self.me)
        c.delete(self.anchor1H)
        c.delete(self.anchor1L)
        c.delete(self.anchor2H)
        c.delete(self.anchor2L)

        if (self.anchor1x == None and self.anchor1y == None and
                    self.anchor2x == None and self.anchor2y == None):
            self.drawLine(c)
        elif (self.anchor1x == None and self.anchor1y == None):
            self.drawBezierQ(c, 0)
        elif (self.anchor2x == None and self.anchor2y == None):
            self.drawBezierQ(c, 1)
        else:
            self.drawBezierC(c)

    def drawAnchor(self, c):
        self.anchor1L = self.create_line(self.x1, self.y1, self.anchor1x, self.anchor1y)
        self.anchor1H = self.create_oval(self.anchor1x - 3, self.anchor1y - 3, self.anchor1x + 3, self.anchor2y + 3,
                                         fill='blue',
                                         activefill='red')

    def drawLine(self, c):
        self.me = c.create_line(self.x1, self.y1, self.x2, self.y2)

    def drawBezierQ(self, c):
        pass

    def drawBezierC(self, c):
        pass


class HelperObject:
    def __init__(self):
        self.x1 = None
        self.x2 = None
        self.x3 = None
        self.x4 = None
        self.y1 = None
        self.y2 = None
        self.y3 = None
        self.y4 = None
        self.state = 0


def masterClick(e, x, y, helper):
    if helper.state == 0:
        pass
    elif helper.state == 2:
        pass


def masterRelease(e, x, y, helper):
    if helper.state == 1:
        pass
    elif helper.state == 3:
        pass


def masterMotion(e, x, y, helper):
    if helper.state == 1:
        pass
    elif helper.state == 3:
        pass


def avtivate(c):
    helper = HelperObject()
    c.bind('<Button-1', lambda e: masterClick(e.x, e.y, helper))
    c.bind('<B1-Motion>', lambda e: masterMotion(e.x, e.y, helper))
    c.bind('<Button-1-Release>', lambda e: masterRelease(e.x, e.y, helper))
    return helper


def deactivate(c, obj):
    c.unbind('<Button-1')
    c.unbind('<B1-Motion>')
    c.unbind('<Button-1-Release>')
    del obj
