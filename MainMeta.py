#   Main Meta module
#   Code designed by: Mohammed Nurul Hoque (andrewID: mnurulho)
#
#   15-112: Principles of Programming and Computer Science at Carnegie Mellon University in Qatar
#   Term Project
#
#   File created on: Saturday 19th of November 2016, 12:14 PM
#   Modification History
#   Start:          End:
#   19/11/16 20:30  19/11/16 21:25
#   20/11/16 16:30  20/11/16 17:30
#   23/11/16 11:15  23/11/16 11:30
#   26/11/16 10:45  26/11/16 10:55

from Tkinter import *
from PIL import Image
import Layer

# This is a helper module that has a class to save the data of the main program


class Meta:
    def __init__(self,parent):
        # initialize
        self.parent = parent
        self.layers = []  # all layers' references
        self.focus_layer = None  # the currently active layer
        self.image= Image.new('RGBA',(620,540),'#ffffff00')
        self.x = 620
        self.y = 540

    # add a layer from given image and redraw the canvas
    def add_layer(self,im,mode):
        if len(self.layers)<5:
            self.layers= [Layer.Layer(im,mode,self)] + self.layers
            self.parent.redraw()
            self.change_focus(self.layers[0]) # change focus to created layer

    # remove a layer and redraw canvas
    def remove_layer(self,layer):
        self.layers.pop(self.layers.index(layer))
        self.parent.redraw()
        if self.layers:
            self.change_focus(self.layers[0]) # focus to first layer if any

    # change the order of layers and redraw canvas
    # by = 1 -> move layer one step up
    # by = 0 -> move layer one step down
    def move_layer(self,layer,by):
        i = self.layers.index(layer)
        if by:
            self.layers[i],self.layers[i-1], = self.layers[i-1], self.layers[i]
        else:
            self.layers[i],self.layers[i+1] = self.layers[i+1], self.layers[i]
        self.parent.redraw()
        self.change_focus(layer)  # focus to layer just moved

    # merge a layer with the layer below it and redraw canvas
    def merge_layers(self,layer):
        i = self.layers.index(layer)
        im  = Image.new('RGBA',(620,620),'#ffffff00')  # a new image to paste both layers to
        im.paste(self.layers[i+1].repr,(self.layers[i+1].x,self.layers[i+1].y),self.layers[i+1].repr)
        im.paste(layer.repr, (layer.x, layer.y),layer.repr)
        self.layers.pop(i)  # remove both
        self.layers.pop(i)
        self.add_layer(im,'F')  # create a new layer with the pasted image
        self.parent.redraw()
        self.change_focus(self.layers[0])  # focus to layer just created

    # takes a layer changes focus to it and updates canvas accordingly
    def change_focus(self,layer):
        # highlight the layer to focus with blue, gray for all other layers
        for i in self.layers:
            i.canvas.config(highlightbackground='gray')
        layer.canvas.config(highlightbackground='#00a2e8')
        self.focus_layer = layer