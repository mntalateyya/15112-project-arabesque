from Tkinter import *
from PIL import Image, ImageDraw
import Layer

class Meta:
    def __init__(self,parent):
        self.parent = parent
        self.layers = []
        self.focus_layer = None
        self.image= Image.new('RGBA',(620,540),'#ffffff00')
        self.x = 620
        self.y = 540

    def add_layer(self,im,mode):
        if len(self.layers)<5:
            self.layers= [Layer.Layer(im,mode,self)] + self.layers
            self.parent.redraw()
            self.change_focus(self.layers[0])

    def remove_layer(self,layer):
        self.layers.pop(self.layers.index(layer))
        self.parent.redraw()
        if self.layers:
            self.change_focus(self.layers[0])

    def move_layer(self,layer,by):
        i = self.layers.index(layer)
        if by:
            self.layers[i],self.layers[i-1], = self.layers[i-1], self.layers[i]
        else:
            self.layers[i],self.layers[i+1] = self.layers[i+1], self.layers[i]
        self.parent.redraw()
        self.change_focus(layer)

    def merge_layers(self,layer):
        i = self.layers.index(layer)
        im  = Image.new('RGBA',(620,620),'#ffffff00')
        im.paste(self.layers[i+1].repr,(self.layers[i+1].x,self.layers[i+1].y),self.layers[i+1].repr)
        im.paste(layer.repr, (layer.x, layer.y),layer.repr)
        self.layers.pop(i)
        self.layers.pop(i)
        self.add_layer(im,'F')
        self.parent.redraw()
        self.change_focus(self.layers[0])

    def change_focus(self,layer):
        for i in self.layers:
            i.canvas.config(highlightbackground='gray')
        layer.canvas.config(highlightbackground='#00a2e8')
        self.focus_layer = layer