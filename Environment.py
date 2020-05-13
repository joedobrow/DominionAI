class Environment:
    
    def __init__(self):
        
        # Key:
        # Types is an array that can have length more than 1 in the case of cards such as
        # witch: ['action', 'attack']
        
        self.reset_supply()     
        
    def check_win(self):
        # Returns True if the game is over, and False otherwise
        
        if self.card_map['province']['supply'] == 0:
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

    def reset_supply(self):

        self.card_map = {
            'copper': {'cost': 0, 'coin': 1, 'vp': 0, 'types': ['coin'], 'supply': 45, 'start_supply': 45},
            'silver': {'cost': 3, 'coin': 2, 'vp': 0, 'types': ['coin'], 'supply': 30, 'start_supply': 30},
            'gold': {'cost': 6, 'coin': 3, 'vp': 0, 'types': ['coin'], 'supply': 30, 'start_supply': 30},
            'estate': {'cost': 2, 'coin': 0, 'vp': 1, 'types': ['victory'], 'supply': 8, 'start_supply': 8},
            'duchy': {'cost': 5, 'coin': 0, 'vp': 3, 'types': ['victory'], 'supply': 8, 'start_supply': 8},
            'province': {'cost': 8, 'coin': 0, 'vp': 6, 'types': ['victory'], 'supply': 8, 'start_supply': 8},
            'curse': {'cost': 0, 'coin': 0, 'vp': -1, 'types': ['victory'], 'supply': 10, 'start_supply': 10},
            'chapel': {'cost': 2, 'coin': 0, 'vp': 0, 'types': ['action'], 'supply': 10, 'start_supply': 10},
            'gardens': {'cost': 4, 'coin': 0, 'vp': 0, 'types': ['victory'], 'supply': 8, 'start_supply': 8},
            'moneylender': {'cost': 4, 'coin': 0, 'vp': 0, 'types': ['action'], 'supply': 10, 'start_supply': 10},
            'remodel': {'cost': 4, 'coin': 0, 'vp': 0, 'types': ['action'], 'supply': 10, 'start_supply': 10},
            # TEMPORARILY BANNED 'smithy': {'cost': 4, 'coin': 0, 'vp': 0, 'types': ['action'], 'supply': 10, 'start_supply': 10},
            'village': {'cost': 3, 'coin': 0, 'vp': 0, 'types': ['action'], 'supply': 10, 'start_supply': 10},
            'witch': {'cost': 5, 'coin': 0, 'vp': 0, 'types': ['action', 'attack'], 'supply': 10, 'start_supply': 10},
        }    