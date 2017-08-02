# qlearningAgents.py
# ------------------
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
#this is my own work, it was written without consulting other students -Junyuan Ke 2148073


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        #intialize Q-values
        self.Qstate = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        #using util.counter
        #util.Counter(state,action)
        return self.Qstate[(state,action)]

    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        """"" returns the max value from all actions
        for each action:
            if Qvalue>maxvalue : maxvalue = qvalue
        return maxvalue
        """
        bestQValue = 0
        actions = self.getLegalActions(state)
        if actions:
            bestQValue = float('-inf')
            for action in actions:
                qValue = self.getQValue(state, action)
                if bestQValue <= qValue:
                    bestQValue = qValue
        return bestQValue

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        """"" returns the max value from all actions
        for each action:
            if Qvalue>maxvalue : maxvalue = qvalue
                bestaction = action
        return bestaction
                """
        bestQValue = 0
        actions = self.getLegalActions(state)
        if actions:
            bestAction = None
            bestQValue = float('-inf')
            for action in actions:
                qValue = self.getQValue(state, action)
                if bestQValue <= qValue:
                    bestQValue = qValue
                    bestAction = action
        return bestAction

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"

        """""
        if no legal action(terminal state): action = None
        else:
            if coinfilp epsilon
                take a random action from all legal actions
            else
                compute the action to take in current state
                take the best policy action

        """
        action = None
        if not legalActions:
            return action
        else:
            prob = self.epsilon
            if util.flipCoin(prob):
                action = random.choice(legalActions)
            else:
                action = self.computeActionFromQValues(state)
        return action


    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        """""
        for each action:
            nextQvalue = get Qvalue
            if nextQvalue > maxQ value: max = next
        sample = R + discount*maxNextQ
        (using counter:)
        self.Q(state,action) = (1-alpha)*thisQvalue + alpha*sample
        """
        "*** YOUR CODE HERE ***"
        #update the Q values in self.Qstate

        bestQvalue = float('-inf')
        Actions = self.getLegalActions(nextState)
        if Actions:
            for nextAction in Actions:
                nextQValue = self.getQValue(nextState, nextAction)
                if bestQvalue < nextQValue:
                    bestQvalue = nextQValue
        else:
            bestQvalue = 0
        sample = reward + self.discount * bestQvalue
        thisQvalue = self.getQValue(state, action)
        a = self.alpha
        self.Qstate[(state, action)] = (1-a) * thisQvalue + a * sample
        return

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        """""
        features = get features
        for each feature:
            Approximate Q function: Qvalue = Qvalue + features(feature)*self.weights[feat]
        """

        sum = 0
        features = self.featExtractor.getFeatures(state,action)
        for feature in features:
            f = features[feature]
            w = self.weights[feature]
            sum = sum + f * w
        return sum

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        """""
        features = get feature
        difference = reward + gamma * bestQvalue - currentQvalue
        update weights...
        for each weight:
                wight += alpha * difference * feature(s,a)
        """
        features = self.featExtractor.getFeatures(state, action)
        difference = reward + self.discount * self.getValue(nextState) - self.getQValue(state, action)
        for feature in features:
            #w =
            #print w
            self.weights[feature] += self.alpha * difference * features[feature]

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            #for weight in self.weights:
            #print weight
            pass