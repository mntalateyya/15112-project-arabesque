from Tkinter import *
import tkMessageBox
from PIL import Image, ImageTk


class Resize:
    def __init__(self,parent):
        self.parent = parent

        self.root = Toplevel()
        self.root.grab_set()
        self.root.geometry('240x150')
        self.root.title('Resize')

        self.canvas = Canvas(self.root, width=240, height = 150, bg='white')
        self.canvas.pack()

        self.canvas.create_text(50, 40, text='Stretch in x:')
        self.canvas.create_text(50, 80, text='Stretch in y:')
        self.x = Entry(self.canvas,width = 15,
                       highlightcolor='#00a2e8',highlightbackground='gray', highlightthickness=1)
        self.y = Entry(self.canvas,width = 15,
                       highlightbackground='gray', highlightcolor='#00a2e8', highlightthickness=1)
        self.canvas.create_window(100,30,anchor=NW,window=self.x)
        self.canvas.create_window(100,70,anchor=NW,window=self.y)
        self.canvas.create_text(210,40,text='%')
        self.canvas.create_text(210, 80, text='%')
        pic = ImageTk.PhotoImage(Image.open('Resources/OK.png'))
        ok = self.canvas.create_image(120,120,image=pic)
        self.canvas.tag_bind(ok,'<ButtonRelease-1>',self.finish)

        self.root.mainloop()

    def finish(self,e):
        try:
            x = float(self.x.get())/100.0
            y = float(self.y.get())/100.0
            1/x
            1/y
        except:
            tkMessageBox.showerror('Invalid Input', 'Please enter a valid nonzero number',parent=self.root)
            return
        self.parent.resize_layer(x,y)
        self.root.destroy()



class Rotate:
    def __init__(self,parent):
        self.parent = parent

        self.root = Toplevel()
        self.root.grab_set()
        self.root.geometry('240x100')
        self.root.title('Rotate')

        self.canvas = Canvas(self.root, width=240, height = 100, bg='white')
        self.canvas.pack()

        self.canvas.create_text(50, 40, text='Angle:')
        self.angle = Entry(self.canvas,width = 15,
                       highlightcolor='#00a2e8',highlightthickness=1)
        self.canvas.create_window(100,30,anchor=NW,window=self.angle)
        self.canvas.create_text(210,40,text=unichr(0x00b0))
        pic = ImageTk.PhotoImage(Image.open('Resources/OK.png'))
        ok = self.canvas.create_image(120,80,image=pic)
        self.canvas.tag_bind(ok,'<ButtonRelease-1>',self.finish)

        self.root.mainloop()

    def finish(self,e):
        try:
            angle = float(self.angle.get())
        except:
            tkMessageBox.showerror('Error','please enter a valid number',parent=self.root)
        self.parent.rotate_layer(angle)
        self.root.destroy()