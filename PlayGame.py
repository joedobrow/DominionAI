import random
import time
import Environment
import copy

class PlayGame:
    
    def __init__(self, bot1, bot2):
        
        # Determine player1 and player2. Note: Player 1 loses a victory point tie.
        

        self.flip = random.randint(0, 1)
        if self.flip == 0:
            self.player = [bot1, bot2]
        else:
            self.player = [bot2, bot1]
            
        self.env = Environment.Environment()
        self.deck = [{}, {}]
        self.hand = [{}, {}]
        self.discard = [{}, {}]
        self.move_list = [[], []]
        self.hand_list = [[], []]
        self.bonus_draw_list = [[], []]
        self.runtimes = [0, 0]
        self.extra_text = ["", ""]
        
        for card in list(self.env.card_map.keys()):
            self.deck[0][card], self.deck[1][card] = 0, 0
            self.hand[0][card], self.hand[1][card] = 0, 0
            self.discard[0][card], self.discard[1][card] = 0, 0
            
        self.deck[0]['copper'], self.deck[1]['copper'] = 7, 7
        self.deck[0]['estate'], self.deck[1]['estate'] = 3, 3
        
    def play_game(self):
        
        self.clean_up(0)
        self.clean_up(1)

        
        for turn in range(500):


            self.hand_list[0].append(list(self.hand[0].values()))
            self.coin = 0
            
            # ADD CHECK FOR IF THEY HAVE THE ACTIOn
            self.timer = time.time()
            action = self.player[0].action(
                    copy.deepcopy(self.env.card_map), 
                    copy.deepcopy(self.deck[0]), 
                    copy.deepcopy(self.hand[0]), 
                    copy.deepcopy(self.discard[0]),
                    self.coin,
                    0
            )
            self.add_time(0)
            self.execute_action(action, 0)

            self.timer = time.time()
            buy = self.player[0].buy(
                    copy.deepcopy(self.env.card_map), 
                    copy.deepcopy(self.deck[0]), 
                    copy.deepcopy(self.hand[0]), 
                    copy.deepcopy(self.discard[0]), 
                    copy.copy(self.coin), 
                    0
            )
            self.add_time(0)

            for card in self.env.card_map:
                self.coin += self.hand[0][card] * self.env.card_map[card]['coin']

            if buy in self.env.card_map:
                if (self.env.card_map[buy]['supply'] > 0) and (self.coin >= self.env.card_map[buy]['cost']):
                    self.discard[0][buy] += 1
                    self.env.card_map[buy]['supply'] -= 1
                else:
                    buy = 'nobuy'
            else:
                buy = 'nobuy'
            self.move_list[0].append([self.coin, action, buy])

            if self.env.check_win():
                to_return = []
                for i in self.declare_winner():
                    to_return.append(i)
                for i in [
                    turn,
                    self.move_list[self.flip], 
                    self.move_list[1 - self.flip], 
                    self.hand_list[self.flip], 
                    self.hand_list[1 - self.flip],
                    self.runtimes[self.flip],
                    self.runtimes[1 - self.flip],
                    self.extra_text[self.flip],
                    self.extra_text[1 - self.flip],
                    self.bonus_draw_list[self.flip],
                    self.bonus_draw_list[1 - self.flip]
                ]:
                    to_return.append(i)
                return to_return
            self.clean_up(0)

            self.hand_list[1].append(list(self.hand[1].values()))
            self.coin = 0
            
            self.timer = time.time()
            action = self.player[1].action(
                    copy.deepcopy(self.env.card_map), 
                    copy.deepcopy(self.deck[1]), 
                    copy.deepcopy(self.hand[1]), 
                    copy.deepcopy(self.discard[1]),
                    self.coin, 
                    1
            )            
            self.add_time(1)
            self.execute_action(action, 1)

            self.timer = time.time()
            buy = self.player[1].buy(
                    copy.deepcopy(self.env.card_map), 
                    copy.deepcopy(self.deck[1]), 
                    copy.deepcopy(self.hand[1]), 
                    copy.deepcopy(self.discard[1]), 
                    copy.copy(self.coin), 
                    1
            )
            self.add_time(1)

            for card in self.env.card_map:
                self.coin += self.hand[1][card] * self.env.card_map[card]['coin']

            if buy in self.env.card_map:
                if (self.env.card_map[buy]['supply'] > 0) and (self.coin >= self.env.card_map[buy]['cost']):
                    self.discard[1][buy] += 1
                    self.env.card_map[buy]['supply'] -= 1
                else:
                    buy = 'nobuy'
            else:
                buy = 'nobuy'
            self.move_list[1].append([self.coin, action, buy])

            if self.env.check_win():
                to_return = []
                for i in self.declare_winner():
                    to_return.append(i)
                for i in [
                    turn,
                    self.move_list[self.flip], 
                    self.move_list[1 - self.flip], 
                    self.hand_list[self.flip], 
                    self.hand_list[1 - self.flip],
                    self.runtimes[self.flip],
                    self.runtimes[1 - self.flip],
                    self.extra_text[self.flip],
                    self.extra_text[1 - self.flip],
                    self.bonus_draw_list[self.flip],
                    self.bonus_draw_list[1 - self.flip]
                ]:
                    to_return.append(i)
                return to_return
            self.clean_up(1)

        print('Time Out')
        return [self.declare_winner(), turn]
                       
    def clean_up(self, player):
            
        for card in self.env.card_map:
            card_amount = self.hand[player][card]
            self.discard[player][card] += card_amount
            self.hand[player][card] -= card_amount
            
        self.extra_text[player] = ''
        self.draw_card(5, player)

    def draw_card(self, cards, player):

        for i in range(cards):
            if sum(self.deck[player].values()) < 1:
                for card in self.env.card_map:
                    card_amount = self.discard[player][card]
                    self.discard[player][card] -= card_amount
                    self.deck[player][card] += card_amount
            else:
                draw = random.randint(1, sum(self.deck[player].values()))
                for card in self.env.card_map:
                    if draw <= self.deck[player][card]:
                        self.deck[player][card] -= 1
                        self.hand[player][card] += 1
                        break
                    draw -= self.deck[player][card]
     
    
    def declare_winner(self):
        p1_score = self.get_vp(0)
        p2_score = self.get_vp(1)
        if (p1_score > p2_score):
            return [self.flip, 0, p1_score, p2_score]
        else:
            return [1 - self.flip, 1, p2_score, p1_score]
        
    def get_vp(self, player):
        
        vp_total = 0
        
        for card in self.env.card_map:
            vp_total += self.deck[player][card] * self.env.card_map[card]['vp']
            vp_total += self.discard[player][card] * self.env.card_map[card]['vp']
            vp_total += self.hand[player][card] * self.env.card_map[card]['vp']
        return vp_total

    def add_time(self, player):

        self.runtimes[player] += time.time() - self.timer

    def execute_action(self, action, player):
        if action == 'smithy':
            self.draw_card(3, player)
            self.bonus_draw_list[player].append(self.hand[player])

        elif action == 'moneylender':
            if self.hand[player]['copper'] > 0:
                self.hand[player]['copper'] -= 1
                self.coin += 3

        elif action == 'remodel':
            if self.hand[player]['remodel'] > 0:
                self.hand[player]['remodel'] -= 1
                self.discard[player]['remodel'] += 1
                remodel = self.player[player].remodel(self.env.card_map, self.deck[player], self.hand[player], self.discard[player], self.coin, player)
                # NEED TO PUT IN CHECK FOR LEGAL REMODEL
                if (remodel[0] in self.env.card_map) and (remodel[1] in self.env.card_map):
                    if (
                            (self.hand[player][remodel[0]] > 0) and 
                            (self.hand[player][remodel[1]] > 0) and 
                            (self.env.card_map[remodel[1]]['supply'] > 0) and
                            (self.env.card_map[remodel[1]]['cost'] <= self.env.card_map[remodel[0]]['cost'] + 2)
                        ):

                        self.hand[player][remodel[0]] -= 1
                        self.discard[player][remodel[1]] += 1
                        self.env.card_map[remodel[1]]['supply'] -= 1

                    self.extra_text[player] = remodel[0] + ' into ' + remodel[1]