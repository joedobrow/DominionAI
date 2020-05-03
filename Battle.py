# git status
# git commit -a -m'message'
# git push

import random
import Environment
import ExampleBot
import MoneyBot
import PlayGame

iterations = 1
score = [0, 0]
bot1 = ExampleBot.ExampleBot()
bot2 = MoneyBot.MoneyBot()
for i in range(iterations):
    x = PlayGame.PlayGame(bot1, bot2, verbose=3)
    result = x.play_game()
    if result == 1:
        score[0] += 1
    else:
    	score[1] += 1

print('\n{}'.format(score))
        
if score[1] > score[0]:
    print('{} wins! with {}% WR.'.format(bot2.name, score[1]*100/iterations))
elif score[1] < score[0]:
    print('{} wins! {}% WR.'.format(bot1.name, score[0]*100/iterations))
else:
    print('Tie!')
print(bot1.name, 'runtime:', x.bot1_runtime)
print(bot2.name, 'runtime:', x.bot2_runtime)
print('\nRemaining cards:')
if x.verbose > 1:
	for card in x.env.card_map.keys():
		print(card, x.env.card_map[card]['supply'])