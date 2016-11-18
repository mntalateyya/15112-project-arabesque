from Tkinter import *
from PIL import Image,ImageTk

class ColorPicker:
    def __init__(self,master):
        self.root = Toplevel()
        self.root.resizable(width=False, height=False)
        self.canvas = Canvas(self.root,bg='white', width=400,height=270)
        self.canvas.pack()
        self.red,self.green,self.blue = [255]*3
        self.color = '#ffffff'
        self.colorBox = self.canvas.create_rectangle(310,120,390,200,outline = '#00a2e8', fill = self.color)
        self.ok = ImageTk.PhotoImage(Image.open('Resources/ok.png'))
        okButton = self.canvas.create_image(350,235,image=self.ok)
        self.canvas.tag_bind(okButton,'<ButtonRelease-1>',lambda e: OKColor(self.color,self,master))

        colors = []
        for i in [0,64,128,255]:
            for j in [0,64,128,255]:
                for k in [0,64,128,255]:
                    colors.append((i,j,k))
        i = 0
        for y in [0,1,2,3]:
            for x in range(16):
                color = '#'+hex(colors[i][0])[2:].rjust(2,'0')+hex(colors[i][1])[2:].rjust(2,'0')+hex(colors[i][2])[2:].rjust(2,'0')
                box = self.canvas.create_rectangle(x*25+5,y*25+2,x*25+25,y*25+22,fill=color,outline='#00a2e8')
                self.canvas.tag_bind(box,'<Button-1>',lambda e,i=i: self.changeColor(colors[i]))
                i+=1
        self.redLabels = [0]*17
        self.greenLabels = [0] * 17
        self.blueLabels = [0] * 17

        self.canvas.create_text(20,145,text='R')
        for i in range(17):
            color = '#'+hex(i*16 if i<16 else 255)[2:].rjust(2,'0')+hex(self.green)[2:].rjust(2,'0')+hex(self.blue)[2:].rjust(2,'0')
            self.redLabels[i] = self.canvas.create_rectangle(i*15+40,140,i*15+52,152,outline='#00a2e8',fill=color)
            self.canvas.tag_bind(self.redLabels[i],'<Button-1>',lambda e, i=i: self.changeColor((i*16 if i<16 else 255,self.green,self.blue)))
        self.canvas.create_text(20, 185, text='G')
        for i in range(17):
            color = '#'+hex(self.red)[2:].rjust(2,'0')+hex(i*16 if i<16 else 255)[2:].rjust(2,'0')+hex(self.blue)[2:].rjust(2,'0')
            self.greenLabels[i] = self.canvas.create_rectangle(i * 15 + 40, 180, i * 15 + 52, 192, outline='#00a2e8',fill=color)
            self.canvas.tag_bind(self.greenLabels[i],'<Button-1>',lambda e, i=i: self.changeColor((self.red,i*16 if i<16 else 255,self.blue)))
        self.canvas.create_text(20, 225, text='B')
        for i in range(17):
            color = '#'+hex(self.red)[2:].rjust(2,'0')+hex(self.green)[2:].rjust(2,'0')+hex(i*16 if i<16 else 255)[2:].rjust(2,'0')
            self.blueLabels[i] = self.canvas.create_rectangle(i*15+40,220,i*15+52,232,outline='#00a2e8',fill = color)
            self.canvas.tag_bind(self.blueLabels[i],'<Button-1>',lambda e, i=i: self.changeColor((self.red,self.green,i*16 if i<16 else 255)))

    def changeColor(self,color):
        self.red = color[0]
        self.green = color[1]
        self.blue = color[2]
        self.color = '#'+hex(color[0])[2:].rjust(2,'0')+hex(color[1])[2:].rjust(2,'0')+hex(color[2])[2:].rjust(2,'0')
        for i in range(17):
            color = '#'+hex(i*16 if i<16 else 255)[2:].rjust(2,'0')+hex(self.green)[2:].rjust(2,'0')+hex(self.blue)[2:].rjust(2,'0')
            self.canvas.itemconfig(self.redLabels[i],fill=color)
        for i in range(17):
            color = '#'+hex(self.red)[2:].rjust(2,'0')+hex(i*16 if i<16 else 255)[2:].rjust(2,'0')+hex(self.blue)[2:].rjust(2,'0')
            self.canvas.itemconfig(self.greenLabels[i], fill=color)
        for i in range(17):
            color = '#'+hex(self.red)[2:].rjust(2,'0')+hex(self.green)[2:].rjust(2,'0')+hex(i*16 if i<16 else 255)[2:].rjust(2,'0')
            self.canvas.itemconfig(self.blueLabels[i], fill=color)
        self.canvas.itemconfig(self.colorBox,fill = self.color)

def OKColor(color,window,master):
    window.root.destroy()
    master.changeColor(color)