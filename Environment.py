class Environment:
    
    def __init__(self):
        
        # Key:
        # Types is an array that can have length more than 1 in the case of cards such as
        # witch: ['action', 'attack']
        
        self.card_map = {
            'copper': {'cost': 0, 'coin': 1, 'vp': 0, 'types': ['coin'], 'supply': 45},
            'silver': {'cost': 3, 'coin': 2, 'vp': 0, 'types': ['coin'], 'supply': 30},
            'gold': {'cost': 6, 'coin': 3, 'vp': 0, 'types': ['coin'], 'supply': 30},
            'estate': {'cost': 2, 'coin': 0, 'vp': 1, 'types': ['victory'], 'supply': 8},
            'duchy': {'cost': 5, 'coin': 0, 'vp': 3, 'types': ['victory'], 'supply': 8},
            'province': {'cost': 8, 'coin': 0, 'vp': 6, 'types': ['victory'], 'supply': 8},
            'curse': {'cost': 0, 'coin': 0, 'vp': -1, 'types': ['victory'], 'supply': 8}
        }      
        
    def check_win(self):
        # Returns True if the game is over, and False otherwise
        
        if self.card_map['province'] == 0:
            return True
        else:
            count = 0
            for card in self.card_map.keys():
                if self.card_map[card]['supply'] == 0:
                    count += 1
            if count > 2:
                return True
            else:
                return False