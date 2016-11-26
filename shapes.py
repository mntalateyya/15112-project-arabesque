#   shapes module
#   Code designed by: Mohammed Nurul Hoque (andrewID: mnurulho)
#
#   15-112: Principles of Programming and Computer Science at Carnegie Mellon University in Qatar
#   Term Project
#
#   File created on: Sunday 13 of November 2016, 09:04 PM
#   Modification History
#   Start:          End:
#   15/11/16 19:05  15/11/16 19:15
#   15/11/16 09:55  15/11/16 10:00
#   22/11/16 22:12  22/11/16 22:20

from PIL import ImageDraw

# This module draws squares or ellipses on a Tkinter canvas based on mouse events


# a helper class to facilitate data communication between objects
class HelperObject:
    def __init__(self,shape):
        # initialize variables
        self.x1, self.x2, self.y1, self.y2 = [None] * 4
        self.shape=shape
        self.draw = None

    # clear canvas
    def clear(self, c):
        c.delete(self.draw)

# when mouse pressed first point initialized
def press(helper, meta,e):
    helper.x1, helper.y1 = e.x,e.y


# when mouse moved second point updated and canvas drawing updated
def move(helper, meta,e):
    helper.x2,helper.y2 = e.x,e.y
    meta.canvas.delete(helper.draw)

    # choose rectangle or oval (oval=0, rectangle = 1)
    if helper.shape:
        helper.draw = meta.canvas.create_oval(helper.x1,helper.y1,helper.x2,helper.y2,
                                              outline=meta.get_color(),width=meta.get_width())
    else:
        helper.draw = meta.canvas.create_rectangle(helper.x1,helper.y1,helper.x2,helper.y2,
                                                   outline=meta.get_color(),width=meta.get_width())

# when mouse released, shape drawn to canvas image
def release(helper, meta):
    if helper.x1 and helper.x2 and helper.y1 and helper.y2:
        # correct second point before first point
        if helper.x1>helper.x2: helper.x1,helper.x2 = helper.x2,helper.x1
        if helper.y1>helper.y2: helper.y1,helper.y2 = helper.y2,helper.y1

        image = meta.get_image()  # get canvas image
        Draw = ImageDraw.Draw(image)
        w = meta.get_width()
        if helper.shape:
            for i in range(w):
                Draw.ellipse((helper.x1+i-w/2,helper.y1+i-w/2,helper.x2-i+w/2,helper.y2-i+w/2),
                             outline=meta.get_color())
        else:
            for i in range(w):
                Draw.rectangle((helper.x1+i-w/2,helper.y1+i-w/2,helper.x2-i+w/2,helper.y2-i+w/2),
                               outline=meta.get_color())
        meta.draw(image)  # push image to canvas
        helper.clear(meta.canvas) # clear the canvas drawing


def activate(meta,shape):
    # create helper object and bind canvas events to tools
    helper = HelperObject(shape)
    meta.canvas.bind('<Button-1>', lambda e: press(helper, meta,e))
    meta.canvas.bind('<ButtonRelease-1>', lambda e: release(helper, meta))
    meta.canvas.bind('<B1-Motion>', lambda e: move(helper, meta,e))
    return helper