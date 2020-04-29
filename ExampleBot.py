import random

class ExampleBot:
    
    def __init__(self):
        
        self.name = "RandBot"
    
    def get_moves(self, env, deck, hand, discard):
        
            
        money = hand['copper'] + hand['silver'] * 2 + hand['gold'] * 3
        moves = []
        for card in env.card_map.keys():
            if (money >= env.card_map[card]['cost']) and env.card_map[card]['supply'] > 0:
                moves.append(card)
           
        try:
            move = random.choice(moves)
            return move
        except: 
            # indicates an error  
            print('error 1')  
            return -1