#   Layer module
#   Code designed by: Mohammed Nurul Hoque (andrewID: mnurulho)
#
#   15-112: Principles of Programming and Computer Science at Carnegie Mellon University in Qatar
#   Term Project
#
#   File created on: Saturday 19 of November 2016, 06:12 PM
#   Modification History
#   Start:          End:
#   19/11/16 18:12  19/11/16 18:23
#   19/11/16 18:50  19/11/16 20:18
#   19/11/16 21:35  19/11/16 21:50
#   20/11/16 17:50  20/11/16 15:25
#   26/11/16 11:35  26/11/16 11:43

from Tkinter import *
from PIL import Image, ImageTk
import math

# This module packs the data of each layer in the main canvas and shows its representation

class Layer():
    def __init__(self, im, mode, meta):
        self.image = im  # original image of layer
        self.mode = mode
        self.meta = meta
        self.x = 0
        self.y = 0
        self.widthO,self.heightO = im.size
        self.repr = process(self.image,self.mode)  # image to represent layer on canvas
        self.widthR, self.heightR = self.repr.size
        self.photos = []
        self.canvas = Canvas(meta.parent.frame2,width=235, height = 60, bg='white')
        self.init_canvas()

    # getters
    def get_im(self):
        return self.repr

    def get_canvas(self):
        return self.canvas

    # set image of layer
    def set_im(self,im):
        self.repr = im

    # create the layer label (a canvas)
    def init_canvas(self):
        self.canvas.config(highlightbackground='#00a2e8')

        # create a thumbnail of the layer's image
        # ewsize
        if self.widthR>self.heightR*1.5:
            ratio = 75.0/self.widthR
        else:
            ratio = 50.0/self.heightR
        self.photos.append(ImageTk.PhotoImage(self.repr.resize((
            int(self.widthR * ratio)-2, int(self.heightR * ratio)-2),Image.ANTIALIAS)))
        # draw
        self.thumbnail = self.canvas.create_image(47,32,image = self.photos[-1])
        self.canvas.create_rectangle(10, 7, 85, 57, outline='gray')

        # tools' icons
        # move up
        self.photos.append(ImageTk.PhotoImage(Image.open('Resources/up.png')))
        self.up = self.canvas.create_image(100,30,image=self.photos[-1])
        self.canvas.tag_bind(self.up,'<ButtonRelease-1>',lambda e: self.move(1))
        # move down
        self.photos.append(ImageTk.PhotoImage(Image.open('Resources/down.png')))
        self.down = self.canvas.create_image(125, 30, image=self.photos[-1])
        self.canvas.tag_bind(self.down, '<ButtonRelease-1>', lambda e: self.move(0))
        # merge with below
        self.photos.append(ImageTk.PhotoImage(Image.open('Resources/mergeL.png')))
        self.mergeL = self.canvas.create_image(150, 30, image=self.photos[-1])
        self.canvas.tag_bind(self.mergeL, '<ButtonRelease-1>', lambda e: self.merge())
        # duplicate
        self.photos.append(ImageTk.PhotoImage(Image.open('Resources/duplicate.png')))
        self.duplicate = self.canvas.create_image(175, 30, image=self.photos[-1])
        self.canvas.tag_bind(self.duplicate,'<ButtonRelease-1>',
                             lambda e: self.meta.add_layer(self.image.copy(),self.mode))
        # delete
        self.photos.append(ImageTk.PhotoImage(Image.open('Resources/delete.png')))
        self.delete = self.canvas.create_image(200, 30, image=self.photos[-1])
        self.canvas.tag_bind(self.delete, '<ButtonRelease-1>', lambda e: self.meta.remove_layer(self))
        # bind clicking on layer's label to changing focus to the layer
        self.canvas.bind('<Button-1>', lambda e: self.meta.change_focus(self))

    # call the functions in parent window to execute the command
    def move(self,i):
        self.meta.move_layer(self,i)

    def merge(self):
        self.meta.merge_layers(self)

    # redraw label canvas
    def redraw(self):
        self.canvas.delete('all') # delete all items
        self.init_canvas()  # redraw

    # configure as first layer in stack (disable move up)
    def config_first(self):
        self.canvas.tag_unbind(self.up,'<ButtonRelease-1>')
        self.photos.append(ImageTk.PhotoImage(Image.open('Resources/up_.png')))
        self.canvas.itemconfig(self.up,image=self.photos[-1])

    # configure as first layer in stack (disable move down and merge with below)
    def config_last(self):
        self.canvas.tag_unbind(self.down, '<ButtonRelease-1>')
        self.photos.append(ImageTk.PhotoImage(Image.open('Resources/down_.png')))
        self.canvas.itemconfig(self.down, image=self.photos[-1])

        self.canvas.tag_unbind(self.mergeL, '<ButtonRelease-1>')
        self.photos.append(ImageTk.PhotoImage(Image.open('Resources/mergeL_.png')))
        self.canvas.itemconfig(self.mergeL, image=self.photos[-1])


# process image to complete pattern
def process(im,mode):
    tokens = mode.split('#')  # split mode string
    x, y = im.size
    image = im
    if tokens[0]=='F':
        return image

    if len(tokens)>1 and tokens[1] == 'S':  # symmetric drawing, mirror image
        image = Image.new('RGBA', (x * 2, y))
        image.paste(im, (x, 0))
        image.paste(im.transpose(Image.FLIP_LEFT_RIGHT), (0, 0))
        im = image

    if tokens[0] == 'P':  # polar drawing, repeat the image around a circle
        n = int(tokens[-1])  # number repetitions
        image = rotate(im, n)

    if tokens[0] == 'L':
        n = int(tokens[-1])  # number repetitions
        image = Image.new('RGBA',(im.size[0]*n, im.size[1]))
        for i in range(n):
            image.paste(im,(i*im.size[0],0))

    return image


# this function takes an image reference and number of repetitions as inputs and putputs and image
# that is an n-time-repeated version of input image around centre.
def rotate(im, n):
    x, y = im.size
    output = Image.new('RGBA', (y * 2, y * 2))  # new image

    # paste two copies
    output.paste(im, (y - x / 2, 0))
    output.paste(im.transpose(Image.ROTATE_180), (y - x / 2, y))

    theta = 2 * math.pi / n  # angle of rotation
    pic = output.load()
    for block in range(1, (n - 2) / 2 + 1):  # loop through number of blocks required
        for xcoord in range(-y + 1, 0):  # all x
            # upper and lower bound on y for given x
            limits = [int(xcoord * math.tan(block * theta - theta / 2.0 + math.pi / 2)),
                      int(xcoord * math.tan(block * theta + theta / 2.0 + math.pi / 2))]
            for ycoord in range(max(min(limits), -y + 1), min(max(limits), y - 1)):  # all values of y
                # get coordinated of pixel to copy from
                origin = int(xcoord * math.cos(theta * block) + ycoord * math.sin(theta * block)), \
                         int(-xcoord * math.sin(theta * block) + ycoord * math.cos(theta * block))
                if -y + 1 < origin[0] < y - 1 and -y + 1 < origin[1] < y - 1:  # within limits
                    pix = pic[origin[0] + y, -origin[1] + y]  # get color
                    if -y < origin[0] < y and -y < origin[1] < y:  # copy color
                        pic[xcoord + y, -ycoord + y] = pix
                        pic[-xcoord + y, ycoord + y] = pix

    return output
