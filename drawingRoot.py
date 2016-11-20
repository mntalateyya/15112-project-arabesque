from Tkinter import *
from PIL import Image,ImageTk
import DrawMeta
import ColorPicker
import curve
import selection
import fill
import pencil
import shapes

# This is a class to create the drawing window
class drawer():
    def __init__(self,x,y,meta,image=None,theta=None):
        self.MainMeta = meta
        # create window
        self.root = Toplevel(bg='#888888')
        self.root.geometry('720x'+str(y+130)) # window size
        self.root.iconbitmap('Resources/icon.ico') # icon
        self.root.resizable(width=False, height=False) # fixed size
        self.tools = Canvas(self.root,width=720,height=58,bg='white') # a canvas to draw tools
        self.canvas = Canvas(self.root,width=x,height=y,bg='white',cursor='tcross') # drawing canvas
        self.tools.grid()
        self.canvas.grid(pady=10)
        self.bottom = Canvas(self.root,width=720,height=50,bg='#f0f0f0')
        self.bottom.grid()
        # meta class
        self.meta = DrawMeta.MetaResources(x,y,self.canvas,image if image is not None else None )

        self.helper = None # reference to helper object of active tool\
        self.selectWidth = Spinbox(self.tools, from_=1, to=10, command = self.getWidth,buttonbackground='#00a2e8')
        self.tools.create_window(680,25,window=self.selectWidth,width=30)
        self.labels,IDs = [],[]

        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/undo.png')))
        self.tools.create_text(30, 52, text='undo', fill='gray', font=('Arial', '8'))
        IDs.append(self.tools.create_image(30, 24, image=self.labels[-1]))
        self.tools.tag_bind(IDs[-1],'<Button-1>',lambda e: self.meta.undo())

        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/redo.png')))
        self.tools.create_text(74, 52, text='redo', fill='gray', font=('Arial','8'))
        IDs.append(self.tools.create_image(74, 24,image = self.labels[-1]))
        self.tools.tag_bind(IDs[-1],'<Button-1>',lambda e: self.meta.redo())

        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/select.png')))
        self.tools.create_text(148, 52, text='select', fill='gray', font=('Arial','8'))
        IDs.append(self.tools.create_image(148, 24, image = self.labels[-1]))
        self.tools.tag_bind(IDs[-1],'<Button-1>',lambda e, i = IDs[-1]: self.activateTool(selection.activate,
                                                                                          i,'select',128))
        self.tools.tag_bind(IDs[-1],'<Enter>',lambda e, i = IDs[-1]: self.highlight(i))

        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/bezier.png')))
        self.tools.create_text(192, 52, text='bezier', fill='gray', font=('Arial', '8'))
        IDs.append(self.tools.create_image(192, 24, image=self.labels[-1]))
        self.tools.tag_bind(IDs[-1], '<Button-1>', lambda e, i = IDs[-1]: self.activateTool(curve.activate,
                                                                                            i,'bezier',172))
        self.tools.tag_bind(IDs[-1], '<Enter>', lambda e, i=IDs[-1]: self.highlight(i))

        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/fill.png')))
        self.tools.create_text(236, 52, text='fill', fill='gray', font=('Arial', '8'))
        IDs.append(self.tools.create_image(236, 24, image=self.labels[-1]))
        self.tools.tag_bind(IDs[-1], '<Button-1>', lambda e, i = IDs[-1]: self.activateTool(fill.activate,
                                                                                            i,'fill',216))
        self.tools.tag_bind(IDs[-1], '<Enter>', lambda e, i=IDs[-1]: self.highlight(i))

        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/pen.png')))
        self.tools.create_text(280, 52, text='pencil', fill='gray', font=('Arial', '8'))
        IDs.append(self.tools.create_image(280, 24, image=self.labels[-1]))
        self.tools.tag_bind(IDs[-1], '<Button-1>', lambda e, i = IDs[-1]: self.activateTool(pencil.activate
                                                                                            ,i,'pen',260))
        self.tools.tag_bind(IDs[-1], '<Enter>', lambda e, i=IDs[-1]: self.highlight(i))

        self.focus = (IDs[-1], 'pen')
        self.square = self.tools.create_rectangle(260,4,300,44,outline='#00a2e8')
        self.activateTool(pencil.activate, IDs[-1],'pen',260)

        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/square.png')))
        self.tools.create_text(324, 52, text='square', fill='gray', font=('Arial', '8'))
        IDs.append(self.tools.create_image(324, 24, image=self.labels[-1]))
        self.tools.tag_bind(IDs[-1], '<Button-1>', lambda e, i=IDs[-1]: self.activateTool(shapes.activate
                                                                                          , i,'square', 304,0))
        self.tools.tag_bind(IDs[-1], '<Enter>', lambda e, i=IDs[-1]: self.highlight(i))

        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/circle.png')))
        self.tools.create_text(368, 52, text='circle', fill='gray', font=('Arial', '8'))
        IDs.append(self.tools.create_image(368, 24, image=self.labels[-1]))
        self.tools.tag_bind(IDs[-1], '<Button-1>', lambda e, i=IDs[-1]: self.activateTool(shapes.activate
                                                                                          , i,'circle',348, 1))
        self.tools.tag_bind(IDs[-1], '<Enter>', lambda e, i=IDs[-1]: self.highlight(i))

        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/eraser.png')))
        self.tools.create_text(412, 52, text='erase', fill='gray', font=('Arial', '8'))
        IDs.append(self.tools.create_image(412, 24, image=self.labels[-1]))
        self.tools.tag_bind(IDs[-1], '<Enter>', lambda e, i=IDs[-1]: self.highlight(i))

        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/copy.png')))
        self.tools.create_text(476, 52, text='copy', fill='gray', font=('Arial', '8'))
        IDs.append(self.tools.create_image(476, 24, image=self.labels[-1]))
        self.tools.tag_bind(IDs[-1], '<Enter>', lambda e, i=IDs[-1]: self.highlight(i))

        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/cut.png')))
        self.tools.create_text(520, 52, text='cut', fill='gray', font=('Arial', '8'))
        IDs.append(self.tools.create_image(520, 24, image=self.labels[-1]))
        self.tools.tag_bind(IDs[-1], '<Enter>', lambda e, i=IDs[-1]: self.highlight(i))

        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/paste.png')))
        self.tools.create_text(564, 52, text='paste', fill='gray', font=('Arial', '8'))
        IDs.append(self.tools.create_image(564, 24, image=self.labels[-1]))
        self.tools.tag_bind(IDs[-1], '<Enter>', lambda e, i=IDs[-1]: self.highlight(i))

        self.color = self.tools.create_oval(610,8,642,40,outline='#00a2e8',width=2,fill=self.meta.get_color())
        self.tools.create_text(626,52,text='color', fill='gray', font=('Arial', '8'))
        self.tools.tag_bind(self.color,'<Button-1>',lambda e: ColorPicker.ColorPicker(self))
        self.canvas.bind('<Control_L><z>', self.meta.undo)
        self.canvas.bind('<Control_L><y>', lambda e: self.meta.redo)

        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/finish.png')))
        finish = self.bottom.create_image(670, 23, image=self.labels[-1])
        self.bottom.tag_bind(finish,'<ButtonRelease-1>',lambda e: self.finalize())

        self.tools.lower(self.square)

        self.root.mainloop()

    def changeColor(self,color):
        self.meta.set_color(color)
        self.tools.itemconfig(self.color,fill=color)

    def activateTool(self,func, id, string, x,shape=0):
        if self.helper is not None:
            self.canvas.unbind('<Button-1>')
            self.canvas.unbind('<ButtonRelease-1>')
            self.canvas.unbind('<B1-Motion>')
            self.canvas.unbind('<Motion>')
            self.canvas.unbind('x')
            self.canvas.unbind('c')
            self.canvas.unbind('v')
            self.helper.clear(self.canvas)
        self.tools.delete(self.square)
        self.square = self.tools.create_rectangle(x,4,x+40,44,outline = '#00a2e8')
        self.tools.lower(self.square)
        self.change_focus(id,string)
        if func == shapes.activate:
            func(self.meta,shape)
        else:
            func(self.meta)

    def finalize(self):
        self.MainMeta.add_layer(self.meta.get_image())
        self.root.destroy()

    def getWidth(self):
        self.meta.set_width(self.selectWidth.get())

    def change_focus(self,id,string):
        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/'+self.focus[1]+'.png')))
        self.tools.itemconfig(self.focus[0],image=self.labels[-1])
        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/'+string+'_.png')))
        self.tools.itemconfig(id, image=self.labels[-1])
        self.focus = (id,string)

    def highlight(self,id):
        x,y = self.tools.coords(id)
        self.tools.coords(self.square,x-20,y-20,x+20,y+20)
