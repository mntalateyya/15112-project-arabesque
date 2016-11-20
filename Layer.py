from Tkinter import *
from PIL import Image, ImageTk
import MainMeta

class Layer():
    def __init__(self, im, meta):
        self.image = im.getbbox()
        self.x = meta.x / 2
        self.y = meta.y / 2
        self.widthO,self.heightO = im.size
        self.repr = im
        self.widthR, self.heightR = self.repr.size
        self.photos = []
        self.canvas = Canvas(meta.parent.frame2,width=235, height = 60, bg='white')
        self.str = 'Layer'+str(len(meta.layers))
        self.init_canvas()

    def get_im(self):
        return self.repr

    def get_canvas(self):
        return self.canvas

    def init_canvas(self):
        self.outline = self.canvas.create_rectangle(2,2,236,61,outline='#00a2e8')
        self.photos.append(ImageTk.PhotoImage(Image.open('Resources/visible.png')))
        self.canvas.create_image(12,30,image=self.photos[-1])

        self.visibility = IntVar()

        check = Checkbutton(self.canvas, variable = self.visibility, command = lambda: 111,
                            bg='white', activebackground='white')
        self.canvas.create_window(35,30,window=check)

        self.canvas.create_rectangle(50,5,150,55,outline='gray')
        if self.widthR>self.heightR*2:
            ratio = 100.0/self.widthR
        else:
            ratio = 50.0/self.heightR
        self.photos.append(ImageTk.PhotoImage(self.repr.resize((
            int(self.widthR * ratio)-2, int(self.heightR * ratio)-2))))
        self.thumbnail = self.canvas.create_image(100,30,image = self.photos[-1])
        self.canvas.create_text(175,30,text=self.str,fill='#00a2e8')

        self.photos.append(ImageTk.PhotoImage(Image.open('Resources/up.png')))
        self.up = self.canvas.create_image(210,10,image=self.photos[-1])

        self.photos.append(ImageTk.PhotoImage(Image.open('Resources/down.png')))
        self.up = self.canvas.create_image(210, 30, image=self.photos[-1])

        self.photos.append(ImageTk.PhotoImage(Image.open('Resources/mergeL.png')))
        self.up = self.canvas.create_image(210, 50, image=self.photos[-1])
