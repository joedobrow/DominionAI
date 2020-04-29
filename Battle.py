# git status
# git commit -a -m'message'
# git push

import random
import Environment
import ExampleBot
import PlayGame

iterations = 1000
score = [0, 0]
bot1 = ExampleBot.ExampleBot()
bot2 = ExampleBot.ExampleBot()
for i in range(iterations):
    x = PlayGame.PlayGame(bot1, bot2)
    x = x.play_game()
    if x == 1:
        score[0] += 1
    else:
    	score[1] += 1

print(score)
        
if score[1] > score[0]:
    print('{} wins! with {}% WR.'.format(bot2.name, score[1]*100/iterations))
elif score[1] < score[0]:
    print('{} wins! {}% WR.'.format(bot1.name, score[0]*100/iterations))
else:
    print('Tie!')