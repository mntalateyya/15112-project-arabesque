#   drawing root module
#   Code designed by: Mohammed Nurul Hoque (andrewID: mnurulho)
#
#   15-112: Principles of Programming and Computer Science at Carnegie Mellon University in Qatar
#   Term Project
#
#   File created on: Sunday 10th of November 2016, 08:55 PM
#   Modification History
#   Start:          End:
#   10/11/16 20:55  10/11/16 23:57
#   13/11/16 18:18  13/11/16 19:15
#   13/11/16 20:15  13/11/16 21:40
#   15/11/16 19:00  15/11/16 19:15
#   18/11/16 17:00  18/11/16 17:40
#   19/11/16 08:25  19/11/16 08:55
#   19/11/16 10:15  19/11/16 10:40
#   21/11/16 16:00  21/11/16 16:30
#   21/11/16 18:15  21/11/16 18:35
#   22/11/16 22:15  22/11/16 22:55
#   24/11/16 12:35  24/11/16 12:50

from Tkinter import *
import tkMessageBox
from PIL import Image, ImageTk, ImageDraw, ImageGrab
import math
import DrawMeta
import ColorPicker
import curve
import selection
import fill
import pencil
import shapes
import Eraser
import win32clipboard, StringIO

# This module has the class to create a window to draw shapes that returns an image
# when finish button pressed


# This is a class to create the drawing window
class drawer:
    def __init__(self,x,y,meta,mode,image=None,layer=None):
        # initialize fields
        self.mode = mode
        self.MainMeta = meta
        # create window
        self.root = Toplevel(bg='#888888')
        self.root.title('Draw')
        self.root.grab_set()
        s = '720x'+str(y+130)+'+200+0'
        self.root.geometry(s) # window size
        self.root.iconbitmap('Resources/icon.ico') # icon
        self.root.resizable(width=False, height=False) # fix size
        self.tools = Canvas(self.root,width=720,height=58,bg='white') # a canvas to draw tools
        self.canvas = Canvas(self.root,width=x,height=y,bg='white',cursor='crosshair',
                             bd=-2,highlightthickness=0) # drawing canvas
        self.tools.grid()
        self.canvas.grid(pady=10)
        self.bottom = Canvas(self.root,width=720,height=50,bg='#f0f0f0')
        self.bottom.grid()
        # meta class
        self.meta = DrawMeta.MetaResources(x,y,self,self.canvas,image if image is not None else None )
        self.layer = layer # keeps reference to the layer it is editing if any

        self.helper = None # reference to helper object of active tool
        # stroke width selector
        self.selectWidth = Spinbox(self.tools, from_=1, to=10, command = self.getWidth,buttonbackground='#00a2e8')
        self.tools.create_window(680,25,window=self.selectWidth,width=30)
        self.tools.create_text(680,52,text='width',fill='gray', font=('Arial','8'))

        self.labels,IDs = [],[] # to reference items

        # place tools' icons on window and bind them to their functions

        # undo
        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/undo.png')))
        self.tools.create_text(30, 52, text='undo', fill='gray', font=('Arial', '8'))
        IDs.append(self.tools.create_image(30, 24, image=self.labels[-1]))
        self.tools.tag_bind(IDs[-1], '<Button-1>', lambda e, id=IDs[-1]: self.flash(id,'undo'))
        self.tools.tag_bind(IDs[-1],'<ButtonRelease-1>',lambda e: self.meta.undo())

        # redo
        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/redo.png')))
        self.tools.create_text(74, 52, text='redo', fill='gray', font=('Arial','8'))
        IDs.append(self.tools.create_image(74, 24,image = self.labels[-1]))
        self.tools.tag_bind(IDs[-1], '<Button-1>', lambda e, id=IDs[-1]: self.flash(id, 'redo'))
        self.tools.tag_bind(IDs[-1],'<ButtonRelease-1>',lambda e: self.meta.redo())

        # select an area
        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/select.png')))
        self.tools.create_text(148, 52, text='select', fill='gray', font=('Arial','8'))
        IDs.append(self.tools.create_image(148, 24, image = self.labels[-1]))
        self.tools.tag_bind(IDs[-1],'<Button-1>',lambda e, i = IDs[-1]: self.activateTool(selection.activate,
                                                                                          i,'select',128))
        self.tools.tag_bind(IDs[-1],'<Enter>',lambda e, i = IDs[-1]: self.highlight(i))

        # bezier curve
        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/bezier.png')))
        self.tools.create_text(192, 52, text='bezier', fill='gray', font=('Arial', '8'))
        IDs.append(self.tools.create_image(192, 24, image=self.labels[-1]))
        self.tools.tag_bind(IDs[-1], '<Button-1>', lambda e, i = IDs[-1]: self.activateTool(curve.activate,
                                                                                            i,'bezier',172))
        self.tools.tag_bind(IDs[-1], '<Enter>', lambda e, i=IDs[-1]: self.highlight(i))

        # buckert fill
        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/fill.png')))
        self.tools.create_text(236, 52, text='fill', fill='gray', font=('Arial', '8'))
        IDs.append(self.tools.create_image(236, 24, image=self.labels[-1]))
        self.tools.tag_bind(IDs[-1], '<Button-1>', lambda e, i = IDs[-1]: self.activateTool(fill.activate,
                                                                                            i,'fill',216))
        self.tools.tag_bind(IDs[-1], '<Enter>', lambda e, i=IDs[-1]: self.highlight(i))

        # free pen
        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/pen.png')))
        self.tools.create_text(280, 52, text='pencil', fill='gray', font=('Arial', '8'))
        IDs.append(self.tools.create_image(280, 24, image=self.labels[-1]))
        self.tools.tag_bind(IDs[-1], '<Button-1>', lambda e, i = IDs[-1]: self.activateTool(pencil.activate
                                                                                            ,i,'pen',260))
        self.tools.tag_bind(IDs[-1], '<Enter>', lambda e, i=IDs[-1]: self.highlight(i))

        # chnage current tool to pen when window started
        self.focus = (IDs[-1], 'pen')
        self.square = self.tools.create_rectangle(260,4,300,44,outline='#00a2e8')
        self.activateTool(pencil.activate, IDs[-1],'pen',260)

        # draw a square tool
        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/square.png')))
        self.tools.create_text(324, 52, text='square', fill='gray', font=('Arial', '8'))
        IDs.append(self.tools.create_image(324, 24, image=self.labels[-1]))
        self.tools.tag_bind(IDs[-1], '<Button-1>', lambda e, i=IDs[-1]: self.activateTool(shapes.activate
                                                                                          , i,'square', 304,0))
        self.tools.tag_bind(IDs[-1], '<Enter>', lambda e, i=IDs[-1]: self.highlight(i))

        # drraw a circle tool
        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/circle.png')))
        self.tools.create_text(368, 52, text='circle', fill='gray', font=('Arial', '8'))
        IDs.append(self.tools.create_image(368, 24, image=self.labels[-1]))
        self.tools.tag_bind(IDs[-1], '<Button-1>', lambda e, i=IDs[-1]: self.activateTool(shapes.activate
                                                                                          , i,'circle',348, 1))
        self.tools.tag_bind(IDs[-1], '<Enter>', lambda e, i=IDs[-1]: self.highlight(i))

        # eraser tool
        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/eraser.png')))
        self.tools.create_text(412, 52, text='erase', fill='gray', font=('Arial', '8'))
        IDs.append(self.tools.create_image(412, 24, image=self.labels[-1]))
        self.tools.tag_bind(IDs[-1], '<Button-1>', lambda e, i=IDs[-1]: self.activateTool(Eraser.activate,
                                                                                          i,'eraser',392))
        self.tools.tag_bind(IDs[-1], '<Enter>', lambda e, i=IDs[-1]: self.highlight(i))

        # copy selection to clipboard
        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/copy.png')))
        self.tools.create_text(490, 52, text='copy', fill='gray', font=('Arial', '8'))
        IDs.append(self.tools.create_image(490, 24, image=self.labels[-1]))
        self.tools.tag_bind(IDs[-1], '<Enter>', lambda e, i=IDs[-1]: self.highlight(i))
        self.tools.tag_bind(IDs[-1], '<Button-1>', lambda e: self.copy())

        # paste image from clipboard
        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/paste.png')))
        self.tools.create_text(534, 52, text='paste', fill='gray', font=('Arial', '8'))
        IDs.append(self.tools.create_image(534, 24, image=self.labels[-1]))
        self.tools.tag_bind(IDs[-1], '<Enter>', lambda e, i=IDs[-1]: self.highlight(i))
        self.tools.tag_bind(IDs[-1], '<Button-1>', lambda e: self.paste())

        # current color and change color
        self.color = self.tools.create_oval(610,8,642,40,outline='#00a2e8',width=2,fill=self.meta.get_color())
        self.tools.create_text(626,52,text='color', fill='gray', font=('Arial', '8'))
        self.tools.tag_bind(self.color,'<Button-1>',lambda e: ColorPicker.ColorPicker(self))

        # finish button
        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/finish.png')))
        finish = self.bottom.create_image(670, 23, image=self.labels[-1])
        self.bottom.tag_bind(finish,'<ButtonRelease-1>',lambda e: self.finalize())

        self.canvas.focus_set()

        self.tools.lower(self.square)
        self.preprocess()
        self.root.mainloop()

    # color changing function
    def changeColor(self,color):
        self.meta.set_color(color)
        self.tools.itemconfig(self.color,fill=color) # update interface

    # this function deactivates last active tool and activates the new given tool
    def activateTool(self,func, id, string, x,shape=0):
        if self.helper is not None: # deactivate previous tool
            self.canvas.unbind('<Button-1>')
            self.canvas.unbind('<ButtonRelease-1>')
            self.canvas.unbind('<B1-Motion>')
            self.canvas.unbind('<Motion>')
            self.canvas.unbind('<Delete>')
            self.canvas.unbind('<space>')
            self.helper.clear(self.canvas)
        self.tools.lower(self.square)
        self.change_focus(id,string) # change active tool reference
        if func == shapes.activate: # square and oval
            self.helper = func(self.meta,shape)
        else:
            self.helper = func(self.meta)

    # complete the image, add layer to main window and close the window
    def finalize(self):
        if self.layer:
            self.MainMeta.remove_layer(self.layer)
        self.MainMeta.add_layer(self.postprocess(),self.mode)
        self.root.destroy()

    # get stroke width
    def getWidth(self):
        self.meta.set_width(self.selectWidth.get())

    # change active tool highlighting
    def change_focus(self,id,string):
        # reset icon of previous tool
        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/'+self.focus[1]+'.png')))
        self.tools.itemconfig(self.focus[0],image=self.labels[-1])

        # set icon of active tool
        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/'+string+'_.png')))
        self.tools.itemconfig(id, image=self.labels[-1])

        self.focus = (id,string)  # update reference

    # moves the highlighting rectangle to given tool when mouse hovers above it
    def highlight(self,id):
        x,y = self.tools.coords(id)
        self.tools.coords(self.square,x-20,y-20,x+20,y+20)

    # an icon flahes when clicked (for undo, redo, copy and paste)
    def flash(self,id,string,repeat=0):
        if not repeat:
            # if repeat = 0 change icon to highlighted version
            self.labels.append(ImageTk.PhotoImage(Image.open('Resources/'+string+'_.png')))
            self.tools.itemconfig(id,image=self.labels[-1])
            self.tools.after(200,lambda : self.flash(id,string,1))
        else:
            # change icon to un-highlighted version
            self.labels.append(ImageTk.PhotoImage(Image.open('Resources/' + string + '.png')))
            self.tools.itemconfig(id, image=self.labels[-1])

    # copy selected area to clipboard
    def copy(self):
        if self.focus[1]=='select'  and self.helper.image is not None:
            # if current tool is selct tool and an image is selected
            # ==============================================================================
            # This part was adapted from code at http://stackoverflow.com/questions/7050448/
            #         write-image-to-windows-clipboard-in-python-with-pil-and-win32clipboard
            output = StringIO.StringIO()
            self.helper.image.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]
            output.close()

            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()
            # ==============================================================================

    # pastes image from clipboard to canvas
    def paste(self):
        try:
            im = self.meta.get_image()
            im.paste(ImageGrab.grabclipboard(),(0,0))
            self.meta.draw(im)  # push new image to MetaResources
        except: # if no image in clipboard
            pass

    # creates black blocks on areas that will not be repeated when image is processed
    # only for polar mode
    def preprocess(self):
        tokens = self.mode.split('#')
        if tokens[0] in 'FL':
            return
        if tokens[0] == 'P':
            # if polar symmetric the lower triangle will not be repeated
            im = self.meta.get_image()
            disp = im.size[0]/math.tan(math.pi/int(tokens[-1]))
            if tokens[1] == 'S':
                # draw triangle to an image
                draw = ImageDraw.Draw(im)
                draw.polygon((im.size[0],im.size[1]-disp+1,im.size[0],im.size[1],1,im.size[1]),fill='black')

                # make image canvas image
                self.meta.image = im
                photo = ImageTk.PhotoImage(image=im)
                self.canvas.one = photo
                self.canvas.create_image(0, 0, image=photo, anchor=NW)
                tkMessageBox.showinfo('Borders', 'Only draw in the white area.\nThe rest will not show in the'
                                                 ' final drawing', parent=self.root)
            # if simple polar, two triangles formed by each vertical side with the middle of lower side
            # will not repeat
            elif self.mode[-2:]!='#2':
                disp*=0.5
                # draw triangle to an image
                draw = ImageDraw.Draw(im)
                draw.polygon((im.size[0],im.size[1]-disp+1,im.size[0],im.size[1],im.size[0]/2+1,im.size[1]), fill='black')
                draw.polygon((0,im.size[1]-disp+1,0,im.size[1],im.size[0]/2-1,im.size[1]), fill='black')

                # make image canvas image
                self.meta.image = im
                photo = ImageTk.PhotoImage(image=im)
                self.canvas.one = photo
                self.canvas.create_image(0, 0, image=photo, anchor=NW)
                tkMessageBox.showinfo('Borders', 'Only draw in the white area.\The rest will not show in the'
                                                 ' final drawing', parent=self.root)

    # remove preprocess triangles from image if polar
    def postprocess(self):
        tokens = self.mode.split('#')
        if self.mode[0] in 'FL':
            return self.meta.image
        if self.mode[0] == 'P':
            im = self.meta.get_image()
            disp = im.size[0] / math.tan(math.pi / int(tokens[-1]))
            if self.mode[2] == 'S':
                disp = disp
                draw = ImageDraw.Draw(im)
                draw.polygon((im.size[0], im.size[1] - disp+1, im.size[0], im.size[1], 1, im.size[1]), fill='#ffffff00')
            elif self.mode[-2:] != '#2':
                disp*=0.5
                draw = ImageDraw.Draw(im)
                draw.polygon((im.size[0], im.size[1] - disp+1, im.size[0], im.size[1], im.size[0] / 2 + 1, im.size[1]),
                             fill='#ffffff00')
                draw.polygon((0, im.size[1] - disp+1, 0, im.size[1], im.size[0] / 2 - 1, im.size[1]), fill='#ffffff00')
            else:
                im = self.meta.get_image()
            return im