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
#   13/11/16 12:35  13/11/16 12:55
#   18/11/16 15:20  18/11/16 15:45
#   22/11/16 21:50  22/11/16 21:56


from Tkinter import *
from PIL import Image, ImageTk


# This is a class that manages meta date for the drawing window
class MetaResources:
    def __init__(self, size_x, size_y,parent,c,im=None):
        self.image = Image.new('RGBA', (size_x, size_y), color='#ffffff00') # new image
        if im is not None: # if initialized with given image
            self.image.paste(im,box=(0,0))
        # undo and redo stacks
        self.undoStack = []
        self.redoStack = []
        self.color = '#000000'  # color
        self.width = 1  # stroke width
        self.parent = parent
        self.canvas = c
        self.photo = []
        self.photo.append(ImageTk.PhotoImage(self.image))
        self.canvas.create_image(0, 0, image=self.photo[-1], anchor=NW)

    # getters

    def get_image(self):
        return self.image.copy()

    def get_color(self):
        return self.color

    def get_width(self):
        return self.width

    # setters

    def set_color(self, col):
        self.color = col

    def set_width(self, w):
        self.width = int(w)

    # an image is pushed to canvas by a tool
    def draw(self, im):
        # update undo and redo stacks
        self.undoStack.append(self.image)
        self.redoStack = []

        # update image and draw on canvas
        self.canvas.delete('all')
        self.image = im
        self.photo.append(ImageTk.PhotoImage(self.image))
        self.canvas.create_image(0,0,image= self.photo[-1],anchor=NW)

    # undo a change in image
    def undo(self):
        # update stacks
        if self.undoStack != []:
            self.redoStack.append(self.image)
            self.image = self.undoStack.pop()
            self.canvas.delete('all')
            # draw on canvas
            self.photo.append(ImageTk.PhotoImage(self.image))
            self.canvas.create_image(0, 0, image=self.photo[-1], anchor=NW)

    # redo a change in image
    def redo(self):
        if self.redoStack != []:
            # update stacks
            self.undoStack.append(self.image)
            self.image = self.redoStack.pop()

            #draw on canvas
            self.canvas.delete('all')
            self.photo.append(ImageTk.PhotoImage(self.image))
            self.canvas.create_image(0, 0, image=self.photo[-1], anchor=NW)
