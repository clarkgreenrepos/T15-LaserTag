class Player:
    def __init__(self, ID, Codename, EqpID, Team):
        self.ID = ID
        self.Codename = Codename
        self.EqpID = EqpID
        self.Team = Team
        self.Score = 0
        self.Base = False
    def printPlayer(self):
        print(self.ID)
        print(self.Codename)
        print(self.EqpID)
        print(self.Team)
        print(self.Score)
        print(self.Base)
        print("\n")
        
        