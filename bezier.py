import Tkinter

def linearSegment(x1,y1,x2,y2,n):
    x=[None]*(n+1)
    y=[None]*(n+1)
    x[0],y[0],x[n],y[n]=x1,y1,x2,y2
    for i in range(1,n):
        xp=(i*x2+(n-i)*x1)/n
        yp=(i*y2+(n-i)*y1)/n
        x[i]=xp
        y[i]=yp
    return (x,y)

def bezierQ(x1,y1,x2,y2,cx,cy,n):
    q1 = linearSegment(x1,y1,cx,cy,n)
    q2 = linearSegment(cx,cy,x2,y2,n)
    xq = [None]*(n+1)
    yq = [None]*(n+1)
    xq[0],yq[0],xq[n],yq[n]= x1,y1,x2,y2
    for i in range(1,n):
        xq[i]=(i*q2[0][i]+(n+1-i)*q1[0][i])/(n+1)
        yq[i]=(i*q2[1][i]+(n+1-i)*q1[1][i])/(n+1)
    return (xq,yq)

def draw(x1,y1,x2,y2,cx,cy):
    global wnd
    global c
    n  = int(((x2-x1)**2+(y2-y1)**2)**0.5)
    points = []
    xq,yq = bezierQ(x1,y1,x2,y2,cx,cy,n)
    for i in range(n+1):
        points.append(xq[i])
        points.append(yq[i])
    curve = c.create_line(points)
    return curve

def showCurve(event):
    global c
    global state
    global curve
    global coord
    if state==2 or state==3:
        c.delete(curve)
        coord[4]=event.x
        coord[5]=event.y
        curve = draw(coord[0],coord[1],coord[2],coord[3],coord[4],coord[5])
        if state==2: state += 1

def drawCurve(event):
    global state
    global coord
    global curve
    if state ==3:
        coord[4]=event.x
        coord[5]=event.y
        draw(coord[0],coord[1],coord[2],coord[3],coord[4],coord[5])
        state=0
        coord=[0]*6

def getCoord(event):
    global state
    global coord
    global curve
    if state ==0:
        coord[0]=event.x
        coord[1]=event.y
        state+=1
    elif state ==1:
        coord[2]=event.x
        coord[3]=event.y
        state+=1
            
curve = None
state = 0
coord = [0]*6
wnd = Tkinter.Tk()
wnd.geometry("400x400")
wnd.title("Bezier")
c = Tkinter.Canvas(wnd,background="white",width=400,height=400)
c.bind("<Button-1>",getCoord)
c.bind("<B1-Motion>",showCurve)
c.bind("<ButtonRelease-1>",drawCurve)
c.pack()
wnd.mainloop()
