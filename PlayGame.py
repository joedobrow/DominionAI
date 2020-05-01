import random
import Environment

class PlayGame:
    
    def __init__(self, bot1, bot2, verbose=False):
        
        # Determine player1 and player2. Note: Player 1 loses a victory point tie.
        
        flip = random.randint(1, 2)
        self.flip = flip
        if flip == 1:
            self.p1 = bot1
            self.p2 = bot2
        else:
            self.p2 = bot1
            self.p1 = bot2
            
        self.env = Environment.Environment()
        self.verbose = verbose
        self.p1_deck, self.p2_deck = {}, {}
        self.p1_hand, self.p2_hand = {}, {}
        self.p1_discard, self.p2_discard = {}, {}
        self.p1_move_list, self.p2_move_list = [], []
        
        for card in self.env.card_map.keys():
            self.p1_deck[card], self.p2_deck[card] = 0, 0
            self.p1_hand[card], self.p2_hand[card] = 0, 0
            self.p1_discard[card], self.p2_discard[card] = 0, 0
            
        self.p1_deck['copper'], self.p2_deck['copper'] = 7, 7
        self.p1_deck['estate'], self.p2_deck['estate'] = 3, 3
        
        if verbose:
            print("Player 1: {}".format(self.p1.name))
            print("Player 2: {}".format(self.p2.name))
        
    def play_game(self):
        
        self.clean_up(1)
        self.clean_up(-1)
        
        for turn in range(2000):
            
            move = self.p1.get_moves(self.env, self.p1_deck, self.p1_hand, self.p1_discard)
            if move in self.env.card_map.keys():
                coin = 0
                for card in self.p1_hand.keys():
                    coin += self.p1_hand[card] * self.env.card_map[card]['coin']
                if (self.env.card_map[move]['supply'] > 0) and (coin >= self.env.card_map[move]['cost']):
                    self.p1_discard[move] += 1
                    self.env.card_map[move]['supply'] -= 1
                    self.p1_move_list.append(move)
                else:
                    self.p1_move_list.append('Error bad bot move')
            else:
                self.p1_move_list.append('bot bad or no return')
            if self.env.check_win():
                return [self.declare_winner(), turn]
            self.clean_up(1)
                
            move = self.p2.get_moves(self.env, self.p2_deck, self.p2_hand, self.p2_discard)
            if move in self.env.card_map.keys():
                coin = 0
                for card in self.p2_hand.keys():
                    coin += self.p2_hand[card] * self.env.card_map[card]['coin']
                if (self.env.card_map[move]['supply'] > 0) and (coin >= self.env.card_map[move]['cost']):
                    self.p2_discard[move] += 1
                    self.env.card_map[move]['supply'] -= 1
                    self.p2_move_list.append(move)
                else:
                    self.p1_move_list.append('Error bad bot move')
            else:
                self.p1_move_list.append('bot bad or no return')
            if self.env.check_win():
                return [self.declare_winner(), turn]
            self.clean_up(-1)

        print('Time Out')
        return [self.declare_winner(), None]
                       
    def clean_up(self, player):

        if player == 1:
            deck, discard, hand = self.p1_deck, self.p1_discard, self.p1_hand
        else:
            deck, discard, hand = self.p2_deck, self.p2_discard, self.p2_hand
            
        for card in self.env.card_map.keys():
            card_amount = hand[card]
            discard[card] += card_amount
            hand[card] -= card_amount
            
        for i in range(5):
            if sum(deck.values()) < 1:
                for card in self.env.card_map.keys():
                    card_amount = discard[card]
                    discard[card] -= card_amount
                    deck[card] += card_amount
            if sum(deck.values()) > 0:
                draw = random.randint(1, sum(deck.values()))
                for card in self.env.card_map.keys():
                    if draw <= deck[card]:
                        deck[card] -= 1
                        hand[card] += 1
                        break
                    draw -= deck[card]
    
    
    def declare_winner(self):
        p1_score = self.get_vp(1)
        p2_score = self.get_vp(-1)
        if (p1_score > p2_score):
            if self.flip == 1:
                return 1
            else:
                return -1
        else:
            if self.flip == 1:
                return -1
            else:
                return 1
        
    def get_vp(self, player):
        
        vp_total = 0
        
        if player == 1:
            for card in self.env.card_map.keys():
                vp_total += self.p1_deck[card] * self.env.card_map[card]['vp']
                vp_total += self.p1_discard[card] * self.env.card_map[card]['vp']
                vp_total += self.p1_hand[card] * self.env.card_map[card]['vp']
            return vp_total
        
        else:
            for card in self.env.card_map.keys():
                vp_total += self.p2_deck[card] * self.env.card_map[card]['vp']
                vp_total += self.p2_discard[card] * self.env.card_map[card]['vp']
                vp_total += self.p2_hand[card] * self.env.card_map[card]['vp']
            return vp_total