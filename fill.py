#   fill module
#   Code designed by: Mohammed Nurul Hoque (andrewID: mnurulho)
#   Filling algorithm cited from https://en.wikipedia.org/wiki/Flood_fill
#
#   15-112: Principles of Programming and Computer Science at Carnegie Mellon University in Qatar
#   Term Project
#
#   File created on: Tuesday 8 of November 2016, 20:15 PM
#   Modification History
#   Start:          End:
#   08/11/16 20:15  08/11/16 20:36
#   08/11/16 21:18  08/11/16 23:13

from Tkinter import *
import DrawMeta

class helperObject:
    def __init__(self,meta):
        self.x = None
        self.y = None
        self.bg = meta.get_bg()
        self.initial_col = (0,0,0)
        self.image = meta.get_image()

    def set_coords(self,e,meta):
        self.x = e.x
        self.y = e.y
        self.initial_col = self.image.getpixel((self.x,self.y))

    def reset_bg(self,col):
        self.bg = meta.get_bg()

# This algoriths is cited from https://en.wikipedia.org/wiki/Flood_fill
def fill_loop(im, fillColor, origin, w, h, q):
    print q
    while q!=[]:
        try:
            n = q.pop()
            im[n[0],n[1]] = fillColor
            if n[0]>0 and im[n[0]-1,n[1]] == origin:
                q.append((n[0]-1,n[1]))
            if n[0]<w-1 and im[n[0]+1,n[1]] == origin:
                q.append((n[0] + 1, n[1]))
            if n[1]>0 and im[n[0],n[1]-1] == origin:
                q.append((n[0] , n[1]-1))
            if n[1]<h-1 and im[n[0],n[1]+1] == origin:
                q.append((n[0], n[1] + 1))
        except:
            print n
    print 'finished', q


def fill(helper, c, e, meta):
    print'abc'
    if '#' + ''.join(str(x) for x in helper.initial_col) == helper.bg:
        return
    if e.x == helper.x and e.y == helper.y:
        pic = helper.image.load()
        # helper.draw.point((helper.x,helper.y),fill=helper.bg)
        w, h = helper.image.size
        q = []
        q.append((e.x, e.y))
        fill_color = (int(helper.bg[1:3],16),int(helper.bg[3:5],16),int(helper.bg[5:7],16))
        fill_loop(pic, fill_color, helper.initial_col, w, h, q)
        helper.image.save('test2.png')
        meta.draw(c)

def activate(c,meta):
    helper = helperObject(meta)
    c.bind('<Button-1>',lambda e: helper.set_coords(e,meta))
    c.bind('<ButtonRelease-1>',lambda e: fill(helper,c,e,meta))

wnd = Tk()
c = Canvas(wnd,bg='white',width=400,height=400)
c.pack()
meta = DrawMeta.MetaResources(400,400,'C:/Python27/test1.png')
meta.draw(c)
activate(c,meta)
wnd.mainloop()
