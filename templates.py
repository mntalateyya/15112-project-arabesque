#   templates module
#   Code designed by: Mohammed Nurul Hoque (andrewID: mnurulho)
#
#   15-112: Principles of Programming and Computer Science at Carnegie Mellon University in Qatar
#   Term Project
#
#   File created on: Sunday 20th of November 2016, 10:00 PM
#   Modification History
#   Start:          End:
#   22:00           23:30

from Tkinter import *
from PIL import Image, ImageTk
import drawingRoot
import math

class template:
    def __init__(self,parent):
        self.root = Toplevel()
        self.root.geometry('310x280')
        self.root.resizable(width=False, height=False)
        self.parent = parent
        self.canvas = Canvas(self.root,width=310, height=280, bg='#e0e0e0')
        self.canvas.pack()
        self.labels,self.rec = [],[]
        self.focus = (None,None)

        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/freeForm.png')))
        self.free = self.canvas.create_image(10,10,anchor=NW, image=self.labels[-1])
        self.rec.append(self.canvas.create_rectangle(10, 10, 100, 100, outline='#cccccc'))
        self.canvas.create_text(55,110,text='Free Form', fill='#00a2e8')
        self.canvas.tag_bind(self.free,'<ButtonRelease-1>',
                             lambda e,i=self.rec[-1] ,temp='free': self.changeFocus(i,temp))
        self.changeFocus(self.rec[-1],'free')

        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/polar.png')))
        self.polar = self.canvas.create_image(110, 10, anchor=NW, image=self.labels[-1])
        self.rec.append(self.canvas.create_rectangle(110, 10, 200, 100, outline='#cccccc'))
        self.canvas.create_text(155, 110, text='Polar', fill='#00a2e8')
        self.canvas.tag_bind(self.polar, '<ButtonRelease-1>',
                             lambda e, i=self.rec[-1], temp='polar': self.changeFocus(i, temp))

        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/polarSymm.png')))
        self.polarS = self.canvas.create_image(210, 10, anchor=NW, image=self.labels[-1])
        self.rec.append(self.canvas.create_rectangle(210, 10, 300, 100, outline='#cccccc'))
        self.canvas.create_text(255, 110, text='Polar Symmetric', fill='#00a2e8')
        self.canvas.tag_bind(self.polarS, '<ButtonRelease-1>',
                             lambda e, i=self.rec[-1], temp='polarS': self.changeFocus(i, temp))

        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/linear.png')))
        self.linear = self.canvas.create_image(60, 130, anchor=NW, image=self.labels[-1])
        self.rec.append(self.canvas.create_rectangle(60, 130, 150, 220, outline='#cccccc'))
        self.canvas.create_text(105, 230, text='Linear', fill='#00a2e8')
        self.canvas.tag_bind(self.linear, '<ButtonRelease-1>',
                             lambda e, i=self.rec[-1], temp='linear': self.changeFocus(i, temp))

        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/linearSymm.png')))
        self.linearS = self.canvas.create_image(160, 130, anchor=NW, image=self.labels[-1])
        self.rec.append(self.canvas.create_rectangle(160, 130, 250, 220, outline='#cccccc'))
        self.canvas.create_text(205, 230, text='Linear Symmetric', fill='#00a2e8')
        self.canvas.tag_bind(self.linearS, '<ButtonRelease-1>',
                             lambda e, i=self.rec[-1], temp='linearS': self.changeFocus(i, temp))

        self.canvas.create_rectangle(0,250,310,280,fill='#f0f0f0', width=0)
        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/OK.png')))
        self.ok = self.canvas.create_image(270,267,image=self.labels[-1])
        self.canvas.tag_bind(self.ok,'<ButtonRelease-1>',lambda e: self.finalize())


        self.canvas.create_text(100,265,text='Number of symmetries: ', fill='#00a2e8')
        self.n = IntVar()
        self.n.set(1)
        self.menu = OptionMenu(self.canvas, self.n, 1,2,4,6,8,12,16)
        self.canvas.create_window(200, 265, window=self.menu)

        self.root.mainloop()

    def finalize(self):
        n = self.n.get()
        self.root.destroy()
        print self.focus
        if self.focus[0]=='free':
            drawingRoot.drawer(620,540,self.parent.meta,'F')
        elif self.focus[0]=='polar':
            if n==1:
                drawingRoot.drawer(620, 540, self.parent.meta, 'F')
            elif n==2:
                drawingRoot.drawer(310, 270, self.parent.meta, 'P#' + str(n))
            else:
                angle = 2*math.pi/n
                width = min((int(310*math.tan(angle)),310))
                print width
                drawingRoot.drawer(width,270,self.parent.meta,'P#'+str(n))
        elif self.focus[0]=='polarS':
            if n==1:
                drawingRoot.drawer(310, 540, self.parent.meta, 'L#S#1')
            elif n==2:
                drawingRoot.drawer(310, 270, self.parent.meta, 'P#S#' + str(n))
            else:
                angle = 2*math.pi/n
                width = min((int(310*math.tan(angle/2)),310))
                print width
                drawingRoot.drawer(width,270,self.parent.meta,'P#S#'+str(n))
        elif self.focus[0]=='linear':
            if n==1:
                drawingRoot.drawer(620, 540, self.parent.meta, 'F')
            else:
                drawingRoot.drawer(620/n, 620/n, self.parent.meta, 'L#' + str(n))
        elif self.focus[0]=='linearS':
            drawingRoot.drawer(310/n, max(620/n,50), self.parent.meta, 'L#S#'+str(n))


    def changeFocus(self,i,temp):
        self.canvas.itemconfig(self.focus[1],outline='#cccccc')
        self.canvas.itemconfig(i,outline='#00a2e8')
        self.focus = (temp,i)
        print self.focus
