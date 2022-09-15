from random import randint
class Block:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.color = color
        self.setblock()
    
    def setblock(self):
        self.x = randint(50, 800)
        self.y = randint(100, 150)
        self.id = self.canvas.create_rectangle(0+self.x,0+self.y,150+self.x,60+self.y,fill=self.color, tag="Block")


            
