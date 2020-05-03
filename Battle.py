# git status
# git commit -a -m'message'
# git push

import random
import Environment
import ExampleBot
import PlayGame
import KellenBot01
import GUI
import JoeBot
#import ReinforcedBot

verbose = 0
p1_avg_turn_win, p2_avg_turn_win = 0, 0
if verbose > 0:
	iterations = 1
else:
	iterations = 20000
score = [0, 0]
bot1 = JoeBot.JoeBot25()
bot2 = JoeBot.JoeBot2()
for i in range(iterations):
    x = PlayGame.PlayGame(bot1, bot2, verbose=verbose)
    result = x.play_game()
    if result[0] == 1:
        score[0] += 1
        p1_avg_turn_win += result[1]
    else:
    	score[1] += 1
    	p2_avg_turn_win += result[1]
if score[1] > score[0]:
	winner_name = bot2.name
elif score[1] < score[0]:
	winner_name = bot1.name
else:
	winner_name = 'error'
if verbose == 2:
	y = GUI.CreateGUI(result[2], result[3], result[4], result[5], bot1.name, bot2.name, winner_name)
if score[0] > 0:
	p1_avg_turn_win /= score[0]
else:
	p1_avg_turn_win = 'SHUT OUT'
if score[1] > 0:
	p2_avg_turn_win /= score[1]
else:
	p2_avg_turn_win = 'SHUT OUT'


print('\n{}'.format(score))
        
if score[1] > score[0]:
    print('{} wins! with {}% WR.'.format(bot2.name, score[1]*100/iterations))
elif score[1] < score[0]:
    print('{} wins! {}% WR.'.format(bot1.name, score[0]*100/iterations))
else:
    print('Tie!')
print(bot1.name, 'average turn win:', p1_avg_turn_win)
print(bot2.name, 'average turn win:', p2_avg_turn_win)
if x.verbose > 1:
	print('\nRemaining cards:')
	for card in x.env.card_map.keys():
		print(card, x.env.card_map[card]['supply'])