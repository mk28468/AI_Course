# multiAgents.py
# --------------THIS CODE IS MY OWN WORK, IT WAS WRITTEN WITHOUT CONSULTING
#			A TUTOR OR CODE WRITTEN BY OTHER STUDENTS - Junyuan Ke 2148073
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
#
# Modified by Eugene Agichtein for CS325 Sp 2014 (eugene@mathcs.emory.edu)
#

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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
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

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where "higher numbers are better."

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        Note that the successor game state includes updates such as available food,
        e.g., would *not* include the food eaten at the successor state's pacman position
        as that food is no longer remaining.
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()

        currentCapsules=currentGameState.getCapsules() #power pellets/capsules available from current state
        newCapsules=successorGameState.getCapsules() #capsules available from successor (excludes capsules@successor)
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"

        currentFood = currentGameState.getFood()  # food available from current state
        cf = currentFood.asList()
        newFood = successorGameState.getFood()  # food available from successor state (excludes food@successor)
        nf = newFood.asList()
        GhostPosition = successorGameState.getGhostPositions()
        score = 0
        """
        I want to first consider getting away from ghosts as far as possible
        if the dist to closest ghost is smaller than 3, then we should definately not go there
        else, we decrease 10 in score everytime
        """
        ghostDistance = []
        for ghostPos in GhostPosition:
            ghostDistance.append(manhattanDistance(ghostPos, newPos))
        minGhostDist = min(ghostDistance)
        if minGhostDist < 3:
            return -999
        i = minGhostDist
        while (i != 0):
            score -= 10
            i -= 1
        """
        After considering ghosts, we would like to get as near to food as possible.
        if successor position is food, try to eat it.
        """
        if len(cf) == len(nf) + 1 :
            return 999
        nextFood = []
        for food in nf:
            nextFood.append(manhattanDistance(food, newPos))
        minFoodDist = min(nextFood)
        score = -minFoodDist
        return score

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
            getAction takes a GameState and returns
            some Directions.X for some X in the set {North, South, West, East, Stop}
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            $$$agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game, 0, 1, 2 in this case
        """

        "*** YOUR CODE HERE ***"
        v = -99999

        dep = 0
        ghostag = 1
        # if next is max, return max
        #if next is min, return min
        #for here, self.depth = 2
        for action in gameState.getLegalActions(0):  #actions of pacman
            eval = self.minvalue(dep, ghostag, gameState.generateSuccessor(0, action)) #depth=0; agent=1; state = successor of pacman
            if action != Directions.STOP:
                if v < eval:
                    v = eval
                    nextAct = action

        return nextAct

    def minvalue(self, depth, agent, successor):
        # if terminal state, return state's utility

        if depth != self.depth: #if haven't reach depth 2
            actions = successor.getLegalActions(agent)
            if len(actions) > 0:
                v = 99999
            else:
                v = self.evaluationFunction(successor)

            for action in actions:
                numAg = successor.getNumAgents()
                if agent ==  numAg - 1: #ghost 2, or last ghost
                    score = self.maxvalue(depth + 1, 0, successor.generateSuccessor(agent, action)) #depth=1; agent=0; succ of action
                else:
                    score = self.minvalue(depth, agent + 1, successor.generateSuccessor(agent, action))
                if score < v:
                    v = score
            return v
        else:       #if reaches depth 2
            currstate = self.evaluationFunction(successor)
            return currstate

    def maxvalue(self, depth, agent, successor):
        """
        initialize v = -inifnity
        for	each	successor	of	state:
        v	=	max(v,	min-value(successor))
        return	v
        """
        if depth != self.depth:
            actions = successor.getLegalActions(agent)
            if len(actions) > 0:
                v = -99999
            else:
                v = self.evaluationFunction(successor)

            for action in actions:
                score = self.minvalue(depth, agent + 1, successor.generateSuccessor(agent, action))
                if score > v:
                    v = score
            return v
        else:       #if reaches depth 2
            currstate = self.evaluationFunction(successor)
            return currstate


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        v = -99999
        a = -99999
        b = 99999
        nextAct = Directions.STOP
        dep = 0
        ghostag = 1
        # if next is max, return max
        # if next is min, return min
        # for here, self.depth = 2
        for action in gameState.getLegalActions(0):  # actions of pacman
            eval = self.minvalue(a, b, dep, ghostag, gameState.generateSuccessor(0, action))  # depth=0; agent=1; state = successor of pacman
            if action != Directions.STOP:
                if v < eval:
                    v = eval
                    nextAct = action
            a = max(a, eval)
        return nextAct

    def maxvalue(self, alpha, beta, depth, agent, successor):
        """
        initialize v = -inifnity
        for	each	successor	of	state:
        v	=	max(v,	min-value(successor))
        return	v
        """
        if depth != self.depth:
            actions = successor.getLegalActions(agent)
            if len(actions) > 0:
                v = -99999
            else:
                v = self.evaluationFunction(successor)

            for action in actions:
                v = max(self.minvalue(alpha, beta, depth, agent + 1, successor.generateSuccessor(agent, action)), v)
                if v > beta:
                    return v
                alpha = max(v, alpha)
            return v
        else:  # if reaches depth 2
            currstate = self.evaluationFunction(successor)
            return currstate

    def minvalue(self, alpha, beta, depth, agent, successor):
        # if terminal state, return state's utility

        if depth != self.depth:  # if haven't reach depth 2
            actions = successor.getLegalActions(agent)
            if len(actions) > 0:
                v = 99999
            else:
                v = self.evaluationFunction(successor)

            for action in actions:
                numAg = successor.getNumAgents()
                if agent == numAg - 1:  # ghost 2, or last ghost
                    v = min(self.maxvalue(alpha, beta, depth + 1, 0, successor.generateSuccessor(agent,action)), v)
                else:
                    v = min(self.minvalue(alpha, beta, depth, agent + 1, successor.generateSuccessor(agent, action)), v)
                if v < alpha:
                    return v
                beta = min(beta, v)
            return v
        else:  # if reaches depth 2
            currstate = self.evaluationFunction(successor)
            return currstate


        util.raiseNotDefined()

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
        v = -99999

        #nextAction = Directions.STOP
        for action in gameState.getLegalActions(0):
            eval = self.expectedvalue(0, 1, gameState.generateSuccessor(0, action))
            if action != Directions.STOP  :
                if eval > v:
                    v = eval
                    nextAct = action
        return nextAct

    def maxValue(self, depth, agent, state):

        if depth == self.depth:
            currstate = self.evaluationFunction(state)
            return currstate
        if depth != self.depth:
            actions = state.getLegalActions(agent)
            if len(actions) > 0:
                v = -99999
            else:
                currstate = self.evaluationFunction(state)
                v = currstate
            for action in actions:
                v = max(self.expectedvalue(depth, agent + 1, state.generateSuccessor(agent, action)),v)
        return v

    def expectedvalue(self, depth, agent, state):

        if depth != self.depth:
            v = 0
            actions = state.getLegalActions(agent)
            for action in actions:
                numAg = state.getNumAgents()
                if agent != numAg - 1:
                    v += self.expectedvalue(depth, agent + 1, state.generateSuccessor(agent, action))
                else:
                    v += self.maxValue(depth + 1, 0, state.generateSuccessor(agent, action))
            if len(actions) != 0:
                return v / len(actions)
            else:
                currstate = self.evaluationFunction(state)
                return currstate
        else:
            currstate = self.evaluationFunction(state)
            return currstate

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    score = currentGameState.getScore()
    nextGhost = 99999
    nextFood = 99999
    nextPellet = 99999
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    for ghost in range(len(newGhostStates)):
        ghostDist = manhattanDistance(newPos, currentGameState.getGhostPosition(ghost + 1))
        if nextGhost > ghostDist :
            nextGhost = ghostDist
        if nextGhost == 0:
            nextGhost = 99999

    for pellet in currentGameState.getCapsules():
        nextPellet = min(nextPellet, manhattanDistance(newPos, pellet))
        if nextPellet == 0:
            nextPellet = 99999

    for food in newFood.asList():
        nextFood = min(nextFood, manhattanDistance(newPos, food))
        if nextFood == 0:
            nextFood = 99999

    timescore = 0
    for sctime in newScaredTimes:
        timescore = timescore + sctime
    score += timescore

    ghostscore = 10.0 / nextGhost
    foodscore = 10.0 / nextFood
    pelletscore = 10.0 / nextPellet

    totalscore = score + timescore + ghostscore + foodscore + pelletscore
    #return totalscore
    return score + 10.0 / nextGhost + 10.0 / nextFood + 10.0 / nextPellet

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

