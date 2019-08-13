# Q-Learning


## Running the Project
Simply run the python file in the command line in the format # # # X (#). The first three numbers show the location of the goal, forbidden square and wall square respectively. The remaining items in the input, determine the output format. The fourth item is either character “p” or “q”, and if it’s “q”, there will be an additional number at the end. Item “p” refers to printing the optimal policy (?*), and “q” refers to the optimal Q-values (Q*). The board size is 12 squares so all numbers must be in the range (inclusive) 1-12. The starting position is always tile 1.

## Examples
Both using the same board with goal state of 3, a negative value square at 5, and an impassable square at 4. 

This shows the best move in all tiles:
python hw3.py 3 5 4 p

This shows the Q-Values for tile 11:
python hw3.py 3 5 4 q 11

This board is illustrated clearly in the "homework 3.pdf" document. 

## Class context

This class was an Artificial Intelligence class crosslisted as a graduate class. Q-Learning is a  model-free reinforcement learning algorithm. For more information on Q-Learning I simply suggest https://en.wikipedia.org/wiki/Q-learning. Once again I also suggest reviewing the "homework 3.pdf" document for more context on the problem if its unclear. 