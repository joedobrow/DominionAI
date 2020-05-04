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

		# print("avg: " + str(average_money_in_total(deck, hand, discard)))

		self.strategy_mode = self.update_strategy_mode(env.card_counts, deck, hand, discard)

		money = hand[0] + hand[1]*2 + hand[2]*3

		if self.strategy_mode == 0:
			return self.buy_best_money_card(env.money_map, env.card_counts, money, deck, hand, discard)

		if self.strategy_mode == 1:
			if can_buy_province(money, env.money_map):
				return 5
			else:
				return self.buy_best_money_card(env.money_map, env.card_counts, money, deck, hand, discard)

		if self.strategy_mode == 2:
			return buy_best_vp_card(env.money_map, env.card_counts, money)

		# buy nothing
		return -1

	def update_strategy_mode(self, card_counts, deck, hand, discard):
		# if two or less provinces, transition to 2
		if card_counts[5] <= 2:
			return 2

		# if two piles are out, transition to 2
		piles_out = 0
		for i in card_counts:
			if i == 0:
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
		if card_counts[2] == 0:
			return 1

		return 0

	def buy_best_money_card(self, money_map, card_counts, money, deck, hand, discard):
		if money >= money_map[2] and card_counts[2] > 0:
			return 2
		if money >= money_map[1] and card_counts[1] > 0 and average_money_in_total(deck, hand, discard) <= self.dont_buy_silver_past_coin_average_in_deck:
			return 1
		return -1 # dont buy copper dummy

def buy_best_vp_card(money_map, card_counts, money):
	if can_buy_province(money, money_map):
		return 5
	if money >= money_map[4] and card_counts[4] > 0:
		return 4
	if money >= money_map[3] and card_counts[3] > 0:
		return 3
	return -1 # dont buy curses dummy


def can_buy_province(money, money_map):
	return money >= money_map[5]

# not used, but probably good to have
def average_money_in_deck(deck, hand, discard):
	return (money_in_object(deck) / num_cards_i_got(deck, hand, discard)) * 5

def average_money_in_total(deck, hand, discard):
	return ((money_in_object(deck) + money_in_object(discard) + money_in_object(hand)) / num_cards_i_got(deck, hand, discard)) * 5

def money_in_object(array):
	return array[0] + array[1]*2 + array[2]*3

def num_cards_i_got(deck, hand, discard):
	return sum(deck) + sum(hand) + sum(discard)


