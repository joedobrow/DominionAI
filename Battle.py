# - - - - - - - - IMPORTS - - - - - - - - - - - - - - - -

import random
import copy

import Environment
import PlayGame
import GUI
import BaseBot
import JoeBotW5

# - - - -  - - - -CHANGE THESE VARIABLES - - - - - - - - -
# verbose 0: display  score, runtime, average VP, and turn win over multiple games
# verbose 1: display all of the moves for 1 game
# verbose 2: turn by turn
# verbose 3: GUI (BROKEN)

verbose = 1
num_games = 100

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

cards = {
	'copper' : 0,
	'silver' : 0,
	'gold' : 0,
	'estate' : 0,
	'duchy' : 0,
	'province' : 0,
	'curse' : 0,
	'chapel': 0,
	'council_room': 0,
	'gardens': 0,
	'militia': 0,
	'moat': 0,
	'moneylender' : 0,
	'remodel' : 0,
	'village' : 0,
	'witch': 0,
	'workshop': 0
}

base_cards = ['copper', 'silver', 'gold', 'estate', 'duchy', 'province', 'curse']
avg_turn_win = [0, 0]
score = [0, 0]
remodel_trash = [copy.deepcopy(cards), copy.deepcopy(cards)]
remodel_gain = [copy.deepcopy(cards), copy.deepcopy(cards)]
avg_vp = [0, 0]
runtime = [0, 0]


if verbose > 0:
	iterations = 1
else:
	iterations = num_games
this_data = []

for i in range(iterations):

	env = Environment.Environment(4)
	bots = [JoeBotW5.GeneralBot(env.card_map), JoeBotW5.BigMoney(env.card_map)]

	if i == 0:
		print('\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
		print('\t\t\tDOMINION BOT BATTLES')
		print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
		print("\n\n\nBot 1: {}\t\tBot 2: {}".format(bots[0].name, bots[1].name), '\n')

	if verbose > 0:
		print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
		print('Kingdom Cards in Pool:')
		for card in cards:
			if (card not in base_cards) and env.card_map[card]['supply'] > 0:
				print(card)
		print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')

	if verbose == 0:
		if (i%(max(iterations // 10, 1)) == 0):
			print('{} out of {} epochs completed, score: {}'.format(i, iterations, score))

	x = PlayGame.PlayGame(bots[0], bots[1], env, verbose=verbose)
	result = x.play_game()
	
	score[result[0]] += 1
	avg_turn_win[result[0]] += result[4]
	avg_vp[result[0]] += result[2]
	avg_vp[1 - result[0]] += result[3]
	runtime[0] += result[9]
	runtime[1] += result[10]

	
# RESULT KEY:
# 0 - winner 0/1 for bot0 or bot1
# 1 - player that won
# 2 - number of VP of winner
# 3 - VP of loser
# 4 - turn
# 5 - move list of bot0
# 6 - move list of bot1
# 7 - hand list of bot0
# 8 - hand list of bot1
# 9 - runtime of bot0
# 10 - runtime of bot1
# 11 - extra text of bot0 (tells what was remodeled)
# 12 - extra text of bot1
# 13 - handlist post smithy bot0
# 14 - handlist post smithy bot1

if verbose == 3:
	y = GUI.CreateGUI(
			result[5], 
			result[6], 
			result[7], 
			result[8], 
			result[13], 
			result[14], 
			result[11], 
			result[12], 
			bots[0].name, 
			bots[1].name, 
			bots[result[0]].name
	)
if verbose == 1:
	print("\n\n\nBot 1: {}\t\tBot 2: {}".format(bots[0].name, bots[1].name), '\n')
	print('\n\t\tMOVE LIST:')
	print('\nStarting player: {}'.format(bots[result[1]].name))
	for move in range(len(result[5])):
		to_print = ''
		for i in result[5][move]:
			to_print += str(i) + ' '
		to_print += '      '
		if move < len(result[6]):
			for i in result[6][move]:
				to_print += str(i) + ' '
		print(to_print)
	if len(result[6]) > len(result[5]):
		to_print = ''
		for i in result[6][-1]:
			to_print += str(i) + ' '
		print(to_print)

print('\n\t\tFINAL SCORE:')
print(score)
if score[1] > score[0]:
	winner_name = bots[1].name
elif score[1] < score[0]:
	winner_name = bots[0].name
else:
	winner_name = 'Tie'
print('{} Wins!!!'.format(winner_name))
print('%{} winrate'.format(100 * max(score[0]/(score[1] + score[0]), score[1]/(score[1] + score[0]))))
print('\n\t\tRUNTIME:')
print(bots[0].name, runtime[0])
print(bots[1].name, runtime[1])

print('\n\t\tAVERAGE VP:')
print(bots[0].name, avg_vp[0]/iterations)
print(bots[1].name, avg_vp[1]/iterations)

print('\n\t\tAVERAGE TURN WIN:')
if score[0] > 0:
	avg_turn_win[0] /= score[0]
else:
	avg_turn_win[0] = 'SHUT OUT'
if score[1] > 0:
	avg_turn_win[1] /= score[1]
else:
	avg_turn_win[1] = 'SHUT OUT'
print(bots[0].name, avg_turn_win[0])
print(bots[1].name, avg_turn_win[1])

if sum(remodel_trash[0].values()) > 0 or sum(remodel_trash[1].values()) > 0:
	print('\n\t\tREMODEL STATS:')
	print(bots[0].name, 'Trashed map:', remodel_trash[0])
	print('Gained map:', remodel_gain[0])
	print(bots[1].name, 'Trashed map:', remodel_trash[1])
	print('Gained map:', remodel_gain[1])

if verbose == 1:
	print('\nRemaining cards:')
	for card in x.env.card_map:
		print(card, x.env.card_map[card]['supply'])

