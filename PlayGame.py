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
        self.in_play = [{}, {}]
        self.bonus_draw_list = [[], []]
        self.runtimes = [0, 0]
        self.extra_text = [[], []]
        self.actions = [1, 1]
        self.trash = {}
        
        for card in list(self.env.card_map.keys()):
            self.deck[0][card], self.deck[1][card] = 0, 0
            self.hand[0][card], self.hand[1][card] = 0, 0
            self.discard[0][card], self.discard[1][card] = 0, 0
            self.in_play[0][card], self.in_play[1][card] = 0, 0
            self.trash[card] = 0
            
        self.deck[0]['copper'], self.deck[1]['copper'] = 7, 7
        self.deck[0]['estate'], self.deck[1]['estate'] = 3, 3
        
    def play_game(self):
        
        self.clean_up(0)
        self.clean_up(1)

        
        for turn in range(500):


            self.hand_list[0].append(list(self.hand[0].values()))
            self.coin = 0
            
            while self.actions[0] > 0:
                self.timer = time.time()
                action = self.player[0].action(
                        copy.deepcopy(self.env.card_map), 
                        copy.deepcopy(self.deck[0]), 
                        copy.deepcopy(self.hand[0]), 
                        copy.deepcopy(self.discard[0]),
                        self.coin,
                        copy.deepcopy(self.actions[0]),
                        copy.deepcopy(self.in_play[0]),
                        copy.deepcopy(self.trash),
                        0
                )
                self.add_time(0)

                if action in self.env.card_map:
                    if self.hand[0][action] > 0:
                        self.execute_action(action, 0)
                self.actions[0] -= 1

            self.timer = time.time()
            buy = self.player[0].buy(
                    copy.deepcopy(self.env.card_map), 
                    copy.deepcopy(self.deck[0]), 
                    copy.deepcopy(self.hand[0]), 
                    copy.deepcopy(self.discard[0]), 
                    copy.copy(self.coin),
                    copy.deepcopy(self.actions[0]),
                    copy.deepcopy(self.in_play[0]),
                    copy.deepcopy(self.trash),
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

            while self.actions[1] > 0:
            
                self.timer = time.time()
                action = self.player[1].action(
                        copy.deepcopy(self.env.card_map), 
                        copy.deepcopy(self.deck[1]), 
                        copy.deepcopy(self.hand[1]), 
                        copy.deepcopy(self.discard[1]),
                        self.coin,
                        copy.deepcopy(self.actions[1]),
                        copy.deepcopy(self.in_play[1]),
                        copy.deepcopy(self.trash),
                        1
                )            
                self.add_time(1)

                if action in self.env.card_map:
                    if self.hand[1][action] > 0:
                        self.execute_action(action, 1)
                self.actions[1] -= 1

            self.timer = time.time()
            buy = self.player[1].buy(
                    copy.deepcopy(self.env.card_map), 
                    copy.deepcopy(self.deck[1]), 
                    copy.deepcopy(self.hand[1]), 
                    copy.deepcopy(self.discard[1]), 
                    copy.copy(self.coin),
                    copy.deepcopy(self.actions[1]),
                    copy.deepcopy(self.in_play[1]),
                    copy.deepcopy(self.trash),
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

       # print('Time Out')
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
                       
    def clean_up(self, player):
            
        for card in self.env.card_map:
            card_amount = self.hand[player][card]
            self.discard[player][card] += card_amount
            self.hand[player][card] -= card_amount
            card_amount = self.in_play[player][card]
            self.discard[player][card] += card_amount
            self.in_play[player][card] -= card_amount
            
        self.draw_card(5, player)
        self.actions[player] = 1

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
            return [self.flip, self.flip, p1_score, p2_score]
        else:
            return [1 - self.flip, self.flip, p2_score, p1_score]
        
    def get_vp(self, player):
        
        vp_total = 0
        
        for card in self.env.card_map:
            vp_total += self.deck[player][card] * self.env.card_map[card]['vp']
            vp_total += self.discard[player][card] * self.env.card_map[card]['vp']
            vp_total += self.hand[player][card] * self.env.card_map[card]['vp']
        num_cards = sum(self.discard[player].values()) + sum(self.deck[player].values()) + sum(self.hand[player].values())
        vp_total += (num_cards//10) * (self.hand[player]['gardens'] + self.discard[player]['gardens'] + self.deck[player]['gardens'])
        return vp_total

    def add_time(self, player):

        self.runtimes[player] += time.time() - self.timer

    def execute_action(self, action, player):

        if action == 'smithy':
            self.in_play[player]['smithy'] += 1
            self.hand[player]['smithy'] -= 1
            self.draw_card(3, player)
            self.bonus_draw_list[player].append(copy.deepcopy(self.hand[player]))

        elif action == 'moneylender':
            if self.hand[player]['copper'] > 0:
                self.in_play[player]['moneylender'] += 1
                self.hand[player]['copper'] -= 1
                self.coin += 3

        elif action == 'remodel':
            self.in_play[player]['remodel'] += 1
            self.hand[player]['remodel'] -= 1
            self.timer = time.time()
            remodel = self.player[player].remodel(
                    copy.deepcopy(self.env.card_map), 
                    copy.deepcopy(self.deck[player]), 
                    copy.deepcopy(self.hand[player]), 
                    copy.deepcopy(self.discard[player]), 
                    self.coin,
                    copy.deepcopy(self.actions[player]),
                    copy.deepcopy(self.in_play[player]),
                    copy.deepcopy(self.trash),
                    player
            )
            self.add_time(player)
            # NEED TO PUT IN CHECK FOR LEGAL REMODEL
            if (remodel[0] in self.env.card_map) and (remodel[1] in self.env.card_map):
                if (
                        (self.hand[player][remodel[0]] > 0) and 
                        (self.hand[player][remodel[1]] > 0) and 
                        (self.env.card_map[remodel[1]]['supply'] > 0) and
                        (self.env.card_map[remodel[1]]['cost'] <= self.env.card_map[remodel[0]]['cost'] + 2)
                    ):

                    self.hand[player][remodel[0]] -= 1
                    self.trash[remodel[0]] += 1
                    self.discard[player][remodel[1]] += 1
                    self.env.card_map[remodel[1]]['supply'] -= 1

                self.extra_text[player].append([remodel[0], remodel[1]])

        elif action == 'chapel':
            self.hand[player]['chapel'] -= 1
            self.in_play[player]['chapel'] += 1
            self.timer = time.time()
            chapel = self.player[player].chapel(
                    copy.deepcopy(self.env.card_map), 
                    copy.deepcopy(self.deck[player]), 
                    copy.deepcopy(self.hand[player]), 
                    copy.deepcopy(self.discard[player]), 
                    self.coin,
                    copy.deepcopy(self.actions[player]),
                    copy.deepcopy(self.in_play[player]),
                    copy.deepcopy(self.trash),
                    player
            )
            for card in chapel:
                if self.hand[player][card] > 0:
                    self.hand[player][card] -= 1
                    self.trash[card] += 1

        elif action == 'village':
            self.hand[player]['village'] -= 1
            self.in_play[player]['village'] += 1
            self.draw_card(1, player)
            self.action[player] += 2

        elif action == 'witch':
            self.hand[player]['witch'] -= 1
            self.in_play[player]['witch'] += 1
            self.draw_card(2, player)
            if self.env.card_map['curse']['supply'] > 0:
                self.discard[1 - player]['curse'] += 1

