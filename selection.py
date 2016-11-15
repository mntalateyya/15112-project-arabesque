#   curve module
#   Code designed by: Mohammed Nurul Hoque (andrewID: mnurulho)
#
#   15-112: Principles of Programming and Computer Science at Carnegie Mellon University in Qatar
#   Term Project
#
#   File created on: Wednesday 2nd of November 2016, 12:14 PM
#   Modification History
#   Start:          End:
#
from Tkinter import *
from PIL import Image,ImageTk
import DrawMeta

class helperObject:
    def __init__(self):
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        self.selection = (0,0,0,0)
        self.mousex = 0
        self.mousey = 0
        self.state = 0
        self.square = None
        self.image = None
        self.TkImage = None
        self.image_label = 0

    def clear(self,c):
        c.delete(self.square)
        c.delete(self.image_label)

def masterClick(c, e,helper,meta):
    if helper.state==1 and not(helper.x1<e.x<helper.x2 and helper.y1<e.y<helper.y2):
        helper.clear(c)
        print 'image',helper.image
        finalize(helper,meta)
        helper.state = 0
    if helper.state == 0:
        helper.x1,helper.y1 = e.x,e.y
    elif helper.state == 1:
        cut(helper,meta)
        helper.mousex = e.x
        helper.mousey = e.y
        helper.state = 2

def masterPressedMotion(c,e,helper):
    if helper.state == 0:
        helper.x2,helper.y2 = e.x,e.y
        c.delete(helper.square)
        helper.square = c.create_rectangle(helper.x1,helper.y1,helper.x2,helper.y2)

    if helper.state ==2:
        c.delete(helper.image_label)
        c.delete(helper.square)
        deltax = e.x-helper.mousex
        deltay = e.y-helper.mousey
        helper.TkImage = ImageTk.PhotoImage(image=helper.image)
        helper.image_label = c.create_image(helper.x1+deltax,helper.y1+deltay, image=helper.TkImage, anchor=NW)
        helper.square = c.create_rectangle(helper.x1+deltax,helper.y1+deltay,helper.x2+deltax,helper.y2+deltay)

def masterRelease(e,helper,meta):
    if helper.state == 0:
        if helper.x1>helper.x2: helper.x1,helper.x2=helper.x2,helper.x1
        if helper.y1 > helper.y2: helper.y1, helper.y2 = helper.y2, helper.y1
        
        helper.image = meta.get_image().crop((helper.x1,helper.y1,helper.x2,helper.y2))
        print helper.x1,helper.y1,helper.x2,helper.y2,helper.image,meta.get_image()
        helper.selection = helper.x1,helper.y1,helper.x2,helper.y2
        helper.state=1
    if helper.state ==2:
        deltax = e.x - helper.mousex
        deltay = e.y - helper.mousey
        helper.x1 += deltax
        helper.x2 += deltax
        helper.y1 += deltay
        helper.y2 += deltay
        helper.state = 1

def cut(helper,meta):
    print 'aaaa'
    image = meta.get_image()
    image.paste('white',helper.selection)
    meta.draw(image)
    helper.square = meta.canvas.create_rectangle(helper.x1, helper.y1, helper.x2, helper.y2)
    helper.image_label = meta.canvas.create_image(helper.x1, helper.y1,anchor=NW,image=helper.TkImage)

def copy(helper,meta):
    helper.image = meta.get_image().crop((helper.x1,helper.y1,helper.x2,helper.y2))

def paste(helper,meta):
    pass

def finalize(helper,meta):
    # paste image into meta image
    image = meta.get_image()
    image.paste(helper.image,(helper.x1, helper.y1, helper.x2, helper.y2))
    meta.draw(image)
    # clear canvas items
    helper.clear(meta.canvas)

def activate(c,meta):
    helper = helperObject()
    c.focus_set()
    c.bind('<Button-1>',lambda e: masterClick(c,e,helper,meta))
    c.bind('<B1-Motion>',lambda e: masterPressedMotion(c,e,helper))
    c.bind('<ButtonRelease-1>',lambda e: masterRelease(e,helper,meta))
    c.bind('x',lambda e: cut(helper,meta))
    c.bind('c',lambda e: copy(helper,meta))
    c.bind('v',lambda e: paste(helper,meta))
    return helper
