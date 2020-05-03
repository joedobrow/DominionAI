import random

class BaseBot:
    
    def __init__(self):
        
        self.name = "BaseBot"
    
    def buy(self, card_map, deck, hand, discard, player):
        # This should return the card you want to buy
        # For example: 'province'
           
        return 'buy'

    def action(self, card_map, deck, hand, discard, player):
        # This should return a string of the action card you want to play
        # For example: 'smithy'
        return 'action'

    def remodel(self, card_map, deck, hand, discard, player):
        # this should return an array with the card you want to trash followed by the card you want to gain.
        # For example: ['silver', 'duchy']
        return ['trashed_card', 'gained_card']


    # HELPER FUNCTIONS:

    def get_coin(self, card_map, hand):
        coin = 0
        for card in card_map:
            coin += hand[card] * card_map[card]['coin']
        return coin

    def get_opponents_vp(self, card_map, deck, hand, discard):
        vp = 0
        for card in card_map:
            vp += card_map[card]['vp'] * (8 - (deck[card] + hand[card] + discard[card]) - card_map[card]['supply'])
        return vp

    def get_my_vp(self, card_map, deck, hand, discard):
        vp = 0
        for card in card_map:
            vp += card_map[card]['vp'] * (deck[card] + hand[card] + discard[card])
        return vp
