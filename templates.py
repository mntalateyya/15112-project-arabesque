#   templates module
#   Code designed by: Mohammed Nurul Hoque (andrewID: mnurulho)
#
#   15-112: Principles of Programming and Computer Science at Carnegie Mellon University in Qatar
#   Term Project
#
#   File created on: Sunday 20th of November 2016, 10:00 PM
#   Modification History
#   Start:          End:
#   20/11/16 22:00  20/11/16 23:30
#   26/11/16 23:25  26/11/16 23:35

# This module crates a window asking the user to select a layer template
# then creates a drawing window with correct size passing the correct mode

from Tkinter import *
from PIL import Image, ImageTk
import drawingRoot
import math

# the class of the tool
class template:
    def __init__(self,parent):
        # create window
        self.root = Toplevel()
        self.root.geometry('310x280')
        self.root.resizable(width=False, height=False)
        self.parent = parent
        self.canvas = Canvas(self.root,width=310, height=280, bg='#e0e0e0')
        self.canvas.pack()
        self.labels,self.rec = [],[]
        self.focus = (None,None)  # the mode that is under focus (rectangle reference, mode string)

        # free form
        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/freeForm.png')))
        self.free = self.canvas.create_image(10,10,anchor=NW, image=self.labels[-1])
        self.rec.append(self.canvas.create_rectangle(10, 10, 100, 100, outline='#cccccc'))
        self.canvas.create_text(55,110,text='Free Form', fill='#00a2e8')
        self.canvas.tag_bind(self.free,'<ButtonRelease-1>',
                             lambda e,i=self.rec[-1] ,temp='free': self.changeFocus(i,temp))
        self.changeFocus(self.rec[-1],'free')

        # simple polar
        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/polar.png')))
        self.polar = self.canvas.create_image(110, 10, anchor=NW, image=self.labels[-1])
        self.rec.append(self.canvas.create_rectangle(110, 10, 200, 100, outline='#cccccc'))
        self.canvas.create_text(155, 110, text='Polar', fill='#00a2e8')
        self.canvas.tag_bind(self.polar, '<ButtonRelease-1>',
                             lambda e, i=self.rec[-1], temp='polar': self.changeFocus(i, temp))

        # symmetric polar
        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/polarSymm.png')))
        self.polarS = self.canvas.create_image(210, 10, anchor=NW, image=self.labels[-1])
        self.rec.append(self.canvas.create_rectangle(210, 10, 300, 100, outline='#cccccc'))
        self.canvas.create_text(255, 110, text='Polar Symmetric', fill='#00a2e8')
        self.canvas.tag_bind(self.polarS, '<ButtonRelease-1>',
                             lambda e, i=self.rec[-1], temp='polarS': self.changeFocus(i, temp))

        # linear
        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/linear.png')))
        self.linear = self.canvas.create_image(60, 130, anchor=NW, image=self.labels[-1])
        self.rec.append(self.canvas.create_rectangle(60, 130, 150, 220, outline='#cccccc'))
        self.canvas.create_text(105, 230, text='Linear', fill='#00a2e8')
        self.canvas.tag_bind(self.linear, '<ButtonRelease-1>',
                             lambda e, i=self.rec[-1], temp='linear': self.changeFocus(i, temp))
        # summetric linear
        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/linearSymm.png')))
        self.linearS = self.canvas.create_image(160, 130, anchor=NW, image=self.labels[-1])
        self.rec.append(self.canvas.create_rectangle(160, 130, 250, 220, outline='#cccccc'))
        self.canvas.create_text(205, 230, text='Linear Symmetric', fill='#00a2e8')
        self.canvas.tag_bind(self.linearS, '<ButtonRelease-1>',
                             lambda e, i=self.rec[-1], temp='linearS': self.changeFocus(i, temp))

        # OK button
        self.canvas.create_rectangle(0,250,310,280,fill='#f0f0f0', width=0)
        self.labels.append(ImageTk.PhotoImage(Image.open('Resources/OK.png')))
        self.ok = self.canvas.create_image(270,267,image=self.labels[-1])
        self.canvas.tag_bind(self.ok,'<ButtonRelease-1>',lambda e: self.finalize())

        # number of symmetries selector
        self.canvas.create_text(100,265,text='Number of symmetries: ', fill='#00a2e8')
        self.n = IntVar()
        self.n.set(1)
        self.menu = OptionMenu(self.canvas, self.n, 1,2,4,6,8,12,16)
        self.canvas.create_window(200, 265, window=self.menu)

        self.root.mainloop()

    # create a drawer class window of the correct geometry
    def finalize(self):
        n = self.n.get()
        self.root.destroy()
        if self.focus[0]=='free':
            drawingRoot.drawer(620,540,self.parent.meta,'F')
        elif self.focus[0]=='polar':
            if n==1:  # same as free
                drawingRoot.drawer(620, 540, self.parent.meta, 'F')
            elif n==2:  # half window
                drawingRoot.drawer(310, 270, self.parent.meta, 'P#' + str(n))
            else:  # the size of rectangle circumscribing the triangle to repeat
                angle = 2*math.pi/n
                width = min((int(310*math.tan(angle)),310))
                drawingRoot.drawer(width,270,self.parent.meta,'P#'+str(n))
        elif self.focus[0]=='polarS':
            if n==1:  # same as linear symm with 1 block
                drawingRoot.drawer(310, 540, self.parent.meta, 'L#S#1')
            elif n==2:  # quarter window
                drawingRoot.drawer(310, 270, self.parent.meta, 'P#S#' + str(n))
            else:  # the size of rectangle circumscribing the triangle to repeat
                angle = 2*math.pi/n
                width = min((int(310*math.tan(angle/2)),310))
                drawingRoot.drawer(width,270,self.parent.meta,'P#S#'+str(n))
        elif self.focus[0]=='linear':
            if n==1:  # same as free
                drawingRoot.drawer(620, 540, self.parent.meta, 'F')
            else:
                drawingRoot.drawer(620/n, 620/n, self.parent.meta, 'L#' + str(n))
        elif self.focus[0]=='linearS':
            drawingRoot.drawer(310/n, max(620/n,50), self.parent.meta, 'L#S#'+str(n))

    # change the mode under focus and highlight its rectangle
    def changeFocus(self,i,temp):
        self.canvas.itemconfig(self.focus[1],outline='#cccccc')
        self.canvas.itemconfig(i,outline='#00a2e8')
        self.focus = (temp,i)
