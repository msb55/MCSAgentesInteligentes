# ghostAgents.py
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


from game import Agent
from game import Actions
from game import Directions
import random
from util import manhattanDistance
import util

class GhostAgent( Agent ):
    def __init__( self, index ):
        self.index = index

    def getAction( self, state ):
        dist = self.getDistribution(state)
        if len(dist) == 0:
            return Directions.STOP
        else:
            return util.chooseFromDistribution( dist )

    def getDistribution(self, state):
        "Returns a Counter encoding a distribution over actions from the provided state."
        util.raiseNotDefined()

class RandomGhost( GhostAgent ):
    "A ghost that chooses a legal action uniformly at random."
    def getDistribution( self, state ):
        dist = util.Counter()
        for a in state.getLegalActions( self.index ): dist[a] = 1.0
        dist.normalize()
        return dist

class DirectionalGhost( GhostAgent ):
    "A ghost that prefers to rush Pacman, or flee when scared."
    def __init__( self, index, prob_attack=0.8, prob_scaredFlee=0.8 ):
        self.index = index
        self.prob_attack = prob_attack
        self.prob_scaredFlee = prob_scaredFlee

    def getDistribution( self, state ):
        # Read variables from state
        ghostState = state.getGhostState( self.index )
        legalActions = state.getLegalActions( self.index )
        pos = state.getGhostPosition( self.index )
        isScared = ghostState.scaredTimer > 0

        speed = 1
        if isScared: speed = 0.5

        actionVectors = [Actions.directionToVector( a, speed ) for a in legalActions]
        newPositions = [( pos[0]+a[0], pos[1]+a[1] ) for a in actionVectors]
        pacmanPosition = state.getPacmanPosition()

        # Select best actions given the state
        distancesToPacman = [manhattanDistance( pos, pacmanPosition ) for pos in newPositions]
        if isScared:
            bestScore = max( distancesToPacman )
            bestProb = self.prob_scaredFlee
        else:
            bestScore = min( distancesToPacman )
            bestProb = self.prob_attack
        bestActions = [action for action, distance in zip( legalActions, distancesToPacman ) if distance == bestScore]

        # Construct distribution
        dist = util.Counter()
        for a in bestActions: dist[a] = bestProb / len(bestActions)
        for a in legalActions: dist[a] += ( 1-bestProb ) / len(legalActions)
        dist.normalize()
        return dist

class ExpectimaxGhost( GhostAgent ):
    "A ghost that prefers to rush Pacman, or flee when scared."
    def __init__( self, index):
        self.index = index

    def getDistribution( self, state ):

        # Read variables from state
        legalActions = state.getLegalActions( self.index )
        ghostState = state.getGhostState(self.index)
        isScared = ghostState.scaredTimer > 0

        # Select best actions given the state
        _, bestActions = self.getActionExpectimax(state, self.index, isScared)
        bestProb = 1

        # Construct distribution
        dist = util.Counter()
        for a in bestActions: dist[a] = bestProb / len(bestActions)
        for a in legalActions: dist[a] += ( 1-bestProb ) / len(legalActions)
        dist.normalize()
        return dist

    def getActionExpectimax(self, State, agent, isScared):
        self.agent = agent
        self.max_depth = 3
        depth = 0
        score, action = self.minMax(State, depth, agent, isScared)
        return score, [action]

    def minMax(self, gameState, depth,  agent, isScared):
       # agent, depth = getAgent(gameState, agent, depth)
        depth += 1
        if  isTerminal(gameState):
            return (float("inf") if gameState.isWin() else -float("inf"), "Stop")
        if depth == self.max_depth:
            return (eval(gameState, agent, isScared), "Stop")

        bestScore = -float("inf") if agent == 0 else 0
        legalMoves = gameState.getLegalActions(agent)
        bestAction = legalMoves[0]

        prob = 1.0/len(legalMoves)   
        for action in legalMoves:
          successorGameState = gameState.generateSuccessor(agentIndex=agent, action=action)
          new_agent = 0 if agent!= 0 else self.agent
          newState =  self.minMax(successorGameState, depth, new_agent, isScared)

          if agent == 0: #MAX
            if newState[0] > bestScore:
              bestScore = newState[0]
              bestAction = action

          else: #Expect
            bestScore += newState[0]*prob #UTILIDADE ESPERADA
            bestAction = action

        return (bestScore, bestAction)


class AlphaBetaGhost( GhostAgent ):
    "A ghost that prefers to rush Pacman, or flee when scared."
    def __init__( self, index):
        self.index = index

    def getDistribution( self, state ):

        # Read variables from state
        legalActions = state.getLegalActions( self.index )
        ghostState = state.getGhostState(self.index)
        isScared = ghostState.scaredTimer > 0

        # Select best actions given the state
        bestScore, bestActions = self.getActionAlphaBeta(state, self.index, isScared)
        bestProb = 1

        # Construct distribution
        dist = util.Counter()
        for a in bestActions: dist[a] = bestProb / len(bestActions)
        for a in legalActions: dist[a] += ( 1-bestProb ) / len(legalActions)
        dist.normalize()
        return dist


    def getActionAlphaBeta(self, State, agent, isScared):
        alpha = -float("inf")
        beta = float("inf")
        max_depth = 3
        depth = 0
        self.agent = agent
        score, action = self.minMax(State, depth, max_depth, alpha, beta, agent, isScared)
        return score, [action]

    def minMax(self, gameState, depth, max_depth, alpha, beta, agent, isScared):
        depth += 1
        if isTerminal(gameState):
            return (float("inf") if gameState.isWin() else -float("inf"), "Stop")
        if depth == max_depth:
            return (eval(gameState, agent, isScared), "Stop")
       
        bestScore = -float("inf") if agent == 0 else float("inf")
        legalMoves = gameState.getLegalActions(agent)
        bestAction = legalMoves[0]

        for action in legalMoves:
          successorGameState = gameState.generateSuccessor(agentIndex=agent, action=action)
          new_agent = 0 if agent!= 0 else self.agent
          newState =  self.minMax(successorGameState, depth, max_depth, alpha, beta, new_agent, isScared)

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
   
def eval(gameState, agent, isScared):
    pac = gameState.getPacmanPosition()
    if agent != 0:
        return manhattanDistance(gameState.getGhostPosition(agent), pac)
    else:
        closest = closestGhost(pac, gameState.getGhostPositions())
        dist = manhattanDistance(closest, pac)
        return dist * -1 if isScared else dist

def closestGhost(newPos, ghostsPos, ghostScaredTimer=None):
    distances = []
    for index in range(len(ghostsPos)):
        if not ghostScaredTimer or ghostScaredTimer[index] > 0:
            distances.append(manhattanDistance(newPos, ghostsPos[index]))
    return ghostsPos[distances.index(min(distances))]

def getAgent(gameState, agent,depth):
    if agent >= gameState.getNumAgents():
        return 0, depth+1
    return agent, depth

def isTerminal(gameState):
      return gameState.isWin() or gameState.isLose()