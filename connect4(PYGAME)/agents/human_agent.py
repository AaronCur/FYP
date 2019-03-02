class HumanAgent():
    def __init__(self):
         self.tag = "Human"

    def makeMove(self, cc):
        return random.randint(0, cc-1)

    def getName(self):
        return self.tag