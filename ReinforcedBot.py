
import random
import ExampleBot
import Environment
import PlayGame
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

class ReinforcedBot:
    
	def __init__(self):

		self.name = "ReinforcedBot"
		self.env = Environment.Environment()
		self.train_data = pd.DataFrame(columns = ['Coin', 'Province', 'Value', 'VP', 'Move', 'Win'])
		self.model = RandomForestClassifier(n_estimators = 30, max_depth=5)
		self.p1_deck, self.p2_deck = {}, {}
		self.p1_hand, self.p2_hand = {}, {}
		self.p1_discard, self.p2_discard = {}, {}
		self.p1_move_list, self.p2_move_list = [], []
		self.flip = 1
		for card in self.env.card_map.keys():
			self.p1_deck[card], self.p2_deck[card] = 0, 0
			self.p1_hand[card], self.p2_hand[card] = 0, 0
			self.p1_discard[card], self.p2_discard[card] = 0, 0
		self.p1_deck['copper'], self.p2_deck['copper'] = 7, 7
		self.p1_deck['estate'], self.p2_deck['estate'] = 3, 3
		self.env.card_map['copper']['supply'] = 1000000

	def get_moves(self, env, deck, hand, discard):

		self.env = env
		self.deck = deck
		self.hand = hand
		self.discard = discard
		coin = 0
		for card in hand.keys():
			coin += self.env.card_map[card]['coin'] * hand[card]
		province = self.env.card_map['province']['supply']
		average_card_value = 0
		for card in self.env.card_map.keys():
			average_card_value += (self.deck[card] * self.env.card_map[card]['coin']+self.discard[card] * self.env.card_map[card]['coin']+self.hand[card]*self.env.card_map[card]['coin'])
		cards_in_deck = sum(self.deck.values()) + sum(self.hand.values()) + sum(self.discard.values())
		average_card_value /= cards_in_deck
		vps = 0
		for card in self.env.card_map.keys():
			vps += (self.deck[card] * self.env.card_map[card]['vp']+self.discard[card]*self.env.card_map[card]['vp']+self.hand[card] * self.env.card_map[card]['vp'])
		input_vector = [coin, province, average_card_value, vps]
		try:
			return self.model.predict(input_vector)
		except:
			moves = []
			for card in env.card_map.keys():
				if (coin >= env.card_map[card]['cost']) and env.card_map[card]['supply'] > 0:
					moves.append(card)
			try:
				move = random.choice(moves)
				return move
			except:
				return ''

	def train_main(self):
		enemy = ExampleBot.ExampleBot()
		for i in range(5000):
			self.train(enemy)
		to_fit = self.train_data[self.train_data.Win == 1]
		X = to_fit.drop(['Move', 'Win'], 1)
		y = pd.get_dummies(to_fit['Move'])
		self.model.fit(X, y)

	def model_test(self, coin, province, value, vp):
		return self.model.predict(np.array([coin, province, value, vp]).reshape(1, -1))

	def train(self, enemy):

		flip = random.randint(1, 2)
		self.flip = flip
		if flip == 1:
			self.p1 = self
			self.p2 = enemy
		else:
			self.p2 = enemy
			self.p1 = self

		self.clean_up(1)
		self.clean_up(-1)
        
		for turns in range(2000):
            
			move = self.p1.get_moves(self.env, self.p1_deck, self.p1_hand, self.p1_discard)
			if move in self.env.card_map.keys():
				coin = 0
				for card in self.p1_hand.keys():
					coin += self.p1_hand[card] * self.env.card_map[card]['coin']
				if (self.env.card_map[move]['supply'] > 0) and (coin >= self.env.card_map[move]['cost']):
					self.p1_discard[move] += 1
					self.env.card_map[move]['supply'] -= 1
					if flip == 1:
						self.collect_data(coin, move)
				else:
					print('1 Error bad move')
					print(self.flip)
			else:
				print('2 Error bad move', move, self.flip)
			if self.env.check_win():
				return self.declare_winner()
			self.clean_up(1)
			move = self.p2.get_moves(self.env, self.p2_deck, self.p2_hand, self.p2_discard)

			if move in self.env.card_map.keys():
				coin = 0
				for card in self.p2_hand.keys():
					coin += self.p2_hand[card] * self.env.card_map[card]['coin']
				if (self.env.card_map[move]['supply'] > 0) and (coin >= self.env.card_map[move]['cost']):
					self.p2_discard[move] += 1
					self.env.card_map[move]['supply'] -= 1
					if flip != 1:
						self.collect_data(coin, move)
				else:
					print('3 Error bad move')
			else:
				print('4 Error bad move')
			if self.env.check_win():
				return self.declare_winner()
			self.clean_up(-1)

		print('Time Out')
		return self.declare_winner()

	def collect_data(self, coin, move):

		if self.flip == 1:
			deck = self.p1_deck
			discard = self.p1_discard
			hand = self.p1_hand
		else:
			deck = self.p2_deck
			discard = self.p1_discard
			hand = self.p1_hand

		provinces = self.env.card_map['province']['supply']
		cards_in_deck = (sum(deck.values()) + sum(discard.values()) + sum(hand.values()))
		# CHECK THIS:
		average_card_value = 0
		for card in self.env.card_map.keys():
			average_card_value += (
				deck[card] * self.env.card_map[card]['coin'] +
				discard[card] * self.env.card_map[card]['coin'] +
				hand[card] * self.env.card_map[card]['coin']
			)
		average_card_value /= cards_in_deck
		vps = 0
		for card in self.env.card_map.keys():
			vps += (
				deck[card] * self.env.card_map[card]['vp'] +
				discard[card] * self.env.card_map[card]['vp'] +
				hand[card] * self.env.card_map[card]['vp']
			)
		self.train_data = self.train_data.append({
			'Coin':coin, 
			'Province':provinces, 
			'Value':average_card_value,
			'VP':vps,
			'Move':move,
			'Win':0
		}, ignore_index=True)



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
		turns = len(self.train_data)
		if (p1_score > p2_score):
			if self.flip == 1:
				self.train_data.iloc[-turns:, 5] = [1]*(turns)
			else:
				self.train_data.iloc[-turns:, 5] = [-1]*(turns)
		else:
			if self.flip == 1:
				self.train_data.iloc[-turns:, 5] = [-1]*(turns)
			else:
				self.train_data.iloc[-turns:, 5] = [1]*(turns)
        
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
    	