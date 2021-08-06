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


import random

import util
from game import Agent, Directions
from util import manhattanDistance, norm
import numpy as np

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
        norm = self.ghostNorm(gameState, legalMoves)
        scores = [self.evaluationFunction(gameState, action, norm) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action, norm):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        ghostsPos = successorGameState.getGhostPositions()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        foodScore = self.foodScore(currentGameState, action, newPos, 
                                   successorGameState, ghostsPos, newScaredTimes)
        ghostScore = self.ghostScore(currentGameState, action, newPos, 
                                    successorGameState, ghostsPos)
        return foodScore+ghostScore/norm

    def ghostScore(self, currentGameState, action, 
                   newPos, successorGameState, ghostsPos):
      """Busca se afastar do fantasma mais próximo"""
      
      closest = self.closestGhost(newPos, ghostsPos)
      return manhattanDistance(closest, newPos)
      
    def foodScore(self, currentGameState, action, newPos, successorGameState,
                  ghostsPos, newScaredTimes):
      """Busca se aproximar da comida ou capsula mais próxima do pacman e mais
      afastada dos fantasmas. Quando há scaredTimer o comportamento busca e
      o pacman busca alcançar o fantasma assustado mais próximo."""
      actualPos = currentGameState.getPacmanPosition()
      closestFood = self.closestFood(currentGameState, successorGameState, 
                                     newScaredTimes)
      isBetterPos = (manhattanDistance(closestFood, newPos) < 
                    manhattanDistance(closestFood, actualPos))
      return 1 if isBetterPos else 0


    def closestFood(self, currentGameState, successorGameState, newScaredTimes):
      """Calcular a comida mais próxima que está distante dos fantasmas"""
      
      # Checa se há fantasmas assustados
      isScaredTimer = self.anyScaredTimer(newScaredTimes)

      #Obtém posições
      ghostsPos = successorGameState.getGhostPositions()
      actualPos = currentGameState.getPacmanPosition()
      foodPos = currentGameState.getFood().asList() + currentGameState.getCapsules()
      foodPos = foodPos + ghostsPos if isScaredTimer else foodPos

      # Calcula distâncias
      pacman_distance = [manhattanDistance(f, actualPos) for f in foodPos]
      ghost_distance = [self.foodDistanceGhosts(f, ghostsPos) for f in foodPos] 
      
      # Obtém o objetivo da próxima ação
      if isScaredTimer:
            # Se existir algum fantasma assustado persegue-o
            closest = self.closestGhost(actualPos,  ghostsPos, newScaredTimes)
      else:
            # Se não, busca a comida mais próxima do pacman e distante do fantasma
            total = list(np.array(pacman_distance) - np.array(ghost_distance))
            closest = foodPos[total.index(min(total))]
      
      return closest

    def closestGhost(self, newPos, ghostsPos, ghostScaredTimer=None):
      distances = []
      for index in range(len(ghostsPos)):
        if not ghostScaredTimer or ghostScaredTimer[index] > 0:
          distances.append(manhattanDistance(newPos, ghostsPos[index]))
      return ghostsPos[distances.index(min(distances))]
    
    def ghostNorm(self, currentGameState, legalMoves):
      distant = 0
      for action in legalMoves:
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        ghostsPos = successorGameState.getGhostPositions()
        for index in range(len(ghostsPos)):
          d = manhattanDistance(newPos, ghostsPos[index])
          if d > distant:
            distant = d
      
      return distant


    def anyScaredTimer(self, newScaredTimes):
      return sum(newScaredTimes) > 0

    def foodDistanceGhosts(self, foodPos, ghostsPos):
      dist = [manhattanDistance(foodPos, ghostPos) for ghostPos in ghostsPos]
      return sum(dist)/len(dist)

    def foodDistanceClosestGhosts(self, foodPos, ghostsPos):
      return min([manhattanDistance(foodPos, ghostPos) for ghostPos in ghostsPos])

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

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        alpha = -float("inf")
        beta = float("inf")
        depth = 0
        score, action = self.minMax(gameState, depth, alpha, beta)
        
        return action

    def minMax(self, gameState, depth, alpha, beta, agent=0):
        agent, depth = self.getAgent(gameState, agent, depth)
        if self.isTerminal(gameState) or depth == self.depth:
            return (self.evaluationFunction(gameState), "Stop")

        bestScore = -float("inf") if agent == 0 else float("inf")
        bestAction = "Stop"

        legalMoves = gameState.getLegalActions(agent)
        for action in legalMoves:
          successorGameState = gameState.generateSuccessor(agentIndex=agent, action=action)
          newState =  self.minMax(successorGameState, depth, alpha, beta, agent+1)

          if agent == 0: #MAX
            if newState[0] > bestScore:
              bestScore = newState[0]
              bestAction = action
            if bestScore > beta:
              return (bestScore, action)
            alpha = max(alpha, newState[0])

          else: #MIN
            if newState[0] < bestScore:
                bestScore = newState[0]
                bestAction = action
            if bestScore < alpha:
              return (bestScore, action)
            beta = min(beta, newState[0])

        return (bestScore, bestAction)

    def isTerminal(self, gameState):
      return gameState.isWin() or gameState.isLose()

    def getAgent(self, gameState, agent,depth):
      if agent >= gameState.getNumAgents():
        return 0, depth+1
      return agent, depth

  
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        depth = 0
        score, action = self.minMax(gameState, depth)

        return action

    def minMax(self, gameState, depth, agent=0):
        agent, depth = self.getAgent(gameState, agent, depth)
        if self.isTerminal(gameState) or depth == self.depth:
            return (self.evaluationFunction(gameState), "Stop")

        bestScore = -float("inf") if agent == 0 else 0
        bestAction = "Stop"

        legalMoves = gameState.getLegalActions(agent)
        prob = 1.0/len(legalMoves)   
        for action in legalMoves:
          successorGameState = gameState.generateSuccessor(agentIndex=agent, action=action)
          newState =  self.minMax(successorGameState, depth, agent+1)

          if agent == 0: #MAX
            if newState[0] > bestScore:
              bestScore = newState[0]
              bestAction = action

          else: #Expect
            bestScore += newState[0]*prob #UTILIDADE ESPERADA
            bestAction = action

        return (bestScore, bestAction)

    def isTerminal(self, gameState):
      return gameState.isWin() or gameState.isLose()

    def getAgent(self, gameState, agent,depth):
      if agent >= gameState.getNumAgents():
        return 0, depth+1
      return agent, depth


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

