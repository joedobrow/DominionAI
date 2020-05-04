import random
import time
import Environment

class PlayGame:
    
    def __init__(self, bot1, bot2, verbose=0):
        
        # Determine player1 and player2. Note: Player 1 loses a victory point tie.
        
        # verbose 0: no prints except errors
        # 1: Display names
        # 2: names and moves

        self.flip = random.randint(0, 1)
        if self.flip == 0:
            self.player = [bot1, bot2]
        else:
            self.player = [bot2, bot1]
            
        self.env = Environment.Environment()
        self.verbose = verbose
        self.deck = [{}, {}]
        self.hand = [{}, {}]
        self.discard = [{}, {}]
        self.move_list = [[], []]
        self.hand_list = [[], []]
        self.runtimes = [0, 0]
        self.extra_text = ["", ""]
        
        for card in list(self.env.card_map.keys()):
            self.deck[0][card], self.deck[1][card] = 0, 0
            self.hand[0][card], self.hand[1][card] = 0, 0
            self.discard[0][card], self.discard[1][card] = 0, 0
            
        self.deck[0]['copper'], self.deck[1]['copper'] = 7, 7
        self.deck[0]['estate'], self.deck[1]['estate'] = 3, 3
        
        if self.verbose == 1:
            print("Player 1: {}".format(self.player[0].name))
            print("Player 2: {}".format(self.player[1].name))
        
    def play_game(self):
        
        self.clean_up(0)
        self.clean_up(1)
        
        for turn in range(500):


            self.hand_list[0].append(list(self.hand[0].values()))
            self.coin = 0
            
            # ADD CHECK FOR IF THEY HAVE THE ACTIOn
            self.timer = time.time()
            action = self.player[0].action(self.env.card_map, self.deck[0], self.hand[0], self.discard[0], 0)
            self.add_time(0)
            self.execute_action(action, 0)
            if self.verbose > 0:
                action += ' '
                action += self.extra_text[0]

            self.timer = time.time()
            buy = self.player[0].buy(self.env.card_map, self.deck[0], self.hand[0], self.discard[0], self.coin, 0)
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
                if self.verbose > 0:
                    return [
                        self.declare_winner(), 
                        turn, 
                        self.move_list[self.flip], 
                        self.move_list[1 - self.flip], 
                        self.hand_list[self.flip], 
                        self.hand_list[1 - self.flip]
                    ]

                return [self.declare_winner(), turn]
            self.clean_up(0)

            self.hand_list[1].append(list(self.hand[1].values()))
            self.coin = 0
            
            self.timer = time.time()
            action = self.player[1].action(self.env.card_map, self.deck[1], self.hand[1], self.discard[1], 1)
            self.add_time(1)
            self.execute_action(action, 1)
            if self.verbose > 0:
                action += ' '
                action += self.extra_text[1]

            self.timer = time.time()
            buy = self.player[1].buy(self.env.card_map, self.deck[1], self.hand[1], self.discard[1], self.coin, 1)
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
                if self.verbose > 0 :
                    return [
                        self.declare_winner(), 
                        turn, 
                        self.move_list[self.flip], 
                        self.move_list[1 - self.flip], 
                        self.hand_list[self.flip], 
                        self.hand_list[1 - self.flip]
                    ]

                return [self.declare_winner(), turn]
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
            return self.flip
        else:
            return 1 - self.flip
        
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

        elif action == 'moneylender':
            if self.hand[player]['copper'] > 0:
                self.hand[player]['copper'] -= 1
                self.coin += 3

        elif action == 'remodel':
            self.hand[player]['remodel'] -= 1
            remodel = self.player[player].remodel(self.env.card_map, self.deck[player], self.hand[player], self.discard[player], player)
            if (
                    (self.hand[player][remodel[0]] > 0) and 
                    (self.hand[player][remodel[1]] > 0) and 
                    (self.env.card_map[remodel[1]]['supply'] > 0) and
                    (self.env.card_map[remodel[1]]['cost'] <= self.env.card_map[remodel[0]]['cost'] + 2)
                ):

                self.hand[player][remodel[0]] -= 1
                self.discard[player][remodel[1]] += 1
                self.env.card_map[remodel[1]]['supply'] -= 1
                self.discard[player]['remodel'] += 1

            if self.verbose > 0:
                self.extra_text[player] = remodel[0] + ' into ' + remodel[1]



    def add_time(self, player):
        if (player == 1) and (self.flip == 1):
            self.bot1_runtime += time.time() - self.timer
        elif (player == 2) and (self.flip == 2):
            self.bot1_runtime += time.time() - self.timer
        else:
            self.bot2_runtime += time.time() - timer

    def process_action(self, action, player):
        if action == 'smithy':
            self.draw_cards(3, player)
        elif action == 'moneylender':
            if player == 1:
                if self.p1_hand['copper'] > 0:
                    self.p1_hand['copper'] -= 1
                    self.coin += 3
            else:
                if self.p2_hand['copper'] > 0:
                    self.p2_hand['copper'] -= 1
                    self.coin += 3
        elif action == 'remodel':
            if player == 1:
                remodel = self.p1.remodel(self.env.card_map, self.p1_deck, self.p1_hand, self.p1_discard, 1)
                if (
                        (self.p1_hand[remodel[0]] > 0) and 
                        (self.env.card_map[remodel[1]]['coin'] <= self.env.card_map[remodel[0]]['coin'] + 2) and 
                        (self.env.card_map[remodel[1]]['supply'] > 0)
                ):
                    self.p1_hand[remodel[0]] -= 1
                    self.env.card_map[remodel[1]]['supply'] -= 1
                    self.p1_discard[remodel[1]] += 1

            else:
                remodel = self.p2.remodel(self.env.card_map, self.p2_deck, self.p2_hand, self.p2_discard, 2)
                if (
                        (self.p2_hand[remodel[0]] > 0) and 
                        (self.env.card_map[remodel[1]]['coin'] <= self.env.card_map[remodel[0]]['coin'] + 2) and 
                        (self.env.card_map[remodel[1]]['supply'] > 0)
                ):
                    self.p2_hand[remodel[0]] -= 1
                    self.env.card_map[remodel[1]]['supply'] -= 1
                    self.p2_discard[remodel[1]] += 1

