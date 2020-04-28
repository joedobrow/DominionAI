import random

class RandBot:
    
    def __init__(self):
        
        self.name = "RandBot"
    
    def get_moves(self, env, deck, hand, discard):
        
            
        money = hand[0] + hand[1] * 2 + hand[2] * 3
        moves = []
        for i in range(7):
            if money >= env.money_map[i]:
                moves.append(i)
        
        for _ in range(100):
            
            move = random.choice(moves)
            if env.card_counts[move] > 0:
                return move
            
        # indicates an error    
        return -1
