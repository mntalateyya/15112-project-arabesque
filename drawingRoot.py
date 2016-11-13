from Tkinter import *
from PIL import Image,ImageTk
import DrawMeta
import ColorPicker
import curve
import selection
import fill
import pencil

class drawer():
    def __init__(self,x,y,image=None,theta=None):
        self.root = Toplevel(bg='#888888')
        self.root.geometry('720x580')
        self.root.resizable(width=False, height=False)
        self.tools = Canvas(self.root,width=720,height=58,bg='white')
        self.canvas = Canvas(self.root,width=x,height=y,bg='white',cursor='tcross')
        self.meta = DrawMeta.MetaResources(x,y,self.canvas,image if image is not None else None )
        self.tools.grid()
        self.canvas.grid(pady=10)
        self.helper = None
        self.selectWidth = Spinbox(self.tools, from_=1, to=10, command = self.getWidth,buttonbackground='#00a2e8')
        self.tools.create_window(680,25,window=self.selectWidth,width=30)
        labels,IDs = [],[]

        labels.append(ImageTk.PhotoImage(Image.open('Resources/undo.png')))
        self.tools.create_text(30, 48, text='undo', fill='gray', font=('Arial', '8'))
        IDs.append(self.tools.create_image(30, 24, image=labels[-1]))
        print self.canvas.coords(IDs[-1]),'==='
        self.tools.tag_bind(IDs[-1],'<Button-1>',lambda e: self.meta.undo())

        labels.append(ImageTk.PhotoImage(Image.open('Resources/redo.png')))
        self.tools.create_text(74, 48, text='redo', fill='gray', font=('Arial','8'))
        IDs.append(self.tools.create_image(74, 24,image = labels[-1]))
        self.tools.tag_bind(IDs[-1],'<Button-1>',lambda e: self.meta.redo())

        labels.append(ImageTk.PhotoImage(Image.open('Resources/select.png')))
        self.tools.create_text(148, 48, text='select', fill='gray', font=('Arial','8'))
        IDs.append(self.tools.create_image(148, 24, image = labels[-1]))
        self.tools.tag_bind(IDs[-1],'<Button-1>',lambda e, i = IDs[-1]: self.activateTool(selection.activate,i))

        labels.append(ImageTk.PhotoImage(Image.open('Resources/bezier.png')))
        self.tools.create_text(192, 48, text='bezier', fill='gray', font=('Arial', '8'))
        IDs.append(self.tools.create_image(192, 24, image=labels[-1]))
        self.tools.tag_bind(IDs[-1], '<Button-1>', lambda e, i = IDs[-1]: self.activateTool(curve.activate,i))

        labels.append(ImageTk.PhotoImage(Image.open('Resources/fill.png')))
        self.tools.create_text(236, 48, text='fill', fill='gray', font=('Arial', '8'))
        IDs.append(self.tools.create_image(236, 24, image=labels[-1]))
        self.tools.tag_bind(IDs[-1], '<Button-1>', lambda e, i = IDs[-1]: self.activateTool(fill.activate,i))

        labels.append(ImageTk.PhotoImage(Image.open('Resources/pen.png')))
        self.tools.create_text(280, 48, text='pencil', fill='gray', font=('Arial', '8'))
        IDs.append(self.tools.create_image(280, 24, image=labels[-1]))
        self.tools.tag_bind(IDs[-1], '<Button-1>', lambda e, i = IDs[-1]: self.activateTool(pencil.activate,i))

        labels.append(ImageTk.PhotoImage(Image.open('Resources/square.png')))
        self.tools.create_text(324, 48, text='square', fill='gray', font=('Arial', '8'))
        IDs.append(self.tools.create_image(324, 24, image=labels[-1]))

        labels.append(ImageTk.PhotoImage(Image.open('Resources/circle.png')))
        self.tools.create_text(368, 48, text='circle', fill='gray', font=('Arial', '8'))
        IDs.append(self.tools.create_image(368, 24, image=labels[-1]))

        labels.append(ImageTk.PhotoImage(Image.open('Resources/eraser.png')))
        self.tools.create_text(412, 48, text='erase', fill='gray', font=('Arial', '8'))
        IDs.append(self.tools.create_image(412, 24, image=labels[-1]))

        labels.append(ImageTk.PhotoImage(Image.open('Resources/copy.png')))
        self.tools.create_text(476, 48, text='copy', fill='gray', font=('Arial', '8'))
        IDs.append(self.tools.create_image(476, 24, image=labels[-1]))

        labels.append(ImageTk.PhotoImage(Image.open('Resources/cut.png')))
        self.tools.create_text(520, 48, text='cut', fill='gray', font=('Arial', '8'))
        IDs.append(self.tools.create_image(520, 24, image=labels[-1]))

        labels.append(ImageTk.PhotoImage(Image.open('Resources/paste.png')))
        self.tools.create_text(564, 48, text='paste', fill='gray', font=('Arial', '8'))
        IDs.append(self.tools.create_image(564, 24, image=labels[-1]))

        self.color = self.tools.create_oval(610,8,642,40,outline='#00a2e8',width=2,fill=self.meta.get_color())
        self.tools.create_text(626,48,text='color', fill='gray', font=('Arial', '8'))
        self.tools.tag_bind(self.color,'<Button-1>',lambda e: ColorPicker.ColorPicker(self))
        self.canvas.bind('<Control_L><z>', self.meta.undo)
        self.canvas.bind('<Control_L><y>', lambda e: self.meta.redo)
        self.root.mainloop()

    def changeColor(self,color):
        self.meta.set_color(color)
        self.tools.itemconfig(self.color,fill=color)

    def activateTool(self,func,id):
        if self.helper is not None:
            self.canvas.unbind('<Button-1>')
            self.canvas.unbind('<ButtonRelease-1>')
            self.canvas.unbind('<B1-Motion>')
            self.canvas.unbind('<Motion>')
            self.canvas.unbind('x')
            self.canvas.unbind('c')
            self.canvas.unbind('v')
            self.helper.clear(self.canvas)
            self.canvas.itemconfig(id,outline='#ff00ff')
        print func
        func(self.canvas,self.meta)
    def getWidth(self):
        self.meta.set_width(self.selectWidth.get())
def highlight(c,id,f):
    labels = []
    labels.append(ImageTk.PhotoImage(Image.open(f)))
    c.itemconfig(id,image=labels[-1])


