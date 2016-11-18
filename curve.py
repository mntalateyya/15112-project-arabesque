#   curve module
#   Code designed by: Mohammed Nurul Hoque (andrewID: mnurulho)
#
#   15-112: Principles of Programming and Computer Science at Carnegie Mellon University in Qatar
#   Term Project
#
#   File created on: Wednesday 2nd of November 2016, 12:14 PM
#   Modification History
#   Start:          End:
#   02/11/16 12:14  02/11/16 12:31
#   03/11/16 21:15  03/11/16 10:40
#   04/11/16 10:00  04/11/16 10:35
#   04/11/16 12:05  04/11/16 14:30
#   04/11/16 18:45  04/11/16 21:30
#   05/11/16 15:30  05/11/16 21:45
#   07/11/16 14:30  07/11/16 15:00
#   07/11/16 15:20  07/11/16 16:00
#   07/11/16 16:20  07/11/16 17:40
#   07/11/16 19:40  07/11/16 20:25
#   08/11/16 17:55  08/11/16 18:14
#   08/11/16 19:31  08/11/16 20:14
#   08
''' This module draws bezier curves on a Tkinter canvas. It is activated by calling activate function and deactivated
 calling deactivate function. When active, it binds mouse motion and left mouse button to its functions.'''


from PIL import ImageDraw



# given a line and number of segments, returns coordinates of points of segmenting the line n segments
# as a list of x and a list of y
def linearSegment(x1, y1, x2, y2, n):
    x = [None] * (n + 1)
    y = [None] * (n + 1)
    x[0], y[0], x[n], y[n] = x1, y1, x2, y2 # 1st and last are given endpoints
    for i in range(1, n):
        # line segmentation formula
        x[i] = (i * x2 + (n - i) * x1) / float(n)
        y[i] = (i * y2 + (n - i) * y1) / float(n)
    return x, y

# This class creates objects that encapsulate one segment of a bezier curve with 2 end points and at most 2 anchors
class Curve:
    def __init__(self):
        # endpoints coordinates
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        # anchors coordinates
        self.anchor1x = None
        self.anchor1y = None
        self.anchor2x = None
        self.anchor2y = None
        # canvas items IDs
        self.me = None # curve path
        self.point1 = None # point1 marker
        self.point2 = None # point2 marker
        self.anchor1L = None # anchor1 line
        self.anchor2L = None # anchor2 line
        self.anchor1H = None # anchor1 marker
        self.anchor2H = None # anchor2 marker

        # locus of curve points
        self.locus = None
        # self.color = globals.fgColor
        # self.width = globals.penWidth

    # coordinates setters

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

    # calculates the locus of points of curve, saves a list [x1,y1,x2,y2,...,xn,yn] to self.locus
    def computeCurve(self):
        # The number of steps to draw the curve
        n = int(((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2) ** 0.5) / 2

        #if no anchors, straight line
        if (self.anchor1x is None and self.anchor1y is None and
                    self.anchor2x is None and self.anchor2y is None):
            self.locus = [self.x1,self.y1,self.x2,self.y2]

        # if only 1 anchor, quadratic bezier curve
        elif (self.anchor1x is None and self.anchor1y is None):
            sgm1 = linearSegment(self.x1, self.y1, self.anchor2x, self.anchor2y, n)
            sgm2 = linearSegment(self.anchor2x, self.anchor2y, self.x2, self.y2, n)
            x = [None] * (n + 1)
            y = [None] * (n + 1)
            x[0], y[0], x[n], y[n] = self.x1, self.y1, self.x2, self.y2
            for i in range(1, n):
                x[i] = (i * sgm2[0][i] + (n + 1 - i) * sgm1[0][i]) / float(n + 1)
                y[i] = (i * sgm2[1][i] + (n + 1 - i) * sgm1[1][i]) / float(n + 1)

            points = (x, y)
            self.locus = [0] * len(points[0]) * 2
            for i in range(len(points[0])):
                self.locus[i * 2] = int(points[0][i])
                self.locus[i * 2 + 1] = int(points[1][i])

        elif (self.anchor2x is None and self.anchor2y is None):
            sgm1 = linearSegment(self.x1, self.y1, self.anchor1x, self.anchor1y, n)
            sgm2 = linearSegment(self.anchor1x, self.anchor1y, self.x2, self.y2, n)
            x = [None] * (n + 1)
            y = [None] * (n + 1)
            x[0], y[0], x[n], y[n] = self.x1, self.y1, self.x2, self.y2
            for i in range(1, n):
                x[i] = (i * sgm2[0][i] + (n + 1 - i) * sgm1[0][i]) / float(n + 1)
                y[i] = (i * sgm2[1][i] + (n + 1 - i) * sgm1[1][i]) / float(n + 1)

            points = (x, y)
            self.locus = [0] * len(points[0]) * 2
            for i in range(len(points[0])):
                self.locus[i * 2] = int(points[0][i])
                self.locus[i * 2 + 1] = int(points[1][i])

        # if 2 anchors cubic bezier curve
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
            self.locus = [0] * len(points[0]) * 2
            for i in range(len(points[0])):
                self.locus[i * 2] = int(points[0][i])
                self.locus[i * 2 + 1] = int(points[1][i])

    # takes a Tkinter canvas instance and draws the curve on it
    def drawCurve(self,meta):
        # compute locus of points
        self.computeCurve()
        meta.canvas.delete(self.me) # delete previous drawing
        self.me = meta.canvas.create_line(self.locus, tags='curve', fill=meta.get_color(), width= meta.get_width()) # curve path
        self.drawAnchor1(meta) # anchors
        self.drawAnchor2(meta)


    # draws the first anchor line of the curve
    def drawAnchor1(self, meta):
        if self.anchor1x != None:
            meta.canvas.delete(self.anchor1L)
            meta.canvas.delete(self.anchor1H)
            self.anchor1L = meta.canvas.create_line(self.x1, self.y1, self.anchor1x, self.anchor1y, tags='anchor_line',
                                          fill='#ff00ff')
            self.anchor1H = meta.canvas.create_oval(self.anchor1x - 3, self.anchor1y - 3, self.anchor1x + 3, self.anchor1y + 3,
                                  fill='blue', activefill='red', tags='anchor')
    # draws the second anchor line of the curve
    def drawAnchor2(self, meta):
        if self.anchor2x is not None:
            meta.canvas.delete(self.anchor2H)
            meta.canvas.delete(self.anchor2L)
            self.anchor2L = meta.canvas.create_line(self.x2, self.y2, self.anchor2x, self.anchor2y, tags='anchor_line',
                                          fill='#ff00ff')
            self.anchor2H = meta.canvas.create_oval(self.anchor2x - 3, self.anchor2y - 3, self.anchor2x + 3, self.anchor2y + 3,
                                      fill='blue',activefill='red', tags='anchor')

    # draws the first point marker
    def drawPoint1(self, meta):
        if self.point1 is not None:
            meta.canvas.delete(self.point1)
        self.point1 = meta.canvas.create_oval(self.x1 - 3, self.y1 - 3, self.x1 + 3, self.y1 + 3,
                                    fill='black', activefill='green', tags='point')
        return self.point1

    # draws the second point marker
    def drawPoint2(self, meta):
        if self.point2 is not None:
            meta.canvas.delete(self.point2)
        self.point2 = meta.canvas.create_oval(self.x2 - 3, self.y2 - 3, self.x2 + 3, self.y2 + 3,
                                    fill='black', activefill='green', tags='point')
        return self.point2

    # deletes the curve's drawing on canvas
    def deleteCurve(self, canvas):
        canvas.delete(self.me)
        canvas.delete(self.point2)
        canvas.delete(self.anchor1L)
        canvas.delete(self.anchor1H)
        canvas.delete(self.anchor2L)
        canvas.delete(self.anchor2H)

# a helper class that facilitates the interaction between objects and and the events
class HelperObject:
    def __init__(self):
        self.x_point = None
        self.x_anchor = None
        self.y_point = None
        self.y_anchor = None
        self.point_mark = None
        self.state = 0
        self.curves = []
        self.object = None

    # deactivates curve drawing
    def clear(self,c):
        for curve in self.curves:
            curve.deleteCurve(c)

# controls click events during drawing
def masterClick(x, y, helperObject, meta):
    if helperObject.state == 0:
        helperObject.object = Curve()
        helperObject.curves.append(helperObject.object)
        helperObject.object.setPoint1(x, y)
        helperObject.object.drawPoint1(meta)
        helperObject.state = 1

    elif helperObject.state == 2:
        if helperObject.object.x1 == x:
            helperObject.object.deleteCurve(meta.canvas)
            helperObject.curves.pop()
            if not helperObject.curves:
                helperObject.state = 0
            else:
                helperObject.state = 4
        else:

            helperObject.object.setPoint2(x, y)
            helperObject.object.drawPoint2(meta)
            helperObject.curves.append(Curve())
            helperObject.x_point = x
            helperObject.y_point = y
            helperObject.point_mark = helperObject.object.point2
            helperObject.state = 3
    elif helperObject.state == 4 or helperObject.state == 5:
        if not(meta.canvas.find_enclosed(x-8,y-8,x+8,y+8)):
            restart(helperObject,meta)
            helperObject.state=0

# controls button release event during drawing
def masterRelease(x, y, helperObject, meta):
    if helperObject.state == 1:
        if helperObject.object.x1 == x and helperObject.object.y1 == y:
            helperObject.object.setAnchor1(None, None)
        else:
            helperObject.object.setAnchor1(x, y)
        helperObject.state = 2

    elif helperObject.state == 3:
        if helperObject.object.x2 == x and helperObject.object.y2 == y:
            helperObject.object.x1,helperObject.object.x2
            helperObject.object.setAnchor2(None,None)
            helperObject.object.drawCurve(meta)
            helperObject.x_anchor,helperObject.y_anchor = None,None
        else:
            helperObject.object.setAnchor2(helperObject.object.x2*2-x,helperObject.object.y2*2-y)
            helperObject.object.drawCurve(meta)
            helperObject.x_anchor = x
            helperObject.y_anchor = y

        helperObject.object = helperObject.curves.pop()
        helperObject.curves.append(helperObject.object)
        helperObject.object.setPoint1(helperObject.x_point,helperObject.y_point)
        helperObject.object.setAnchor1(helperObject.x_anchor,helperObject.y_anchor)
        helperObject.object.point1 = helperObject.point_mark
        helperObject.state = 2


# controls mouse presses-motion event during drawing
def masterPressedMotion(x, y, helperObject, meta):
    if helperObject.state == 1 and abs(helperObject.object.x1-x)>1 and abs(helperObject.object.y1-y)>1:
        helperObject.object.setAnchor1(x,y)
        helperObject.object.drawAnchor1(meta)

    elif helperObject.state == 3 and abs(helperObject.object.x2-x)>1 and abs(helperObject.object.y2-y)>1:
        helperObject.object.setAnchor2(helperObject.object.x2*2-x,helperObject.object.y2*2-y)
        helperObject.object.drawCurve(meta)

# controls mouse motion event during drawing
def masterMotion(x, y, helperObject, meta):
    if helperObject.state == 2 and abs(helperObject.object.x1-x)>1 and abs(helperObject.object.y1-y)>1:
        helperObject.object.setPoint2(x,y)
        helperObject.object.drawCurve(meta)
    elif helperObject.state == 4:
        for i in meta.canvas.find_withtag('anchor'):
            meta.canvas.tag_bind(i,'<Button-1>',lambda e, id=i: bindAnchor(id,helperObject,meta))
        for i in meta.canvas.find_withtag('point'):
            meta.canvas.tag_bind(i,'<Button-1>',lambda e, id=i: bindPoint(id,helperObject,meta))
            meta.canvas.tag_raise(i)
        helperObject.state = 5

# binds canvas to an anchor during drawing
def bindAnchor(id,helperObject,meta):
    meta.canvas.bind('<B1-Motion>',lambda e, i = id: moveAnchor(i,e,helperObject,meta))
    meta.canvas.bind('<ButtonRelease-1>',lambda e : unbind(helperObject,meta))

# binds canvas to a point during drawing
def bindPoint(id,helperObject,meta):
    meta.canvas.bind('<B1-Motion>', lambda e, i=id: movePoint( i,e,helperObject,meta))
    meta.canvas.bind('<ButtonRelease-1>', lambda e: unbind( helperObject,meta))

# moves anchor to mouse coordinates and redraws curve
def moveAnchor( id,e,helperObject,meta):
    for i in helperObject.curves:
        if i.anchor1H == id:
            i.setAnchor1(e.x,e.y)
            i.computeCurve()
            i.drawCurve( meta)
            meta.canvas.bind('<B1-Motion>', lambda e, id=i: moveAnchor(  id.anchor1H, e, helperObject,meta))
            return
        elif i.anchor2H == id:
            i.setAnchor2(e.x, e.y)
            i.computeCurve()
            i.drawCurve( meta)
            meta.canvas.bind('<B1-Motion>', lambda e, id=i: moveAnchor(  id.anchor2H, e, helperObject,meta))
            return
# moves point to mouse coordinates and redraws curves
def movePoint( id,e,helperObject,meta):
    ref = None
    for i in helperObject.curves:
        if i.point2 == id:
            deltax = e.x - i.x2
            deltay = e.y - i.y2
            i.setPoint2(e.x,e.y)
            if i.anchor2x is not None:
                i.setAnchor2(i.anchor2x+deltax,i.anchor2y+deltay)
            i.drawCurve( meta)
            ref = i.drawPoint2(meta)
            meta.canvas.bind('<B1-Motion>', lambda e, id=i: movePoint(  id.point2, e, helperObject,meta))
            meta.canvas.lift(i.point2)
        elif i.point1 == id:
            deltax = e.x - i.x1
            deltay = e.y - i.y1
            i.setPoint1(e.x, e.y)
            if i.anchor1x is not None:
                i.setAnchor1(i.anchor1x+deltax,i.anchor1y+deltay)
            i.drawCurve( meta)
            if ref is not None:
                i.point1 = ref
            else:
                i.drawPoint1(meta)
            meta.canvas.bind('<B1-Motion>', lambda e, id=i: movePoint(  id.point1, e, helperObject,meta))
            meta.canvas.lift(i.point1)

# unbinds canvas from items when mouse released
def unbind( helperObject,meta):
    meta.canvas.unbind('<B1-Motion>')
    for i in meta.canvas.find_withtag('anchor'):
        meta.canvas.tag_bind(i, '<Button-1>', lambda e, id=i: bindAnchor(  id, helperObject,meta))
    for i in meta.canvas.find_withtag('point'):
        meta.canvas.tag_bind(i, '<Button-1>', lambda e, id=i: bindPoint(  id, helperObject,meta))

# finalizes a curve and starts drawing a new curve
def restart( helperObject,meta):
    image = meta.get_image()
    draw = ImageDraw.Draw(image)
    for i in helperObject.curves:
        draw.line(i.locus,fill=meta.get_color(),width=meta.get_width())
        i.deleteCurve(meta.canvas)
    meta.draw(image)
    meta.canvas.delete(helperObject.curves[0].point1)
    helperObject.curves = []
    helperObject.x_point = None
    helperObject.x_anchor = None
    helperObject.y_point = None
    helperObject.y_anchor = None
    helperObject.point_mark = None
    helperObject.state = 0
    helperObject.curves = []
    helperObject.object = None
    meta.canvas.bind('<Button-1>', lambda e: masterClick(e.x, e.y, helperObject, meta))
    meta.canvas.bind('<B1-Motion>', lambda e: masterPressedMotion(e.x, e.y, helperObject, meta))
    meta.canvas.bind('<ButtonRelease-1>', lambda e: masterRelease(e.x, e.y, helperObject, meta))
    meta.canvas.bind('<Motion>', lambda e: masterMotion(e.x, e.y, helperObject, meta))

# activates curve drawing
def activate(meta):
    helperObject = HelperObject()
    meta.canvas.bind('<Button-1>', lambda e: masterClick(e.x, e.y, helperObject, meta))
    meta.canvas.bind('<B1-Motion>', lambda e: masterPressedMotion(e.x, e.y, helperObject, meta))
    meta.canvas.bind('<ButtonRelease-1>', lambda e: masterRelease(e.x, e.y, helperObject, meta))
    meta.canvas.bind('<Motion>',lambda e:masterMotion(e.x,e.y,helperObject,meta))
    return helperObject
