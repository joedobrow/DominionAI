class KellenBot001:

	def __init__(self):

		self.name = "KellenBot001"

	def get_moves(self, env, deck, hand, discard):

		money = hand['copper'] + hand['silver'] * 2 + hand['gold'] * 3
		moves = []
		for card in env.card_map.keys():
			if (money >= env.card_map[card]['cost']) and env.card_map[card]['supply'] > 0:
				moves.append(card)

		CardsInDeck = deck['gold'] + deck['silver'] + deck['copper'] + deck['province'] + deck['duchy'] + deck['estate'] + deck['curse']

		provinces = env.card_map['province']['supply']
		duchies = env.card_map['duchy']['supply']
		estates = env.card_map['estate']['supply']

		MyProvinces = hand['province'] + deck['province'] + discard['province']
		MyDuchies = hand['duchy'] + deck['duchy'] + discard['duchy']
		MyEstates = hand['estate'] + deck['estate'] + discard['estate']
		MyVPs = (MyProvinces*6) + (MyDuchies*3) + MyEstates

		OppProvinces = provinces - MyProvinces
		OppDuchies = duchies - MyDuchies
		OppEstates = estates - MyEstates
		OppVPs = (OppProvinces*6) + (OppDuchies*3) + OppEstates
		
		VPs = MyVPs - OppVPs

		MyGold = hand['gold'] + deck['gold'] + discard['gold']

		if (provinces > 4) and ('province' in moves) and (MyGold > 1):
			return 'province'

		if (provinces == 5) and (MyDuchies <= OppDuchies) and ('duchy' in moves):
			return 'duchy'

		if (provinces > 4) and 'gold' in moves:
			return 'gold'

		if (provinces > 4) and 'silver' in moves:
			return 'silver'

		if (provinces > 2) and (provinces <= 4) and ('province' in moves):
			return 'province'

		if (provinces == 4) and (CardsInDeck <= 5) and ('gold' in moves):
			return 'gold'

		if (provinces > 2) and (provinces <= 4) and ('duchy' in moves):
			return 'duchy'

		if (provinces > 2) and (provinces <= 4) and (CardsInDeck <= 5) and ('silver' in moves):
			return 'silver'

		if (provinces > 2) and (provinces <= 4) and ('estate' in moves):
			return 'estate'

		if (provinces == 2) and (VPs <= -3 or VPs >= 0) and ('province' in moves):
			return 'province'

		if (provinces == 2) and ('duchy' in moves):
			return 'duchy'

		if (provinces == 2) and ('province' in moves):
			return 'province'

		if (provinces == 2) and ('estate' in moves):
			return 'estate'

		if (provinces <= 1) and (VPs >= -6) and ('province' in moves):
			return 'province'

		if (provinces <= 1) and ('duchy' in moves):
			return 'duchy'

		if (provinces <= 1) and ('province' in moves):
			return 'province'

		if (provinces <= 1) and ('estate' in moves):
			return 'estate'
