#   meta data class
#   Code designed by: Mohammed Nurul Hoque (andrewID: mnurulho)
#
#   15-112: Principles of Programming and Computer Science at Carnegie Mellon University in Qatar
#   Term Project
#
#   File created on: Tuesday 8 of November 2016, 15:00 PM
#   Modification History
#   Start:          End:
#   08/11/16 15:55  08/11/16 16:03
#   08/11/16 17:40  08/11/16 18:15

from Tkinter import *
from PIL import Image, ImageTk


class MetaResources:
    def __init__(self, size_x, size_y,im=None):
        self.image = Image.new('RGB', (size_x, size_y), color='#ffffff')
        if im is not None:
            pic = Image.open(im)
            print pic.mode
            self.image.paste(pic,box=(0,0))
        self.imagesStack = []
        self.fg = '#000000'  # foreground color
        self.bg = '#990000'  # background color
        self.width = 1  # stroke width

    def get_image(self):
        return self.image.copy()

    def get_fg(self):
        return self.fg

    def get_bg(self):
        return self.bg

    def get_width(self):
        return self.width

    def set_fg(self, col):
        self.fg = col

    def set_bg(self, col):
        self.bg = col

    def set_width(self, w):
        self.width = w

    def draw(self, c, im):
        self.image = im
        photo = ImageTk.PhotoImage(image=self.image)
        c.one = photo
        c.create_image(0,0,image= photo,anchor=NW)

    #img_ice = ImageTk.PhotoImage(image=Image.open("ice.png"))
    #ice_img = c.create_image(500,345,image=img_ice)