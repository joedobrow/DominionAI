# git status
# git commit -a -m'message'
# git push

import random
import Environment
import ExampleBot
import TomBot
import PlayGame

iterations = 1
score = [0, 0]
avg_turn_win = [0,0]
bot1 = TomBot.TomBot()
bot2 = TomBot.TomBot()
for i in range(iterations):
    x = PlayGame.PlayGame(bot1, bot2)
    x = x.play_game()
    if x[0] == 1:
        score[0] += 1
        if x[1]:
        	avg_turn_win[0] += x[1]
    else:
    	score[1] += 1
    	if x[1]:
    		avg_turn_win[1] += x[1]
if (score[0] > 0):
	avg_turn_win[0] /= score[0]
if (score[1] > 0):
	avg_turn_win[1] /= score[1]

print('\n{}'.format(score))
        
if score[1] > score[0]:
    print('{} wins! with {}% WR.'.format(bot2.name, score[1]*100/iterations))
    print('{} average turn to win: {}'.format(bot2.name, avg_turn_win[1]))
elif score[1] < score[0]:
    print('{} wins! {}% WR.'.format(bot1.name, score[0]*100/iterations))
    print('{} average turn to win: {}'.format(bot1.name, avg_turn_win[0]))
else:
    print('Tie!')
print(bot1.name, 'runtime:', x.bot1_runtime)
print(bot2.name, 'runtime:', x.bot2_runtime)
print('\nRemaining cards:')
if x.verbose > 1:
	for card in x.env.card_map.keys():
		print(card, x.env.card_map[card]['supply'])