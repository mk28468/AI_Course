# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.oldValues=util.Counter()
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        """""
        for each iteration:
            for each state:
                if state is terminal: v(state)=0
                else:
                    max qvalue = -9999
                    for action in possible actions
                        qvalue = compute Q value
                        **get max q value
                        bestaction =
                    v(state) = max qvalue
            self.oldvalue = self.value
        """

        for i in range(0, iterations):
            for state in mdp.getStates():
                if not mdp.isTerminal(state):
                    bestQValue = float('-inf')
                    bestAction = None
                    actions = self.mdp.getPossibleActions(state)
                    for action in actions:
                        qValue = self.computeQValueFromValues(state, action)
                        if bestQValue < qValue:
                            bestQValue = qValue
                            bestAction = action
                    self.values[state] = bestQValue
                else:
                    self.values[state] = 0
            self.oldValues = self.values.copy()

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        """""
        if action = none:   return 0
        else
            for each t-state and p
                qvalue = qvalue + p(Reward of action + discount* oldValue of T-state )

            """
        qValue = 0
        if not action:
            qValue = 0
        else:
            tStateAndProbs = self.mdp.getTransitionStatesAndProbs(state, action)
            for(t,p) in tStateAndProbs:
                reward = self.mdp.getReward(state, action, t)
                qValue = qValue + p * (reward + self.discount * self.oldValues[t])
        return qValue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        """""
        getting the best action from a state:
        if no legal action(terminal state): return None
        else get actions
        maxreward = -9999
        bestaction = none
        for action in actions:
            reward = 0
            get tstate and p for state
            for each tstate and prob:
                reward = reward + oldvalue of t-state* p
                if reward >= maxReward
                    maxReward = reward
                    bestAction = action
            return bestaction
        """
        #getting the best action from a state

        actions = actions=self.mdp.getPossibleActions(state)
        if not actions:
            return None
        bestReward = float('-inf')
        bestAction = None
        for action in actions:
            reward = 0
            tStateAndProbs = self.mdp.getTransitionStatesAndProbs(state, action)
            for (t, p) in tStateAndProbs:
                reward = reward + p * self.oldValues[t]
            if bestReward < reward:
                bestAction = action
                bestReward = reward

        return bestAction

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
