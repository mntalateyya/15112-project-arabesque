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


def blink(c,helper,count=0):
    if helper.state in [1,2]:
        if count ==0:
            c.itemconfig(helper.square,outline='#ff8888')
        else:
            c.itemconfig(helper.square, outline='#888888')
    c.after(250,lambda : blink(c,helper,1-count))

def masterClick(c, e,helper):
    if helper.state==1 and not(helper.x1<e.x<helper.x2 and helper.y1<e.y<helper.y2):
        finalize()
        c.delete(helper.square)
        helper.state = 0
    if helper.state == 0:
        helper.x1,helper.y1 = e.x,e.y
        print 'x1,y1:', helper.x1, helper.y1
    elif helper.state == 1:
        helper.mousex = e.x
        helper.mousey = e.y
        helper.state = 2
        print 'e.x,e.y: ', e.x, e.y, '  =  '

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

def masterRelease(e,helper):
    if helper.state == 0:
        helper.image = meta.get_image().crop((helper.x1,helper.y1,helper.x2,helper.y2))
        blink(c,helper)
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
    if helper.state ==1:
        helper.image = meta.get_image().crop((helper.x1,helper.y1,helper.x2,helper.y2))


def copy(helper,meta):
    helper.image = meta.get_image().crop((helper.x1,helper.y1,helper.x2,helper.y2))

def paste(helper,meta):
    pass

def finalize():
    pass

def activate(c,meta):
    helper = helperObject()
    c.focus_set()
    c.bind('<Button-1>',lambda e: masterClick(c,e,helper))
    c.bind('<B1-Motion>',lambda e: masterPressedMotion(c,e,helper))
    c.bind('<ButtonRelease-1>',lambda e: masterRelease(e,helper))
    c.bind('x',lambda e: cut(helper,meta))
    c.bind('c',lambda e: copy(helper,meta))
    c.bind('v',lambda e: paste(helper,meta))

wnd = Tk()
c = Canvas(wnd,bg='white',width=400,height=400)
c.pack()
meta = DrawMeta.MetaResources(400,400,'C:/Python27/test1.png')
meta.draw(c)
activate(c,meta)
wnd.mainloop()