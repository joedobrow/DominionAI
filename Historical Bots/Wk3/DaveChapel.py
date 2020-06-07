import BaseBot

class DaveChapel(BaseBot.BaseBot):

    # MESS AROUND WITH THESE
    BIG_FAT_DUCHY_TIME = 6
    GAME_OF_INCHES = 6
    CHAPEL_COUNT = 0
    WITCH_COUNT = 0.0
    GOLDEN_WITCH_RATIO = .1
    COPPERS_BURNED = 0
    ESTATES_BURNED = 0
    BURNED_ENOUGH = 6
    ENOUGH_SHIT_CARDS = 1

    def __init__ (self):

        self.name = 'Dave Chapel'
        
    def action(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):
        if (hand['chapel'] > 0): 
            if (hand['witch'] == 0):
                return 'chapel'
            elif (hand['copper'] + hand['estate'] + hand['curse'] >= self.ENOUGH_SHIT_CARDS):
                return 'chapel'
            else:
                return 'witch'
        else:
            return -1

    def deck_size(self, deck, discard):
        total = 0
        for key in deck:
            total += deck[key]
        for key in discard:
            total += discard[key]
        return total+5

    def buy(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):

        coin = self.get_coin(card_map, hand, bonus_coin)
        provinces_remaining = card_map['province']['supply']
        
        if (coin >= card_map['province']['cost'] and provinces_remaining > 0):
            return 'province'

        elif (provinces_remaining < self.BIG_FAT_DUCHY_TIME and coin >= card_map['duchy']['cost'] and card_map['duchy']['supply'] > 0):
            return 'duchy'

        elif (provinces_remaining < self.GAME_OF_INCHES and coin >= card_map['estate']['cost'] and  card_map['estate']['supply'] > 0):
            return 'estate'

        else:
            if (coin >= card_map['gold']['cost'] and card_map['gold']['supply'] > 0):
                return 'gold'
            elif (coin >= card_map['chapel']['cost'] and self.CHAPEL_COUNT < 1):
                self.CHAPEL_COUNT += 1
                return 'chapel'
            elif (coin >= card_map['witch']['cost'] and self.COPPERS_BURNED + self.ESTATES_BURNED >= self.BURNED_ENOUGH and self.WITCH_COUNT < 1):
                self.WITCH_COUNT += 1
                return 'witch'
            elif (coin >= card_map['silver']['cost'] and card_map['silver']['supply'] > 0):
                return 'silver'
            else:
                return -1

    def chapel(self, card_map, deck, hand, discard, bonus_coin, actions, in_play, trash, player):
        # If cards are erroneously returned, nothing will be trashed. If some of the cards are
        # erroneous but some are correct, the correct returns will still be trashed.
        trashTheseShitCards = []
        for i in range(hand['copper']):
            trashTheseShitCards.append('copper')
            self.COPPERS_BURNED += 1
        for i in range(hand['estate']):
            trashTheseShitCards.append('estate')
            self.ESTATES_BURNED += 1
        for i in range(hand['curse']):
            trashTheseShitCards.append('curse')
        return trashTheseShitCards

            
