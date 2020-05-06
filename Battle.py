# git status
# git commit -a -m'message'
# git push

import random
import Environment
import PlayGame
import GUI
import JoeBotw2

verbose = 0
avg_turn_win = [0, 0]

if verbose > 0:
	iterations = 1
else:
	iterations = 1000
score = [0, 0]

bots = [JoeBotw2.TrainedBot4(), JoeBotw2.TrainedBot5()]

for i in range(iterations):
    x = PlayGame.PlayGame(bots[0], bots[1], verbose=verbose)
    result = x.play_game()
    score[result[0]] += 1
    avg_turn_win[result[0]] += result[1]

if score[1] > score[0]:
	winner_name = bots[1].name
elif score[1] < score[0]:
	winner_name = bots[0].name
else:
	winner_name = 'error'

if verbose == 2:
	y = GUI.CreateGUI(result[2], result[3], result[4], result[5], bot1.name, bot2.name, winner_name)
elif verbose == 1:
	for move in range(len(result[2]) + 1):
		try:
			print(result[2][move], result[3][move])
		except:
			None

if score[0] > 0:
	avg_turn_win[0] /= score[0]
else:
	avg_turn_win[0] = 'SHUT OUT'
if score[1] > 0:
	avg_turn_win[1] /= score[1]
else:
	avg_turn_win[1] = 'SHUT OUT'


print('\n{}'.format(score))
        
if score[1] > score[0]:
    print('{} wins! with {}% WR.'.format(bots[1].name, score[1]*100/iterations))
elif score[1] < score[0]:
    print('{} wins! {}% WR.'.format(bots[0].name, score[0]*100/iterations))
else:
    print('Tie!')
print(bots[0].name, 'average turn win:', avg_turn_win[0])
print(bots[1].name, 'average turn win:', avg_turn_win[1])

if x.verbose > 1:
	print('\nRemaining cards:')
	for card in x.env.card_map.keys():
		print(card, x.env.card_map[card]['supply'])