<h1>Dominion AI Competition</h1>

Who can design the best Dominion bots? Each week we will play with a different set of cards. Winners will be mostly graded on winrates with some small adjustment for runtime. Weekly winners will be tracked here.

Rules for the bots: They must be a class with an __init__ method that declares a class variable 'name' that is a string of your bot's name. There must also be a get_moves method with parameters in order: environment(Environment object see class Environment), deck(dictionary type see class PlayGame), hand(dictionary see PlayGame), discard(dictionary see PlayGame), and it must return a string of the card it will purchase.

<h3>Week 1 5/3/2020: Just Base Cards</h3>
1st Place: Kellen with KellenBot001
2nd Place: Joe with JoeBot2

KellenBot001 utilized duchy dancing and extensive ad hoc logic using if statements to edge out the win over JoeBot in week 1! More complex bots did worse this week.

<h3>Week 2 5/10/2020</h3>

New cards: Remodel, Smithy, Moneylender

1st Place: Joe with AdHocStrat8
2nd Place: Kellen with KellenBot002

AdHocStrat8 only bought smithy, usually 2-3 in a game, and utilized priority lists based on a simple function of 'provinces remaining', 'average coin' and 'number actions.' Kellens bot was close, jack tried moneylender but it wasn't good enough, and tom's bot prioritzed silvers over gold...He blamed it on bugs in joe's code.

<h3>Week 3 5/17/2020</h3>

Smithy: banned
New cards: Chapel, Village, Gardens, Witch

1st Place: Joe with HolyWitch
2nd Place: Kellen with KellenBot003

Another neck and neck showdown between Joe and Kellen. KellenBot003 highlighted diverse strategy, even buying gardens and remodels in the right situations, but was barely edged out by HolyWitch's finely tuned parameters.

<h3>Week 4 6/7/2020</h3>

New cards: Moat, Workshop, Militia, Council Room
