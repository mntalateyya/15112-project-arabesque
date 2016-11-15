from  Tkinter import *
from PIL import Image, ImageDraw
import DrawMeta

class helperObject:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.linesIDs = []
        self.linesLoci = []
    def clear(self,c):
        for i in self.linesIDs:
            c.delete(i)


def press(e,helper):
    helper.x = e.x
    helper.y = e.y
    helper.linesLoci.append([e.x,e.y])

def move(e,helper,meta):
    if e.x != helper.x or e.y != helper.y:
        helper.linesIDs.append(meta.canvas.create_line(helper.x, helper.y, e.x,e.y,fill=meta.get_color(),width = int(meta.get_width())))
        helper.linesLoci[-1].append(e.x)
        helper.linesLoci[-1].append(e.y)
    helper.x, helper.y = e.x,e.y

def release(e,helper,meta):
    image = meta.get_image()
    draw = ImageDraw.Draw(image)
    for i in helper.linesLoci:
        draw.line(i,fill=meta.get_color(),width = int(meta.get_width()))
    image.save('test.png')
    meta.draw(image)
    for i in helper.linesIDs:
        meta.canvas.delete(i)
    helper.linesIDs = []
    helper.linesLoci = []


def activate(c,meta):
    helper = helperObject()
    c.bind('<Button-1>',lambda e: press(e,helper))
    c.bind('<B1-Motion>', lambda e: move(e, helper,meta))
    c.bind('<ButtonRelease-1>', lambda e: release(e, helper,meta))
