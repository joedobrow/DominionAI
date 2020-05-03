class MoneyBot:

	def __init__(self):
		self.name = "FuckYoBitchBot"
		self.money = 0
		self.card_map = None

	def get_moves(self, env, deck, hand, discard):

		self.money = hand['copper'] + hand['silver']*2 + hand['gold']*3
		self.card_map = env.card_map

		piles_out = 0
		for pile in self.card_map:
			if self.card_map[pile]['supply'] == 0:
				piles_out += 1

		if self.can_buy_province():
			return 'province'

		if self.card_map['province']['supply'] <= 2:
			choice = self.buy_best_vp_card(True)
			if choice != -1:
				return choice

		if piles_out == 2:
			choice = self.buy_best_vp_card(False)
			if choice != -1:
				return choice

		best_money_choice = {'name': -1, 'avg_coin': average_money_in_total(deck, hand, discard)}
		for card in self.card_map:
			new_avg = average_money_with_additional_card(deck, hand, discard, self.card_map[card])
			if self.money >= self.card_map[card]['cost'] and self.card_map[card]['supply'] > 0 and new_avg > best_money_choice['avg_coin']:
				best_money_choice['name'] = card
				best_money_choice['avg_coin'] = new_avg


		return best_money_choice['name']


	def buy_best_vp_card(self, consider_estate):
		best = {'name': -1, 'vp': -1}
		for card in self.card_map:
			if self.money >= self.card_map[card]['cost'] and self.card_map[card]['supply'] > 0 and self.card_map[card]['vp'] > best['vp']:
				if not consider_estate and card == 'estate':
					continue
				best['name'] = card
				best['vp'] = self.card_map[card]['vp']
		return best['name']

	def can_buy_province(self):
		return self.money >= self.card_map['province']['cost']


def average_money_in_total(deck, hand, discard):
	return ((money_in_object(deck) + money_in_object(discard) + money_in_object(hand)) / num_cards_i_got(deck, hand, discard)) * 5

def average_money_with_additional_card(deck, hand, discard, potential_card):
	return ((money_in_object(deck) + money_in_object(discard) + money_in_object(hand) + money_from_card(potential_card)) / (1 + num_cards_i_got(deck, hand, discard))) * 5



def money_in_object(array):
	return array['copper'] + array['silver']*2 + array['gold']*3

def num_cards_i_got(deck, hand, discard):
	return sum(deck.values()) + sum(hand.values()) + sum(discard.values())

def money_from_card(potential_card):
	return potential_card['coin']


