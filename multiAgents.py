# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        ghost_pos = childGameState.getGhostPositions()  #get ghost position every time
        ghost_dist=[]
        for i in range(len(ghost_pos)):
            ghost_distance = manhattanDistance(newPos, ghost_pos[i])  # calculate distance from the ghost to pacman
            ghost_dist.append(ghost_distance)
        all_food = newFood.asList()  #collect all food positions into a list
        food_dist = []
            
        for i in range(len(all_food)):   #calculate distance from pacman to every avalaible food
            dist =  manhattanDistance(newPos, all_food[i])
            food_dist.append(dist)
        if food_dist:   
            return childGameState.getScore()-max(food_dist)-0.01*min(food_dist)+min(ghost_dist)
        if newScaredTimes[0]!=0 and food_dist:
            return childGameState.getScore()-max(food_dist)-0.01*min(food_dist)

        return childGameState.getScore()+min(ghost_dist)



def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose(): 
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        minimax = self.max_value(gameState,0,0)    #since root is Pacman call get_max for AgentIndex=0 and depth=0
        return minimax[1]   #return minimax move


    def max_value(self, gameState,agentIndex,depth):

        v = float('-inf')    
        if gameState.isWin() or gameState.isLose() or depth==self.depth: #check if termination state is reached
            return self.evaluationFunction(gameState),""

        next_actions = gameState.getLegalActions(agentIndex)

        for next_action in next_actions:
            v2, a2 = self.min_value(gameState.getNextState(agentIndex,next_action),agentIndex+1,depth)
            if v2 > v:
                v,move = v2,next_action
        return v, move

    def min_value(self, gameState,agentIndex,depth):
        
        v = float('inf')
        if gameState.isWin() or gameState.isLose() or depth == self.depth:   #check if termination state is reached
            return self.evaluationFunction(gameState),""

        next_actions = gameState.getLegalActions(agentIndex)
        for next_action in next_actions:
            if agentIndex == gameState.getNumAgents()-1:  #check if next agent is packman
                v2, a2 = self.max_value(gameState.getNextState(agentIndex,next_action),0,depth+1)
            else:       #check if next agent in another ghost
                v2, a2 = self.min_value(gameState.getNextState(agentIndex,next_action),agentIndex+1,depth)
            if v2 < v:
                v,move = v2,next_action
        return v, move
    
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"        
        a = float('-inf')
        b = float('inf')
        minimax = self.max_value(gameState,0,0,a,b)    #since root is Pacman call get_max for AgentIndex=0 and depth=0
        return minimax[1]  #return minimax move


    def max_value(self, gameState,agentIndex,depth,a,b):

        v = float('-inf')    
        if gameState.isWin() or gameState.isLose() or depth==self.depth: #check termination state is reached
            return self.evaluationFunction(gameState),""

        next_actions = gameState.getLegalActions(agentIndex)

        for next_action in next_actions:
            v2, a2 = self.min_value(gameState.getNextState(agentIndex,next_action),agentIndex+1,depth,a,b)
            if v2 > v:
                v,move = v2,next_action
                a=max(a,v)
            if v > b:
                return v,move
        return v, move

    def min_value(self, gameState,agentIndex,depth,a,b):
        
        v = float('inf')

        if gameState.isWin() or gameState.isLose() or depth == self.depth:   #check if termination state is reached
            return self.evaluationFunction(gameState),""

        next_actions = gameState.getLegalActions(agentIndex)
        for next_action in next_actions:
            if agentIndex == gameState.getNumAgents()-1:  #check if next agent is packman
                v2, a2 = self.max_value(gameState.getNextState(agentIndex,next_action),0,depth+1,a,b)
            else:                       #check if next agent in another ghost
                v2, a2 = self.min_value(gameState.getNextState(agentIndex,next_action),agentIndex+1,depth,a,b)
            if v2 < v:
                v,move = v2,next_action
                b = min(b,v)
            if v<a:
                return v,move
        return v, move
    

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
    
        minimax = self.max_value(gameState,0,0)    #since root is Pacman call get_max for AgentIndex=0 and depth=0
        return minimax[1]   #return the expectimax move 


    def max_value(self, gameState,agentIndex,depth):

        v = float('-inf')    
        if gameState.isWin() or gameState.isLose() or depth==self.depth: #check if termination state is reached
            return self.evaluationFunction(gameState),""

        next_actions = gameState.getLegalActions(agentIndex)

        for next_action in next_actions:  
            v2, a2 = self.chance_value(gameState.getNextState(agentIndex,next_action),agentIndex+1,depth)
            if v2 > v:
                v,move = v2,next_action
        return v, move

    def chance_value(self, gameState,agentIndex,depth):
        
        v = 0
        if gameState.isWin() or gameState.isLose() or depth == self.depth:   #check if termination state is reached
            return self.evaluationFunction(gameState),""

        next_actions = gameState.getLegalActions(agentIndex)
        for next_action in next_actions:
            p = 1 / len(next_actions)  #calculate the current propability for the actions of this agent
            if agentIndex == gameState.getNumAgents()-1:  #check if next agent is packman
                v +=p* self.max_value(gameState.getNextState(agentIndex,next_action),0,depth+1)[0]   #calculate the sum of all utility values multiplied by the probability
                move =self.max_value(gameState.getNextState(agentIndex,next_action),0,depth+1)[1]
            else:                       #check if next agent in another ghost
                v+=p*self.chance_value(gameState.getNextState(agentIndex,next_action),agentIndex+1,depth)[0]       #calculate the sum of all utility values multiplied by the probability
                move=self.chance_value(gameState.getNextState(agentIndex,next_action),agentIndex+1,depth)[1] 

        return v, move
        
        

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    childGameState = currentGameState  
    newPos = childGameState.getPacmanPosition()
    newFood = childGameState.getFood()
    newGhostStates = childGameState.getGhostStates()        
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    

    ghost_pos = childGameState.getGhostPositions()  #get ghost position every time
    ghost_dist=[]
    for i in range(len(ghost_pos)):
        ghost_distance = manhattanDistance(newPos, ghost_pos[i])  # calculate distance from the ghost to pacman
        ghost_dist.append(ghost_distance)

    all_food = newFood.asList()  #collect all food positions into a list
    food_dist = []
    for i in range(len(all_food)):   #calculate distance from pacman to every avalaible food
        dist =  manhattanDistance(newPos, all_food[i])
        food_dist.append(dist)
    if newScaredTimes[0]==0 and food_dist:   
        return childGameState.getScore()-max(food_dist)-0.01*min(food_dist)+min(ghost_dist)
    elif newScaredTimes[0]!=0 and food_dist:
        return childGameState.getScore()-max(food_dist)-0.01*min(food_dist)+min(ghost_dist)+newScaredTimes[0]*0.5

    return childGameState.getScore()+min(ghost_dist)

    

# Abbreviation
better = betterEvaluationFunction
