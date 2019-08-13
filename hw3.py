import sys
import random as rand

class Square:
  def __init__(self, index, sq_type):
    self.index = index
    self.sq_type = sq_type
    self.qvalN = 0
    self.qvalS = 0
    self.qvalE = 0
    self.qvalW = 0

  def qmax(self):
    return max(self.qvalN, self.qvalS, self.qvalE, self.qvalW)

  def best_action(self): 
    qvals = [self.qvalN, self.qvalS, self.qvalE, self.qvalW]
    actions = ['N', 'S', 'E', "W"]
    return(actions[qvals.index(max(qvals))])
  
  def best_action_index(self):
    qvals = [self.qvalN, self.qvalS, self.qvalE, self.qvalW]
    return qvals.index(max(qvals))
  
  def getq(self, action):
    actions = ['N', 'S', 'E', "W"]
    qvals = [self.qvalN, self.qvalS, self.qvalE, self.qvalW]
    return(qvals[actions.index(action)])
  
  def reward(self):
    if (self.sq_type == 'goal'):
      return 100
    elif (self.sq_type == 'forbidden'):
      return -100
    else:
      return 0
  
  def qupdate(self, action, q):
    if action == 'N':
      self.qvalN = q
    elif action == "S":
      self.qvalS = q
    elif action == "E":
      self.qvalE = q
    elif action == "W":
      self.qvalW = q
  
  def qprint(self):
    print("      " + "{0:.2f}".format(self.qvalN))
    print("       ↑")
    print("{0:.2f}".format(self.qvalW) + " ← " + (str(self.index)) + " → " + "{0:.2f}".format(self.qvalE))
    print("       ↓")
    print("      " + "{0:.2f}".format(self.qvalS))

   
class Agent:
  def __init__(self, board):
    self.location = 1 #index of the current position of the agent
    self.board = board #list of size 12 of type Square
    self.alpha = 0.1 #learning rate
    self.gamma = 0.5 #discount rate
    self.epsilon = 0.1 # probability of acting optimally
    self.living_reward = -0.1
    self.turns_lived = 0

  # reward end = 100, forbidden = -100, turn  = -0.1
  def update(self):
    while(self.board[self.location].sq_type != "goal" and self.board[self.location].sq_type != "forbidden"):
      # Determines what action to take using its epsilon value
      act_randomly = True
      r = rand.randint(0,99)
      if self.epsilon is 0:
        act_randomly = False
        if (r % (self.epsilon * 100) == 0):
            act_randomly = False
      action = None
      loc = self.board[self.location]
      if (act_randomly):
        action = rand.choice(['N', 'S', 'E', 'W'])
      else:
        action = loc.best_action()

      # Take determined action
      self.move(action)
      new_loc = self.board[self.location]
    
      # Uses Bellman equation to update q
      self.turns_lived +=1
      reward = new_loc.reward() + self.turns_lived * self.living_reward
      currentq = new_loc.getq(action)

      q = currentq + self.alpha * (reward + self.gamma * new_loc.qmax() - currentq)
      loc.qupdate(action, q)
      

  def move(self, action):
    if (action is "N"):
      if (self.location < 9):
        if (self.board[self.location + 4].sq_type is not "wall"):
          self.location = self.location + 4
    if (action is "S"):
      if (self.location > 4):
        if (self.board[self.location - 4].sq_type is not "wall"):
          self.location = self.location - 4
    if (action is "E"):
      if (self.location % 4 != 0):
        if (self.board[self.location + 1].sq_type is not "wall"):
          self.location += 1
    if (action is "W"):
      if (self.location % 4 != 1):
        if (self.board[self.location - 1].sq_type is not "wall"):
          self.location -= 1

def print_optimal(board, wall_index, end_index):
  action_symbols = ['↑', '↓', '→', '←']
  print("┏━━━┳━━━┳━━━┳━━━┓")
  for j in range(0, 3):
    for i in range(9-4*j, 13-4*j):
      main_str = (action_symbols[board[i].best_action_index()])
      if (wall_index == i):
        main_str = 'X'
      elif(end_index == i):
        main_str = '☺'
      print("┃" + (str(i) + main_str).ljust(3), end="")
    print("┃")
    if (j != 2):
      print("┣━━━╋━━━╋━━━╋━━━┫")
  print("┗━━━┻━━━┻━━━┻━━━┛")

def main():
  ## INPUT VALIDATION BEGIN ##
  if (len(sys.argv) != 5 and len(sys.argv) != 6):
    print("INVALID INPUT ERROR: Valid Format is: # # # X (#)")
    return
  for i in range(1, 4):
    if (sys.argv[i].isdigit() is False):
      print("INVALID INPUT ERROR: Arguments 1, 2, 3 must be integers")
      return
    elif (int(sys.argv[i]) < 2 or int(sys.argv[i]) > 12):
      print("INVALID INPUT ERROR: Arguments 1, 2, & 3 must be in range [2, 12]")
      return
  if (sys.argv[4] != 'p' and sys.argv[4] != 'q'):
    print("INVAID INPUT ERROR: Argument 4 must be either 'p' or 'q'")
  elif(sys.argv[4] is 'q' and len(sys.argv) != 6):
    print("INVALID INPUT ERROR: When Argument 4 is 'q' there needs to be 5 arguments")
  if (len(sys.argv) == 6):
    if (sys.argv[4] == 'p'):
      print("INPUT WARNING: Argument 5 is ignored when Argument 4 is 'p'")
    elif (sys.argv[5].isdigit() is False):
      print("INVALID INPUT ERROR: Argument 5 must be an integer")
      return
  ## INPUT VALIDATION END ##

  ## BOARD SETUP START ##
  # Assuming valid board configuration from instructor comment on piazza 
  board = [Square(0, 'dummy')] # dummy square so indexes start at 1 to match directions
  board.append(Square(1, "start"))
  for i in range(2,13):
    board.append(Square(i, "ordinary"))
  board[int(sys.argv[1])].sq_type = "goal"
  board[int(sys.argv[2])].sq_type = "forbidden"
  board[int(sys.argv[3])].sq_type = "wall"
  ## BOARD SETUP END ##

  ## START ##
  i = 0
  curr = 0
  prev = 0
  while (i != 10000):
    agent = Agent(board)
    agent.update()
    i += 1

  if (sys.argv[4] == 'p'):
    print_optimal(board, int(sys.argv[3]), int(sys.argv[1]))
  elif (sys.argv[4] == 'q'):
    board[int(sys.argv[5])].qprint()
  ## END ##
if __name__ == "__main__":
    main()