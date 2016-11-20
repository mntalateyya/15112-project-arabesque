from Tkinter import *
from PIL import Image, ImageDraw
import Layer

class Meta:
    def __init__(self,parent):
        self.parent = parent
        self.layers = []
        self.focus_layer = None
        self.x = 620
        self.y = 540

    def add_layer(self,im):
        self.layers= [Layer.Layer(im,self)] + self.layers
        self.change_focus(self.layers[0])
        self.parent.redraw()

    def change_focus(self,layer):
        for i in self.layers:
            i.canvas.itemconfig(i.outline,outline='gray')
        layer.canvas.itemconfig(layer.outline,outline='#00a2e8')
        self.focus_layer = layer