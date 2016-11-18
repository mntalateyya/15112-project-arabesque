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
from PIL import Image, ImageTk
import drawingRoot

#create window
root = Tk()
root.geometry('900x600')
root.resizable(width=False,height=False)
root.iconbitmap('Resources/icon.ico')

IDs= []
photoImages = []
# Layout using nested frames
canvas = Canvas(root,width=640,height=540,bg='#ffffff')
canvas.config(scrollregion=(0,0,640,540))
tools = Canvas(root, width=235,height = 600,bg='#ffffff')
canvas.grid(row=0,column=0,padx=10,pady=20,ipadx=0,ipady=0)
tools.grid(row=0,column=1,)

canvas.create_rectangle(0,0,639,539,outline='#00a2e8')
tools.create_line(2,2,2,600,fill='#00a2e8')

tools.create_rectangle(2,60,236,90,width=0,fill='#00a2e8')
tools.create_text(117,75,text='Layers',fill='white',font=('Arial',12))

image = Image.open('Resources/export.png')
photoImages.append(ImageTk.PhotoImage(image))
IDs.append(tools.create_image(83,25,image=photoImages[-1]))
tools.create_text(83,50,text='Export',fill='#888888',font=('Arial',8))

image = Image.open('Resources/clear.png')
photoImages.append(ImageTk.PhotoImage(image))
IDs.append(tools.create_image(151,25,image=photoImages[-1]))
tools.create_text(151,50,text='Clear',fill='#888888',font=('Arial',8))

image = Image.open('Resources/pen.png')
photoImages.append(ImageTk.PhotoImage(image))
IDs.append(tools.create_image(40,130,image=photoImages[-1]))
tools.create_text(40,155,text='Edit',fill='#888888',font=('Arial',8))

image = Image.open('Resources/moveL.png')
photoImages.append(ImageTk.PhotoImage(image))
IDs.append(tools.create_image(90,130,image=photoImages[-1]))
tools.create_text(90,155,text='Move',fill='#888888',font=('Arial',8))

image = Image.open('Resources/resizeL.png')
photoImages.append(ImageTk.PhotoImage(image))
IDs.append(tools.create_image(140,130,image=photoImages[-1]))
tools.create_text(140,155,text='Resize',fill='#888888',font=('Arial',8))

image = Image.open('Resources/rotateL.png')
photoImages.append(ImageTk.PhotoImage(image))
IDs.append(tools.create_image(190,130,image=photoImages[-1]))
tools.create_text(190,155,text='Rotate',fill='#888888',font=('Arial',8))

image = Image.open('Resources/addL.png')
photoImages.append(ImageTk.PhotoImage(image))
IDs.append(tools.create_image(40,190,image=photoImages[-1]))
tools.create_text(40,215,text='Add',fill='#888888',font=('Arial',8))

image = Image.open('Resources/removeL.png')
photoImages.append(ImageTk.PhotoImage(image))
IDs.append(tools.create_image(90,190,image=photoImages[-1]))
tools.create_text(90,215,text='Remove',fill='#888888',font=('Arial',8))

image = Image.open('Resources/copyL.png')
photoImages.append(ImageTk.PhotoImage(image))
IDs.append(tools.create_image(140,190,image=photoImages[-1]))
tools.create_text(140,215,text='Duplicate',fill='#888888',font=('Arial',8))

image = Image.open('Resources/importL.png')
photoImages.append(ImageTk.PhotoImage(image))
IDs.append(tools.create_image(190,190,image=photoImages[-1]))
tools.create_text(190,215,text='Import',fill='#888888',font=('Arial',8))

drawCanvas = drawingRoot.drawer(500,400)
root.mainloop()