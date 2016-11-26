#   Pencil module
#   Code designed by: Mohammed Nurul Hoque (andrewID: mnurulho)
#
#   15-112: Principles of Programming and Computer Science at Carnegie Mellon University in Qatar
#   Term Project
#
#   File created on: Sunday 13th of November 2016, 7:30 PM
#   Modification History
#   Start:          End:
#   13/11/16 19:30  13/11/16 20:00
#   26/11/16 10:55  26/11/16 11:05

from PIL import ImageDraw

# This module provides a free drawing pencil to a canvas


# This is a helper class to share data
class helperObject:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.linesIDs = []  # references of Tkinter lines IDs
        self.linesLoci = []  # tuples of coordinates
    def clear(self,c):
        for i in self.linesIDs:
            c.delete(i)

# when mouse clicked save current position to starting coordinates
def press(e,helper):
    helper.x = e.x
    helper.y = e.y
    helper.linesLoci.append([e.x,e.y])

# when mouse moved draw a line tracing motion from starting position
# then change starting position to current position for the next line segment
def move(e,helper,meta):
    if e.x != helper.x or e.y != helper.y:
        helper.linesIDs.append(meta.canvas.create_line(helper.x, helper.y, e.x,e.y,fill=meta.get_color(),
                                                       width = int(meta.get_width())))
        helper.linesLoci[-1].append(e.x)
        helper.linesLoci[-1].append(e.y)
    helper.x, helper.y = e.x,e.y

# when mouse released remove Tkinter canvas lines, append the line to image in meta object and
# push new image to canvas
def release(helper,meta):
    image = meta.get_image()
    draw = ImageDraw.Draw(image)
    # draw a line of through all saved coordinates
    for i in helper.linesLoci:
        draw.line(i,fill=meta.get_color(),width = int(meta.get_width()))
    meta.draw(image)  # push to canvas
    # remove canvas lines
    for i in helper.linesIDs:
        meta.canvas.delete(i)
    # reset
    helper.linesIDs = []
    helper.linesLoci = []

# activate the tool and bind canvas events to tool's functions
def activate(meta):
    helper = helperObject()
    meta.canvas.bind('<Button-1>',lambda e: press(e,helper))
    meta.canvas.bind('<B1-Motion>', lambda e: move(e, helper,meta))
    meta.canvas.bind('<ButtonRelease-1>', lambda e: release(helper,meta))
    return helper
