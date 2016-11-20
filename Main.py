#   curve module
#   Code designed by: Mohammed Nurul Hoque (andrewID: mnurulho)
#
#   15-112: Principles of Programming and Computer Science at Carnegie Mellon University in Qatar
#   Term Project
#
#   File created on: Wednesday 2nd of November 2016, 12:14 PM
#   Modification History
#   Start:          End:

# This is the root window of the program

from Tkinter import *
import tkFileDialog
from PIL import Image, ImageTk
import drawingRoot
import MainMeta

#create window
class Main:
    def __init__(self):
        self.root = Tk()
        self.root.geometry('900x600')
        self.root.resizable(width=False,height=False)
        self.root.iconbitmap('Resources/icon.ico')

        self.meta = MainMeta.Meta(self)

        self.IDs= []
        photoImages = []
        # Layout using nested frames
        self.frame1 = Frame(self.root,width=640,height=600)
        self.frame2 = Frame(self.root, width=235, height=600)
        self.frame1.grid(sticky=NW)
        self.frame2.grid(row=0, column=1, sticky=NW)

        self.canvas = Canvas(self.frame1,width=620,height=540,bg='#ffffff')
        self.canvas.config(scrollregion=(0,0,620,540))
        self.canvas.grid(padx=10,pady=10)
        
        self.metaTools = Canvas(self.frame2, width=235, height=60, bg='#ffffff')
        self.metaTools.grid(pady=10)
        self.tools = Canvas(self.frame2, width=235, height=175, bg='#ffffff')
        self.tools.grid(sticky=NW)

        self.canvas.create_rectangle(0,0,619,539,outline='#00a2e8')
        self.metaTools.create_rectangle(2,2,236,61,outline='#00a2e8')
        self.tools.create_rectangle(2,2,235,175,outline='#00a2e8')

        self.tools.create_rectangle(2,2,236,30,width=0,fill='#00a2e8')
        self.tools.create_text(117,15,text='Layers',fill='white',font=('Arial',12))

        self.image = Image.open('Resources/export.png')
        photoImages.append(ImageTk.PhotoImage(self.image))
        self.IDs.append(self.metaTools.create_image(83,25,image=photoImages[-1]))
        self.metaTools.create_text(83,50,text='Export',fill='#888888',font=('Arial',8))

        self.image = Image.open('Resources/clear.png')
        photoImages.append(ImageTk.PhotoImage(self.image))
        self.IDs.append(self.metaTools.create_image(151,25,image=photoImages[-1]))
        self.metaTools.create_text(151,50,text='Clear',fill='#888888',font=('Arial',8))

        self.image = Image.open('Resources/pen.png')
        photoImages.append(ImageTk.PhotoImage(self.image))
        self.IDs.append(self.tools.create_image(40,60,image=photoImages[-1]))
        self.tools.create_text(40,85,text='Edit',fill='#888888',font=('Arial',8))

        self.image = Image.open('Resources/moveL.png')
        photoImages.append(ImageTk.PhotoImage(self.image))
        self.IDs.append(self.tools.create_image(90,60,image=photoImages[-1]))
        self.tools.create_text(90,85,text='Move',fill='#888888',font=('Arial',8))

        self.image = Image.open('Resources/resizeL.png')
        photoImages.append(ImageTk.PhotoImage(self.image))
        self.IDs.append(self.tools.create_image(140,60,image=photoImages[-1]))
        self.tools.create_text(140,85,text='Resize',fill='#888888',font=('Arial',8))

        self.image = Image.open('Resources/rotateL.png')
        photoImages.append(ImageTk.PhotoImage(self.image))
        self.IDs.append(self.tools.create_image(190,60,image=photoImages[-1]))
        self.tools.create_text(190,85,text='Rotate',fill='#888888',font=('Arial',8))

        self.image = Image.open('Resources/addL.png')
        photoImages.append(ImageTk.PhotoImage(self.image))
        self.IDs.append(self.tools.create_image(40,130,image=photoImages[-1]))
        self.tools.create_text(40,160,text='Add',fill='#888888',font=('Arial',8))
        self.tools.tag_bind(self.IDs[-1],'<ButtonRelease-1>',lambda e: drawingRoot.drawer(500,400,self.meta))

        self.image = Image.open('Resources/removeL.png')
        photoImages.append(ImageTk.PhotoImage(self.image))
        self.IDs.append(self.tools.create_image(90,130,image=photoImages[-1]))
        self.tools.create_text(90,160,text='Remove',fill='#888888',font=('Arial',8))

        self.image = Image.open('Resources/copyL.png')
        photoImages.append(ImageTk.PhotoImage(self.image))
        self.IDs.append(self.tools.create_image(140,130,image=photoImages[-1]))
        self.tools.create_text(140,160,text='Duplicate',fill='#888888',font=('Arial',8))

        image = Image.open('Resources/importL.png')
        photoImages.append(ImageTk.PhotoImage(image))
        self.IDs.append(self.tools.create_image(190,130,image=photoImages[-1]))
        self.tools.create_text(190,160,text='Import',fill='#888888',font=('Arial',8))
        self.tools.tag_bind(self.IDs[-1],'<ButtonRelease-1>',lambda e: self.import_layer())

        self.layers_labels = []

        self.root.mainloop()

    def redraw(self):
        for i in self.layers_labels:
            i.grid_forget()
        for i in range(len(self.meta.layers)):
            self.layers_labels.append(self.meta.layers[i].get_canvas())
            self.layers_labels[-1].grid()
        for i in range(len(self.meta.layers)-1,-1,-1):
            self.IDs.append(ImageTk.PhotoImage(self.meta.layers[i].get_im()))
            self.canvas.create_image(self.meta.layers[i].x, self.meta.layers[i].y, image=self.IDs[-1])

    def import_layer(self):
        file = tkFileDialog.askopenfilename(initialdir="C:/python27", title="Import",
                                     filetypes=(("Image files", "*.jpg;*.jpeg;*.png;*.bmp"), ("all files", "*.*")))
        if file:
            self.meta.add_layer(Image.open(file))
application = Main()