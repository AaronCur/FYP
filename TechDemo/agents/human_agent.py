import math
class HumanAgent():
    def __init__(self):
        self.tag = "Human"
        
    def makeMove(self,event, squaresize):
        posX = event.pos[0]
        return int(math.floor(posX/squaresize))

    def getTag(self):
        return self.tag