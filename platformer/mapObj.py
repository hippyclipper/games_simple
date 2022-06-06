from gameObject import GameObject

class Map(GameObject):
    
    def __init__(self):
        super().__init__(0,0)
        self.filePath = "./map.txt"
        self.mapKey = {"wall": "#", "air": ".", "player": "$", "end": "@"}
        self.widthNum = 0
        self.heightNum = 0
        file = open(self.filePath, "r")
        for x in file:
            self.heightNum += 1
            self.widthNum = max(self.widthNum, len(x))
        file.close()
        
        
                                 
            
        
