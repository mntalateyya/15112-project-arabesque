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
    def __init__(self, size_x, size_y,c,im=None):
        self.image = Image.new('RGB', (size_x, size_y), color='#ffffff')
        if im is not None:
            pic = Image.open(im)
            self.image.paste(pic,box=(0,0))
        self.undoStack = []
        self.redoStack = []
        self.color = '#000000'  # color
        self.width = 1  # stroke width
        self.canvas = c

    def get_image(self):
        return self.image.copy()

    def get_color(self):
        return self.color

    def get_width(self):
        return self.width

    def set_color(self, col):
        self.color = col

    def set_width(self, w):
        self.width = w

    def draw(self, im):
        self.undoStack.append(self.image)
        self.redoStack = []
        self.image = im
        photo = ImageTk.PhotoImage(image=self.image)
        self.canvas.one = photo
        self.canvas.create_image(0,0,image= photo,anchor=NW)

    def undo(self):
        if self.undoStack != []:
            self.redoStack.append(self.image)
            self.image = self.undoStack.pop()
            photo = ImageTk.PhotoImage(image=self.image)
            self.canvas.one = photo
            self.canvas.create_image(0, 0, image=photo, anchor=NW)

    def redo(self):
        if self.redoStack != []:
            self.undoStack.append(self.image)
            self.image = self.redoStack.pop()
            photo = ImageTk.PhotoImage(image=self.image)
            self.canvas.one = photo
            self.canvas.create_image(0, 0, image=photo, anchor=NW)


    #img_ice = ImageTk.PhotoImage(image=Image.open("ice.png"))
    #ice_img = c.create_image(500,345,image=img_ice)