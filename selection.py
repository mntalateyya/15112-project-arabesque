#   Selection module
#   Code designed by: Mohammed Nurul Hoque (andrewID: mnurulho)
#
#   15-112: Principles of Programming and Computer Science at Carnegie Mellon University in Qatar
#   Term Project
#
#   File created on: Wednesday 2nd of November 2016, 12:14 PM
#   Modification History
#   Start:          End:
#   18/11/16 21:45  18/11/16 22:30
#   23/11/16 20:20  23/11/16 20:40
#   24/11/16 13:40  24/11/16 13:55
#   26/11/16 23:12  26/11/16 23:26

# This module provides a select tool for a canvas
# it allows user to select an area and move it or delete it

from Tkinter import *
from PIL import Image,ImageTk
import DrawMeta

# a helper class to share date
class helperObject:
    def __init__(self):
        # coordinates of selection
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        # initial position of mouse when area dragged
        self.mousex = 0
        self.mousey = 0

        self.state = 0

        # references
        self.square = None
        self.image = None
        self.TkImage = None
        self.image_label = 0

    # delete canvas items
    def clear(self,c):
        self.state = 0
        c.delete(self.square)
        c.delete(self.image_label)


# when mouse clicked if state = 0: set first coordinates
# if state = 1, set mouse coordinates and get image in area
# if state one but clicked outside area remove selection and start over
def masterClick(meta, e,helper):
    # if outside
    if helper.state==1 and not(helper.x1<e.x<helper.x2 and helper.y1<e.y<helper.y2):
        meta.canvas.delete(helper.square)
        helper.state = 0
    if helper.state == 0:
        helper.x1,helper.y1 = e.x,e.y
    elif helper.state == 1:
        helper.mousex = e.x
        helper.mousey = e.y
        new_im = meta.get_image()
        # fill from_area with transparent white
        new_im.paste('#ffffff00', (helper.x1, helper.y1, helper.x2, helper.y2))
        meta.draw(new_im) # push to canvas
        helper.state = 2

# when moused moved while pressed, if state = 0, set second coordinates of area and redraw guiding square
# if state =2, calculate relative motion mouse and move the area with that amount
def masterPressedMotion(meta,e,helper):
    if helper.state == 0:
        helper.x2,helper.y2 = e.x,e.y
        meta.canvas.delete(helper.square)
        helper.square = meta.canvas.create_rectangle(helper.x1,helper.y1,helper.x2,helper.y2)
    if helper.state ==2:
        meta.canvas.delete(helper.image_label)
        meta.canvas.delete(helper.square)
        # relative motion of mouse
        deltax = e.x-helper.mousex
        deltay = e.y-helper.mousey
        # redraw canvas
        helper.TkImage = ImageTk.PhotoImage(image=helper.image)
        helper.image_label = meta.canvas.create_image(helper.x1+deltax,helper.y1+deltay,
                                                      image=helper.TkImage, anchor=NW)
        helper.square = meta.canvas.create_rectangle(helper.x1+deltax,helper.y1+deltay,
                                                     helper.x2+deltax,helper.y2+deltay)

# when mouse released, if state =0, get image in selected area
# if state =2, updste image's position and finalize area move
def masterRelease(meta, e,helper):
    # flip coordinates if in reversed order
    if helper.state == 0  and e.x!=helper.x1 and e.y!=helper.y1:
        if helper.x1 > helper.x2:
            helper.x1, helper.x2 = helper.x2, helper.x1
        if helper.y1 > helper.y2:
            helper.y1, helper.y2 = helper.y2, helper.y1

        helper.image = meta.get_image().crop((helper.x1,helper.y1,helper.x2,helper.y2))
        helper.state=1

    if helper.state ==2:
        deltax = e.x - helper.mousex
        deltay = e.y - helper.mousey
        # update image's coordinates
        helper.x1 += deltax
        helper.x2 += deltax
        helper.y1 += deltay
        helper.y2 += deltay
        finalize(meta, helper)
        helper.state = 1

# delete selected area and fill it with transparent white
def delete(helper,meta):
    if helper.state ==1:
        to_paste = Image.new('RGB', (abs(helper.x2 - helper.x1), abs(helper.y2 - helper.y1)), '#ffffff00')
        # amend meta with new image
        new_im = meta.get_image()
        new_im.paste(to_paste,(helper.x1, helper.y1, helper.x2, helper.y2))
        meta.draw(new_im)

# create image with area moved
def finalize(meta,helper):
    # paste image into meta image
    image = meta.get_image()
    image.paste(helper.image, (helper.x1, helper.y1, helper.x2, helper.y2),helper.image)
    meta.draw(image)
    # clear canvas items
    helper.clear(meta.canvas)
    helper.state = 0

# activate tool and bind canvas events to functions
def activate(meta):
    helper = helperObject()
    meta.canvas.focus_set()
    meta.canvas.bind('<Button-1>',lambda e: masterClick(meta,e,helper))
    meta.canvas.bind('<B1-Motion>',lambda e: masterPressedMotion(meta,e,helper))
    meta.canvas.bind('<ButtonRelease-1>',lambda e: masterRelease(meta,e,helper))
    meta.canvas.bind('<Delete>',lambda e: delete(helper,meta))
    return helper
