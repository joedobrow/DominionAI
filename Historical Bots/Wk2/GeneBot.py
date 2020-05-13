import random
import numpy as np
import BaseBot

class GeneBot(BaseBot.BaseBot):
    
    def __init__(self, weights=None):
        
        self.name = "AbstinenceBot"

        self.cards = ['province', 'gold', 'duchy', 'smithy', 'silver']
        if weights:
            self.weights = weights
        else:
            self.weights = []
            for i in self.cards:
                self.weights.append([randy(), randy(), randy(), randy(), randy(), randy()])


    def action(self, card_map, deck, hand, discard, bonus_coin, player):
        # This should return a string of the action card you want to play
        # For example: 'smithy'
        return 'smithy'

    
    def buy(self, card_map, deck, hand, discard, bonus_coin, player):
        
        money = self.get_coin(card_map, hand, bonus_coin)

        num_provinces_left = numProvincesLeft(card_map) / 10
        num_smithies = (smithyCount(deck, hand, discard)+1) / 3
        deck_size = (num_cards_i_got(deck, hand, discard)-9) / 20
        vp_spread = (self.get_my_vp(card_map, deck, hand, discard) - self.get_opponents_vp(card_map, deck, hand, discard) + player/2) / 10
        avg_coin_5 = average_money_in_total(deck, hand, discard) / 3

        if num_cards_i_got(deck, hand, discard) < 12 and smithyCount(deck, hand, discard) < 1:
            if money >= 4:
                return 'smithy'
        if numProvincesLeft(card_map) == 3:
            if money >= 8:
                return 'province'
        if numProvincesLeft(card_map) == 1:
            if money >= 8 and vp_spread >= -8:
                return 'province'
            # if money >= 5:
            #     return 'duchy'

        
        priorities = {'province':0, 'gold':0, 'duchy':0, 'smithy':0, 'silver':0}
        priorities['province'] = self.weights[0][0]*num_provinces_left + self.weights[0][1]*num_smithies + self.weights[0][2]*deck_size + self.weights[0][3]*vp_spread + self.weights[0][4]*avg_coin_5 + self.weights[0][5]
        priorities['gold'] = self.weights[1][0]*num_provinces_left + self.weights[1][1]*num_smithies + self.weights[1][2]*deck_size + self.weights[1][3]*vp_spread + self.weights[1][4]*avg_coin_5 + self.weights[1][5]
        priorities['duchy'] = self.weights[2][0]*num_provinces_left + self.weights[2][1]*num_smithies + self.weights[2][2]*deck_size + self.weights[2][3]*vp_spread + self.weights[2][4]*avg_coin_5 + self.weights[2][5]
        priorities['smithy'] = self.weights[3][0]*num_provinces_left + self.weights[3][1]*num_smithies + self.weights[3][2]*deck_size + self.weights[3][3]*vp_spread + self.weights[3][4]*avg_coin_5 + self.weights[3][5]
        priorities['silver'] = self.weights[4][0]*num_provinces_left + self.weights[4][1]*num_smithies + self.weights[4][2]*deck_size + self.weights[4][3]*vp_spread + self.weights[4][4]*avg_coin_5 + self.weights[4][5]

        priorities = {k: v for k, v in sorted(priorities.items(), key=lambda item: item[1])}

        
        for i in range(len(priorities)):
            if money >= card_map[list(priorities.keys())[4-i]]['cost'] and card_map[list(priorities.keys())[4-i]]['supply'] > 0:
                if list(priorities.keys())[4-i] == 'smithy' and smithyCount(deck, hand, discard) >= 3:
                    # print("SKIPPING")
                    continue
                return list(priorities.keys())[4-i]
        return ''

    def remodel(self, card_map, deck, hand, discard, bonus_coin, player):
        # this should return an array with the card you want to trash followed by the card you want to gain.
        # For example: ['silver', 'duchy']
        throw("DERP")
        return ['trashed_card', 'gained_card']

    
    def generate_priority(self, card_map, deck, hand, discard):
        return ['province', 'gold', 'smithy', 'silver', 'duchy']

def randy():
    return random.uniform(-1, 1)

def numProvincesLeft(card_map):
    return card_map['province']['supply']

def smithyCount(deck, hand, discard):
    return deck['smithy'] + hand['smithy'] + discard['smithy']


def average_money_in_total(deck, hand, discard):
    return ((money_in_object(deck) + money_in_object(discard) + money_in_object(hand)) / num_cards_i_got(deck, hand, discard)) * 5

def money_in_object(array):
    return array['copper'] + array['silver']*2 + array['gold']*3

def num_cards_i_got(deck, hand, discard):
    return sum(deck.values()) + sum(hand.values()) + sum(discard.values())

