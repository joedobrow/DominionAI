import random

class BaseBot:
    
    def __init__(self):
        
        self.name = "BaseBot"

    def action(self, card_map, deck, hand, discard, bonus_coin, player):
        # This should return a string of the action card you want to play
        # For example: 'smithy'
        return 'action'
    
    def buy(self, card_map, deck, hand, discard, bonus_coin, player):
        # bonus_coin is extra coin gotten from other effects such as moneylender
        # This should return the card you want to buy
        # For example: 'province'
           
        return 'buy'

    def remodel(self, card_map, deck, hand, discard, bonus_coin, player):
        # this should return an array with the card you want to trash followed by the card you want to gain.
        # For example: ['silver', 'duchy']
        return ['trashed_card', 'gained_card']


    # HELPER FUNCTIONS:

    def get_coin(self, card_map, hand, bonus_coin):
        coin = 0
        for card in card_map:
            coin += hand[card] * card_map[card]['coin']
        return coin + bonus_coin

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

    def get_num_actions_in_deck(self, card_map, deck, hand, discard):
        num_actions = 0
        for card in card_map:
            if 'action' in card_map[card]['types']:
                num_actions += deck[card] + hand[card] + discard[card]
        return num_actions

