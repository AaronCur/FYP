import random

class RandomAgent():
    def __init__(self):
        self.tag = "Random"
        self.description = self.tag
    def makeMove(self, cc):
        return random.randint(0, cc-1)

    def getTag(self):
        return self.tag
    
    def getDescription(self):
        return self.description
