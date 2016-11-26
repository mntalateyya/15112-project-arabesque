#   Main Program
#   Code designed by: Mohammed Nurul Hoque (andrewID: mnurulho)
#
#   15-112: Principles of Programming and Computer Science at Carnegie Mellon University in Qatar
#   Term Project
#
#   File created on: Wednesday 2nd of November 2016, 12:14 PM
#   Modification History
#   Start:          End:
#   18/11/16 19:00  18/11/16 19:48
#   18/11/16 20:30  18/11/16 21:46
#`  19/11/16 20:25  19/11/16 23:00
#   20/11/16 12:30  20/11/16 13:30
#   20/11/16 18;30  20/11/16 19:15
#   23/11/16 20:15  20/11/16 22:15
#   25/11/16 15:15  25/11/16 16:45
#   26/11/16 10:30  26/11/16 10:40

# This is the main window of the program

from Tkinter import *
import tkFileDialog
from PIL import Image, ImageTk, ImageDraw
import MainMeta
import templates
import drawingRoot
import ResizeRotate

#create window
class Main:
    def __init__(self):
        # create the window
        self.root = Tk()
        x = self.root.winfo_screenwidth()
        y = self.root.winfo_screenheight()
        s = '900x660+'+str(x/2-450)+'+'+str(y/2-330)
        self.root.geometry(s)
        self.root.resizable(width=False,height=False)
        self.root.iconbitmap('Resources/icon.ico')
        self.root.title('Arabesque Studio')
        self.meta = MainMeta.Meta(self)

        # the welcome window
        welcome = Toplevel()
        welcome.overrideredirect(1)
        s = '400x475+'+str(x/2-200)+'+'+str(y/2-237)
        welcome.geometry(s)
        canvas = Canvas(welcome,width=400,height=475)
        canvas.pack()
        pic = ImageTk.PhotoImage(Image.open('Resources/welcome.png'))
        canvas.create_image(0,0,image=pic,anchor=NW)
        welcome.grab_set()
        welcome.after(800,lambda : welcome.destroy())

        # put framws to organize widgets
        self.IDs= []
        photoImages = []
        # Layout using nested frames
        self.frame1 = Frame(self.root,width=640)
        self.frame2 = Frame(self.root, width=235)
        self.frame1.grid(sticky=NW)
        self.frame2.grid(row=0, column=1, sticky=NW)

        # The main canvas
        self.canvas = Canvas(self.frame1,width=620,height=620,bg='#ffffff',bd=1, cursor='fleur')
        self.canvas.config(scrollregion=(0,0,620,620))
        self.canvas.grid(padx=10,pady=10)

        self.canvas.config(highlightbackground='#00a2e8')

        # first tools canvas
        self.metaTools = Canvas(self.frame2, width=235, height=60, bg='#ffffff')
        self.metaTools.grid(pady=10)
        self.tools = Canvas(self.frame2, width=235, height=175, bg='#ffffff')
        self.tools.grid(sticky=NW,pady=5)

        self.metaTools.config(highlightbackground='#00a2e8')
        self.tools.config(highlightbackground='#00a2e8')

        # second tools canvas
        self.tools.create_rectangle(2,2,237,30,width=0,fill='#00a2e8')
        self.tools.create_text(117,15,text='Layers',fill='white',font=('Arial',12))

        # place the icons and bind them to their functions

        # export
        self.image = Image.open('Resources/export.png')
        photoImages.append(ImageTk.PhotoImage(self.image))
        self.IDs.append(self.metaTools.create_image(60,25,image=photoImages[-1]))
        self.metaTools.create_text(60,50,text='Export',fill='#888888',font=('Arial',8))
        self.metaTools.tag_bind(self.IDs[-1], '<ButtonRelease-1>', lambda e, id = self.IDs[-1]: self.export())
        self.metaTools.tag_bind(self.IDs[-1], '<Button-1>',
                                lambda e, id = self.IDs[-1]:self.flash(self.metaTools,id,'export'))
        #clear
        self.image = Image.open('Resources/clear.png')
        photoImages.append(ImageTk.PhotoImage(self.image))
        self.IDs.append(self.metaTools.create_image(120, 25, image=photoImages[-1]))
        self.metaTools.create_text(120, 50, text='Clear', fill='#888888', font=('Arial', 8))
        self.metaTools.tag_bind(self.IDs[-1], '<ButtonRelease-1>', lambda e, id=self.IDs[-1]: self.clear())
        self.metaTools.tag_bind(self.IDs[-1], '<Button-1>',
                                lambda e, id=self.IDs[-1]: self.flash(self.metaTools, id,'clear'))
        # move
        self.image = Image.open('Resources/moveL.png')
        photoImages.append(ImageTk.PhotoImage(self.image))
        self.IDs.append(self.tools.create_image(55,60,image=photoImages[-1]))
        self.tools.create_text(55,85,text='Move',fill='#888888',font=('Arial',8))
        self.tools.tag_bind(self.IDs[-1], '<Button-1>',
                                lambda e, id=self.IDs[-1]:self.flash(self.tools, id, 'moveL'))
        #rotate
        self.image = Image.open('Resources/rotateL.png')
        photoImages.append(ImageTk.PhotoImage(self.image))
        self.IDs.append(self.tools.create_image(118, 60, image=photoImages[-1]))
        self.tools.create_text(118, 85, text='Rotate', fill='#888888', font=('Arial', 8))
        self.tools.tag_bind(self.IDs[-1], '<ButtonRelease-1>',
                            lambda e: ResizeRotate.Rotate(self) if len(self.meta.layers)>0 else 0)
        self.tools.tag_bind(self.IDs[-1], '<Button-1>',
                                lambda e, id=self.IDs[-1]:self.flash(self.tools, id, 'rotateL'))
        # resize
        self.image = Image.open('Resources/resizeL.png')
        photoImages.append(ImageTk.PhotoImage(self.image))
        self.IDs.append(self.tools.create_image(180,60,image=photoImages[-1]))
        self.tools.create_text(180,85,text='Resize',fill='#888888',font=('Arial',8))
        self.tools.tag_bind(self.IDs[-1], '<ButtonRelease-1>',
                            lambda e: ResizeRotate.Resize(self) if len(self.meta.layers)>0 else 0)
        self.tools.tag_bind(self.IDs[-1], '<Button-1>',
                                lambda e, id=self.IDs[-1]:self.flash(self.tools, id, 'resizeL'))

        # edit layer
        self.image = Image.open('Resources/pen.png')
        photoImages.append(ImageTk.PhotoImage(self.image))
        self.IDs.append(self.tools.create_image(55,130,image=photoImages[-1]))
        self.tools.create_text(55,160,text='Edit',fill='#888888',font=('Arial',8))
        self.tools.tag_bind(self.IDs[-1], '<ButtonRelease-1>', lambda e: self.edit_layer())
        self.tools.tag_bind(self.IDs[-1], '<Button-1>',
                                lambda e, id=self.IDs[-1]:self.flash(self.tools, id, 'pen'))

        # add layer
        self.image = Image.open('Resources/addL.png')
        photoImages.append(ImageTk.PhotoImage(self.image))
        self.IDs.append(self.tools.create_image(118,130,image=photoImages[-1]))
        self.tools.create_text(118,160,text='Add',fill='#888888',font=('Arial',8))
        self.tools.tag_bind(self.IDs[-1],'<ButtonRelease-1>',
                            lambda e:templates.template(self) if len(self.meta.layers)<5 else 0)
        self.tools.tag_bind(self.IDs[-1], '<Button-1>',
                                lambda e, id=self.IDs[-1]:self.flash(self.tools, id, 'addL'))
        # import from file
        image = Image.open('Resources/importL.png')
        photoImages.append(ImageTk.PhotoImage(image))
        self.IDs.append(self.tools.create_image(180,130,image=photoImages[-1]))
        self.tools.create_text(180,160,text='Import',fill='#888888',font=('Arial',8))
        self.tools.tag_bind(self.IDs[-1],'<ButtonRelease-1>',lambda e: self.import_layer())
        self.tools.tag_bind(self.IDs[-1], '<Button-1>',
                                lambda e, id=self.IDs[-1]:self.flash(self.tools, id, 'importL'))

        self.layers_labels = []

        # move layer when mouse dragged on canvas
        self.canvas.bind('<Button-1>', lambda e: self.to_move(e))
        self.canvas.bind('<B1-Motion>',lambda e: self.move_layer(e))

        self.root.mainloop()

    # this function redraws the canvas and the layers' labels
    def redraw(self):
        self.canvas.delete('all')  # delete previous
        for i in self.layers_labels:  # remove layers' labels
            i.grid_forget()
        for i in range(len(self.meta.layers)):  # redraw llayers' labels
            self.layers_labels.append(self.meta.layers[i].get_canvas())
            self.meta.layers[i].redraw()
            self.layers_labels[-1].grid(pady=2)
        # create an image combining images of all layers
        image = Image.new('RGBA',(620,620),'#ffffff00')
        for i in range(len(self.meta.layers)-1,-1,-1):
            image.paste(self.meta.layers[i].get_im(),
                        (self.meta.layers[i].x, self.meta.layers[i].y),self.meta.layers[i].get_im())

        # deactivate invalid commands on layers
        if self.meta.layers:
            self.meta.layers[0].config_first()
            self.meta.layers[-1].config_last()
        # draw image on canvas
        self.meta.image = image
        self.IDs.append(ImageTk.PhotoImage(self.meta.image))
        self.canvas.create_image(0,0,anchor=NW, image=self.IDs[-1])

    # imports a layer from  an existing file
    def import_layer(self):
        if len(self.meta.layers)<5:
            file = tkFileDialog.askopenfilename(title="Import",
                                         filetypes=(("Image files", "*.jpg;*.jpeg;*.png;*.bmp"), ("all files", "*.*")))
            if file:
                image = Image.open(file)
                image.putalpha(255)
                if image.size[0]>620 or image.size[1]>620:  # resize over-sized images
                    image = image.resize((620,620))
                self.meta.add_layer(image,'F')

    # save current state to prepare for motion
    def to_move(self,e):
        if self.meta.layers:
            self.e_from_x = e.x
            self.e_from_y = e.y
            self.im_x = self.meta.focus_layer.x
            self.im_y = self.meta.focus_layer.y

    # move a layer
    def move_layer(self,e):
        if self.meta.layers:
            # relative motion of mouse
            delta_x = e.x - self.e_from_x
            delta_y = e.y - self.e_from_y
            # append coordinates
            self.meta.focus_layer.x = self.im_x + delta_x
            self.meta.focus_layer.y = self.im_y + delta_y
            self.redraw() #draw again
            self.meta.change_focus(self.meta.focus_layer) # set highlight to current layre

    # rotate a layer
    def rotate_layer(self,angle):
        if self.meta.layers:
            im = self.meta.focus_layer.get_im()
            im = im.rotate(angle,expand=True)
            self.meta.focus_layer.set_im(im)  # change image of layer
            self.redraw()

    # rsize a layer
    def resize_layer(self,x,y):
        if self.meta.layers:
            im = self.meta.focus_layer.get_im()
            w,h = im.size
            # flip image for negative inouts
            if x<0:
                im = im.transpose(Image.FLIP_LEFT_RIGHT)
                x = -x
            if y<0:
                im = im.transpose(Image.FLIP_TOP_BOTTOM)
                y= - y

            im = im.resize((int(w*x),int(h*y)),Image.ANTIALIAS)
            self.meta.focus_layer.set_im(im)  # change image of layer
            self.redraw()

    # edit a layer
    def edit_layer(self):
        if self.meta.layers:
            # start a drawing window
            drawingRoot.drawer(self.meta.focus_layer.widthO,self.meta.focus_layer.heightO,self.meta,
                               self.meta.focus_layer.mode,self.meta.focus_layer.image,self.meta.focus_layer)

    # export to file
    def export(self):
        path = tkFileDialog.asksaveasfilename(defaultextension='.png',
                                       filetypes=(("PNG file", "*.png"),('JPEG file','*.jpeg;'),("all files", "*.*")),
                                       title='Save as'
                                       )
        if path:
            self.meta.image.save(path)

    # delete all layers
    def clear(self):
        self.meta.layers = []
        self.redraw()

    # causes an icon to blink when clicked
    def flash(self,c,id, string, repeat=0):
        if not repeat:
            # change image to blinking image and
            self.IDs.append(ImageTk.PhotoImage(Image.open('Resources/' + string + '_.png')))
            c.itemconfig(id, image=self.IDs[-1])
            c.after(200, lambda: self.flash(c,id, string, 1))
        else:
            # return to normal
            self.IDs.append(ImageTk.PhotoImage(Image.open('Resources/' + string + '.png')))
            c.itemconfig(id, image=self.IDs[-1])

# start the application
if __name__ == '__main__':
    application = Main()