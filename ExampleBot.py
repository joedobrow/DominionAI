import random

class ExampleBot:
    
    def __init__(self):
        
        self.name = "RandBot"
    
    def get_buys(self, game,):
         
        money = hand['copper'] + hand['silver'] * 2 + hand['gold'] * 3

        moves = []
        for card in env.card_map.keys():
            if (money >= env.card_map[card]['cost']) and env.card_map[card]['supply'] > 0:
                moves.append(card)
           
        return move

    def get_actions(self, env, deck, hand, discard)
        return get_actions

    def remodel()