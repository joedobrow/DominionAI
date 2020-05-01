class TomBot:

	def __init__(self):
		self.name = "TomBot"

		# 0 == buy money, 1 == be creative, 2 == buy vps
		self.strategy_mode = 0

		# tweakables:
		self.dont_buy_silver_past_coin_average_in_deck = 8
		self.coin_averge_for_consider_provinces = 5
		self.coin_average_for_only_buy_vps = 9

	def get_moves(self, env, deck, hand, discard):

		self.strategy_mode = self.update_strategy_mode(env.card_map, deck, hand, discard)

		money = hand['copper'] + hand['silver']*2 + hand['gold']*3

		if self.strategy_mode == 0:
			return self.buy_best_money_card(env.card_map, money, deck, hand, discard)

		if self.strategy_mode == 1:
			if can_buy_province(money, env.card_map):
				return 'province'
			else:
				return self.buy_best_money_card(env.card_map, money, deck, hand, discard)

		if self.strategy_mode == 2:
			return buy_best_vp_card(env.card_map, money)

		# buy nothing
		return -1

	def update_strategy_mode(self, card_map, deck, hand, discard):
		# if two or less provinces, transition to 2
		if card_map['province']['supply'] <= 3:
			return 2

		# if two piles are out, transition to 2
		piles_out = 0
		for key in card_map:
			if card_map[key]['supply'] == 0:
				piles_out += 1
		if piles_out > 1:
			return 2

		# if average in deck > 9, transition to 2
		if average_money_in_total(deck, hand, discard) > self.coin_average_for_only_buy_vps:
			return 2

		# if average in deck > 6, transition to 1
		if average_money_in_total(deck, hand, discard) > self.coin_averge_for_consider_provinces:
			return 1

		# if all the golds are bought out, transition to 1
		if card_map['gold']['supply'] == 0:
			return 1

		return 0

	def buy_best_money_card(self, card_map, money, deck, hand, discard):
		if money >= card_map['gold']['cost'] and card_map['gold']['supply'] > 0:
			return 'gold'
		if money >= card_map['silver']['cost'] and card_map['silver']['supply'] > 0 and average_money_in_total(deck, hand, discard) <= self.dont_buy_silver_past_coin_average_in_deck:
			return 'silver'
		return -1 # dont buy copper dummy

def buy_best_vp_card(card_map, money):
	if can_buy_province(money, card_map):
		return 'province'
	if money >= card_map['duchy']['cost'] and card_map['duchy']['supply'] > 0:
		return 'duchy'
	if money >= card_map['estate']['cost'] and card_map['estate']['supply'] > 0:
		return 'estate'
	return -1 # dont buy curses dummy


def can_buy_province(money, card_map):
	return money >= card_map['province']['cost']

# not used, but probably good to have
def average_money_in_deck(deck, hand, discard):
	return (money_in_object(deck) / num_cards_i_got(deck, hand, discard)) * 5

def average_money_in_total(deck, hand, discard):
	return ((money_in_object(deck) + money_in_object(discard) + money_in_object(hand)) / num_cards_i_got(deck, hand, discard)) * 5

def money_in_object(array):
	return array['copper'] + array['silver']*2 + array['gold']*3

def num_cards_i_got(deck, hand, discard):
	return sum(deck.values()) + sum(hand.values()) + sum(discard.values())


