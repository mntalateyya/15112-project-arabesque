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

def masterClick(meta, e,helper):
    if helper.state==1 and not(helper.x1<e.x<helper.x2 and helper.y1<e.y<helper.y2):
        meta.canvas.delete(helper.square)
        helper.state = 0
    if helper.state == 0:
        helper.x1,helper.y1 = e.x,e.y
    elif helper.state == 1:
        helper.mousex = e.x
        helper.mousey = e.y
        new_im = meta.get_image()
        new_im.paste('#ffffff00', (helper.x1, helper.y1, helper.x2, helper.y2))
        meta.draw(new_im)
        helper.state = 2

def masterPressedMotion(meta,e,helper):
    if helper.state == 0:
        helper.x2,helper.y2 = e.x,e.y
        meta.canvas.delete(helper.square)
        helper.square = meta.canvas.create_rectangle(helper.x1,helper.y1,helper.x2,helper.y2)
    if helper.state ==2:
        meta.canvas.delete(helper.image_label)
        meta.canvas.delete(helper.square)
        deltax = e.x-helper.mousex
        deltay = e.y-helper.mousey
        helper.TkImage = ImageTk.PhotoImage(image=helper.image)
        helper.image_label = meta.canvas.create_image(helper.x1+deltax,helper.y1+deltay, image=helper.TkImage, anchor=NW)
        helper.square = meta.canvas.create_rectangle(helper.x1+deltax,helper.y1+deltay,helper.x2+deltax,helper.y2+deltay)

def masterRelease(meta, e,helper):

    if helper.state == 0  and e.x!=helper.x1 and e.y!=helper.y1:
        helper.image = meta.get_image().crop((helper.x1,helper.y1,helper.x2,helper.y2))
        helper.state=1

    if helper.state ==2:
        deltax = e.x - helper.mousex
        deltay = e.y - helper.mousey
        helper.x1 += deltax
        helper.x2 += deltax
        helper.y1 += deltay
        helper.y2 += deltay
        finalize(meta, helper)
        helper.state = 1

def cut(helper,meta):
    if helper.state ==1:
        to_paste = Image.new('RGB', (abs(helper.x2 - helper.x1), abs(helper.y2 - helper.y1)), '#ffffff')
        new_im = meta.get_image()
        new_im.paste(to_paste,(helper.x1, helper.y1, helper.x2, helper.y2))
        meta.draw(new_im)

def copy(helper,meta):
    if helper.state ==1:
        pass

def paste(helper,meta):
    pass

def finalize(meta,helper):
    if helper.x1>helper.x2:
        helper.x1,helper.x2 = helper.x2,helper.x1
    if helper.y1>helper.y2:
        helper.y1,helper.y2 = helper.y2, helper.y1
    # paste image into meta image
    image = meta.get_image()
    print image
    image.paste(helper.image, (helper.x1, helper.y1, helper.x2, helper.y2),helper.image)
    meta.draw(image)
    # clear canvas items
    helper.clear(meta.canvas)
    helper.state = 0

def activate(meta):
    helper = helperObject()
    meta.canvas.focus_set()
    meta.canvas.bind('<Button-1>',lambda e: masterClick(meta,e,helper))
    meta.canvas.bind('<B1-Motion>',lambda e: masterPressedMotion(meta,e,helper))
    meta.canvas.bind('<ButtonRelease-1>',lambda e: masterRelease(meta,e,helper))
    meta.canvas.bind('x',lambda e: cut(helper,meta))
    meta.canvas.bind('c',lambda e: copy(helper,meta))
    meta.canvas.bind('v',lambda e: paste(helper,meta))
    return helper
