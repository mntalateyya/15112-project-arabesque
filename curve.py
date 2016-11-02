#   02/11/16 12:14   02/11/16 12:31
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

class Curve:
    def __init__(self,x1,y1,x2,y2,anchor1=None,anchor2=None):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        if anchor1 != None:
            self.anchor1x = anchor1[0]
            self.anchor1y = anchor1[1]
        else:
            self.anchor1x = x1
            self.anchor1y = y1
        if anchor2 != None:
            self.anchor2x = anchor2[0]
            self.anchor2y = anchor2[1]
        else:
            self.anchor2x = x2
            self.anchor2y = y2
        self.draw = None
        
    def getPoint1(self):
        return self.x1,self.y1
    def getPoint2 (self):
        return self.x2,self.y2
    def getAnchor1(self):
        return self.anchor1x,self.anchor1y
    def getAnchor2(self):
        return self.anchor2x,self.anchor2y

    def setAnchor1(self,x,y):
        self.anchor1x = x
        self.anchor1y = y
    def setAnchor2(self,x,y):
        self.anchor2x = x
        self.anchor2y = y

    def draw(self,c):
        
