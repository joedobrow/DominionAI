import BaseBot

class LoanOsborne2(BaseBot.BaseBot):

    # MESS AROUND WITH THESE
    BIG_FAT_DUCHY_TIME = 6
    GAME_OF_INCHES = 6
    MONEYLENDER_COUNT = 0
    SMITHY_COUNT = 0.0
    GOLDEN_SMITHY_RATIO = .20
    COPPER_REMAINING = 7
    BRING_IN_THE_SMITHY = 4

    def __init__ (self):

        self.name = 'Loan Osborne 2'
        
    def action(self, card_map, deck, hand, discard, bonus_coin, player):
        if (hand['moneylender'] > 0 and hand['copper'] > 0):
            self.COPPER_REMAINING -= 1
            return 'moneylender'

        elif (hand['smithy'] > 0):
            return 'smithy'

        else:
            return -1

    def deck_size(self, deck, discard):
        total = 0
        for key in deck:
            total += deck[key]
        for key in discard:
            total += discard[key]
        return total+5

    def buy(self, card_map, deck, hand, discard, bonus_coin, player):

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
            elif (coin >= card_map['moneylender']['cost'] and self.MONEYLENDER_COUNT < 1):
                self.MONEYLENDER_COUNT += 1
                return 'moneylender'
            elif (coin >= card_map['smithy']['cost'] and self.SMITHY_COUNT / self.deck_size(deck, discard) < self.GOLDEN_SMITHY_RATIO and self.COPPER_REMAINING < self.BRING_IN_THE_SMITHY):
                self.SMITHY_COUNT += 1
                return 'smithy'
            elif (coin >= card_map['silver']['cost'] and card_map['silver']['supply'] > 0):
                return 'silver'
            else:
                return -1
            

    def remodel(self, card_map, deck, hand, discard, bonus_coin, player):
        coin = self.get_coin(card_map, hand, bonus_coin)
        provinces_remaining = card_map['province']['supply']

        if (hand['gold'] > 0 and card_map['province']['supply'] > 0 and (coin >= 11 or coin == 7 or coin == 3 or provinces_remaining < self.BIG_FAT_DUCHY_TIME)):
            return ['gold', 'province']
        elif (hand['silver'] > 0 and card_map['duchy']['supply'] > 0 and provinces_remaining < self.BIG_FAT_DUCHY_TIME):
            return ['silver', 'duchy']
        elif (hand['copper'] > 0 and card_map['estate']['supply'] > 0 and provinces_remaining < self.GAME_OF_INCHES):
            return ['copper', 'estate']
        elif (hand['estate'] > 0 and card_map['remodel']['supply'] > 0):
            return ['estate', 'remodel']
        elif (hand['remodel'] > 0 and card_map['gold']['supply'] > 0):
            return ['remodel', 'gold']
        elif (hand['copper'] > 0 and card_map['estate']['supply'] > 0):
            return ['copper', 'estate']
        elif (hand['silver'] > 0 and card_map['duchy']['supply'] > 0):
            return ['silver', 'duchy']
        else:
            return ['','']


    
