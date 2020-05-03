import ReinforcedBot
import ExampleBot
import random
import Environment
import PlayGame

enemy = ExampleBot.ExampleBot()

bot1 = ReinforcedBot.ReinforcedBot()
bot1.train_main()

iterations = 1000
score = [0, 0]
bot2 = ExampleBot.ExampleBot()
for i in range(iterations):
    x = PlayGame.PlayGame(bot1, bot2, verbose=0)
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

print(bot1.model_test(8, 6, .5, 20))