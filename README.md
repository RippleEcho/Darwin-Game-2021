# Darwin-Game-2021

original inspiration's post: https://www.lesswrong.com/s/GcZCMu7ZYHpJCh5bx/p/CnDsQAdzmDMF2LrY7


What is the game? Evolution!

Simple bots compete over limited resources, balancing competition and cooperation to survive and thrive
The tournament will place all bots into a free-for-all contest to determine which comes out on top
It's a modified version of a modified version of the iterated prisoner's dillema 

*HOW IT WORKS*

A Match consists of 128±16 Turns between two bots. 
Each turn, 7 points are available to split between them.

Each turn, each bot must output a pair of integers each ranging from 0 to 7
The first integer is their claim on the point pool.
The second integer is their veto for their opponent.
For input, bots will have access to all moves for both bots made in this Match, and can act accordingly

Turn scoring works as follows:
 1) If the sum of the claims is greater than 7, BOTH bots score zero this turn
 2) If a bot's claim matches it's oppnent's veto, that bot scores zero this turn
 3) Otherwise, a bot will score its claim this turn
 
 Score accumulates over the match. 
 
 NOW A LAYER OF META
 Each bot starts with 256 copies of itself in the bot pool
 Matches are randomly assigned, and bots can fight other copies of themselves!
 
 POINTS ARE SUMMED ACROSS ALL COPIES OF A BOT PER ROUND
 This means cooperating with itself might be advantageous!
 
 NOW ANOTHER LAYER OF META
 Each round, the bot pool is adjusted to be proportional to the total score from the previous round.
 Bots that accumulate more points will then have more copies next round
 The tournament will have 256 rounds 
 
 The winner is the bot with the most copies of itself at the end of the final round
 
 
 *HOW TO SUBMIT A BOT*
 All I need is a python file with a function with correct inputs and outputs. 
 Inputs: Two lists of tuples (own_moves, opp_moves) with {move format: (claim, veto)}
 Output: One tuple with this turn's move {format: (claim, veto)}
  See example bots for more clarity
  Send me your code over discord in either .txt or .py files
 If you need help putting your bot together, ask around or let me know! 
  If need be, send me a .txt file with the pseudo code. I won't write your bot for you, but I can work with you.
  
  Send this to me over discord preferably
 
 
 
 
