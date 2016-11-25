#   Eraser module
#   Code designed by: Mohammed Nurul Hoque (andrewID: mnurulho)
#
#   15-112: Principles of Programming and Computer Science at Carnegie Mellon University in Qatar
#   Term Project
#
#   File created on: Wednesday 23 of November 2016, 09:03 PM
#   Modification History
#   Start:          End:
#   23/11/16 09:03  23/11/16 09:25
#   24/11/16 09:20  24/11/16 09:27

from PIL import ImageDraw

# this module provides an eraser tool to a canvas using a MetaResources object

# A helper object to manage variables
class HelperObject:
    def __init__(self):
        # store last position of mouse
        self.x = None
        self.y = None

    def clear(self,c):
        # reset
        self.x = None
        self.y = None

def move(e,helper,meta):
    print '$$'
    # movement begin
    if helper.x is None:
        # set position
        helper.x, helper.y = e.x, e.y
        return

    # for subsequent movements, draw a white transparent line from last postion
    # to currrent positions
    image = meta.get_image()
    draw = ImageDraw.Draw(image)
    draw.line((helper.x,helper.y,e.x,e.y),fill='#ffffff00',width=int(meta.get_width())*2)
    meta.draw(image)
    # set coordinates for next movement
    helper.x, helper.y = e.x, e.y

# activate tool
def activate(meta):
    print 'act'
    # create helper object and bind canvas items to tool's methods
    helper = HelperObject()
    meta.canvas.bind('<B1-Motion>', lambda e: move(e, helper,meta))
    meta.canvas.bind('<ButtonRelease-1>', lambda e: helper.clear(0))  # reset when mouse released
    return helper
