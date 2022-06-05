from gameObject import GameObject

class Map(GameObject):
    
    def __init__(self):
        super().__init__(0,0)
        self.filePath = "./map.txt"
        self.mapKey = {"wall": "#", "air": ".", "player": "$", "end": "@"}