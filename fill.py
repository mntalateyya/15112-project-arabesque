#   fill module
#   Code designed by: Mohammed Nurul Hoque (andrewID: mnurulho)

#   ===== Filling algorithm cited from https://en.wikipedia.org/wiki/Flood_fill =====
#
#   15-112: Principles of Programming and Computer Science at Carnegie Mellon University in Qatar
#   Term Project
#
#   File created on: Tuesday 8 of November 2016, 20:15 PM
#   Modification History
#   Start:          End:
#   08/11/16 20:15  08/11/16 20:36
#   08/11/16 21:18  08/11/16 23:13
#   10/11/16 09:25  10/11/16 09:40
#   13/11/16 12:20  13/11/16 12:40
#   13/11/16 19:15  13/11/16 19:30
#   18/11/16 15:15  18/11/16 15:40
#   22/11/16 21:57  22/11/16 22:11

# a helper class to communicate data
class helperObject:
    def __init__(self,meta):
        # initialize fields
        self.x = None
        self.y = None
        self.color = ''
        self.initial_col = (0,0,0)
        self.image = meta.get_image()  # get current canvas image

    def set_coords(self,e,meta):
        meta.canvas.unbind('<Button-1>')
        # set data for clicked point
        self.image = meta.get_image()  # get current canvas image
        self.x = e.x
        self.y = e.y
        self.initial_col = self.image.getpixel((self.x,self.y))
        self.color = meta.get_color()

    # present to match interface only
    def clear(self,c):
        pass


# ===== This algoriths is cited from https://en.wikipedia.org/wiki/Flood_fill =====
def fill_loop( im, fillColor, origin, w, h, q):
    while q!=[]:  # queue is not empty
        n = q.pop()  # take out last pixel of queue
        im[n[0],n[1]] = fillColor  # fill pixel with fill color
        # if a neighbour pixel has the target color, add pixel to queue
        if n[0]>0 and im[n[0]-1,n[1]] == origin:
            q.append((n[0]-1,n[1]))
        if n[0]<w-1 and im[n[0]+1,n[1]] == origin:
            q.append((n[0] + 1, n[1]))
        if n[1]>0 and im[n[0],n[1]-1] == origin:
            q.append((n[0] , n[1]-1))
        if n[1]<h-1 and im[n[0],n[1]+1] == origin:
            q.append((n[0], n[1] + 1))
    
# =================================================================================

# fill the area contiguous with a pixel with the same color, with fill color
def fill(helper, e, meta):
    meta.canvas.unbind('<ButtonRelease-1>')
    if '#' + ''.join(str(x) for x in helper.initial_col) == helper.color:
        # if fill color and target color are same, do nothing
        return
    if e.x == helper.x and e.y == helper.y:
        # initialize variables and call the filling loop
        pic = helper.image.load()
        w, h = helper.image.size
        q = []
        q.append((e.x, e.y)) # append first point
        # convert fill color format from '#xxxxxx' to (x,y,z)
        fill_color = (int(helper.color[1:3],16),int(helper.color[3:5],16),int(helper.color[5:7],16))
        fill_loop(pic, fill_color, helper.initial_col, w, h, q)
        meta.draw(helper.image) # push image to canvas
    meta.canvas.bind('<Button-1>', lambda e: helper.set_coords(e, meta))
    meta.canvas.bind('<ButtonRelease-1>', lambda e: fill(helper, e, meta))

def activate(meta):
    # create helper image and bind canvas events to tool
    helper = helperObject(meta)
    meta.canvas.bind('<Button-1>',lambda e: helper.set_coords(e,meta))
    meta.canvas.bind('<ButtonRelease-1>',lambda e: fill(helper,e,meta))
    return helper
