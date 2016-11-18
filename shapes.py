from PIL import ImageDraw

class HelperObject:
    def __init__(self,shape):
        self.x1, self.x2, self.y1, self.y2 = [None] * 4
        self.shape=shape
        self.draw = None

    def clear(self, c):
        c.delete(self.square)


def press(helper, meta,e):
    helper.x1, helper.y1 = e.x,e.y



def move(helper, meta,e):
    helper.x2,helper.y2 = e.x,e.y
    meta.canvas.delete(helper.draw)
    if helper.shape:
        helper.draw = meta.canvas.create_oval(helper.x1,helper.y1,helper.x2,helper.y2,outline=meta.get_color(),width=meta.get_width())
    else:
        helper.draw = meta.canvas.create_rectangle(helper.x1,helper.y1,helper.x2,helper.y2,outline=meta.get_color(),width=meta.get_width())


def release(helper, meta):
    if helper.x1 and helper.x2 and helper.y1 and helper.y2:
        if helper.x1>helper.x2: helper.x1,helper.x2 = helper.x2,helper.x1
        if helper.y1>helper.y2: helper.y1,helper.y2 = helper.y2,helper.y1
        image = meta.get_image()
        Draw = ImageDraw.Draw(image)
        if helper.shape:
            for i in range(meta.get_width()):
                Draw.ellipse((helper.x1+i,helper.y1+i,helper.x2-i,helper.y2-i),outline=meta.get_color())
        else:
            for i in range(meta.get_width()):
                Draw.rectangle((helper.x1+i,helper.y1+i,helper.x2-i,helper.y2-i),outline=meta.get_color())
        meta.draw(image)


def activate(meta,shape):
    helper = HelperObject(shape)
    meta.canvas.bind('<Button-1>', lambda e: press(helper, meta,e))
    meta.canvas.bind('<ButtonRelease-1>', lambda e: release(helper, meta))
    meta.canvas.bind('<B1-Motion>', lambda e: move(helper, meta,e))
    return helper