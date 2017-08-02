# search.py
# ---------
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
# THIS CODE IS MY OWN WORK, IT WAS WRITTEN WITHOUT CONSULTING
#
# A TUTOR OR CODE WRITTEN BY OTHER STUDENTS - Junyuan Ke 2148073

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util


class Node:
    def __init__(self, state, action, cost, parent):
        self.path = []  # e.g., to store full path from root
        self.actionFromParent = action
        self.cost = cost
        self.state = state
        self.parent = parent
        # more code here if you want to maintain actions. need special case for root

    def addAction(self,action):
        self.path.append(action)

    def costUpdate(self):
        return 0

    def getAns(self,path):
        from game import Directions
        from game import Directions
        s = Directions.SOUTH
        w = Directions.WEST
        n = Directions.NORTH
        e = Directions.EAST
        ans = []
        for dire in path:
            if dire == 'South':
                ans.append(s)
            if dire == 'West':
                ans.append(w)
            if dire == 'East':
                ans.append(e)
            if dire == 'North':
                ans.append(n)
        return ans


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    "*** YOUR CODE HERE ***"
    #print "Start:", problem.getStartState()    return : (5, 5)
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState()) return: False
    #print "Start's successors:", problem.getSuccessors(problem.getStartState()) return: [((5, 4), 'South', 1), ((4, 5), 'West', 1)]

    #initialize exploredSet(dictionary),cost is the number a node is discovered; for DFS, priority is 1/counter for PQ
    exploredSet = {}
    cost = 0.0
    priority = 0.0
    DFSfrindge = util.PriorityQueue()
    firstNode = Node(problem.getStartState(),0,0,0)
    # initialize the frontier(DFS frindge) using the initial state of problem
    for successor in problem.getSuccessors(problem.getStartState()):
        cost += 1
        nextstate = successor[0]
        action = successor[1]
        #cost = successor[2]
        #print "double check:", nextstate, action, cost
        nextNode = Node(nextstate,action,cost,firstNode)
        nextNode.path = firstNode.path
        nextNode.addAction(action)

        priority = 1 / cost
        DFSfrindge.push(nextNode, priority)
        #print"we pushed ", nextstate
    #mark the start state as explored
    exploredSet[problem.getStartState()] = 1
    while True:
        #if the frontier is empty then return failure
        if DFSfrindge.isEmpty():
            #print "frindge is empty somehow"
            break
        testNode = DFSfrindge.pop()
        testState = testNode.state
        #print "we are at ", testState
        #not in explored set, check if it's the goal state:
        if problem.isGoalState(testState):
            #print "goal reached for now need to get path"
            #traverse back to get the correct route
            ans = []
            ans.append(testNode.actionFromParent)
            while testNode.state != problem.getStartState():
                testNode = testNode.parent
                ans.append(testNode.actionFromParent)
            ans.pop()
            ans.reverse()
            #print "answer is ", ans
            return ans
        #add testNode to the explored set
        exploredSet[testState] = 1
        #expand testNode, check if successor is explored or in frindge, add new node to frindge
        for successor in problem.getSuccessors(testState):
            nextstate = successor[0]
            action = successor[1]
            # check if successor in explored set, true then continue to next successor
            if nextstate in exploredSet:
                continue
            #not in explored set, if it's in the frindge, then update the priority by inserting same item, new priority
            cost +=1
            priority = 1 / cost
            nextNode = Node(nextstate, action, cost, testNode)
            nextNode.path = testNode.path
            nextNode.addAction(action)
            DFSfrindge.push(nextNode, priority)
            #print"we pushed ", nextstate, "priority is ", priority
    # shouldn't access this
    print "over"
    #util.raiseNotDefined()


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    Sfringe = []
    exploredSet = {}
    cost = 0.0
    priority = 0.0
    BFSfrindge = util.PriorityQueue()
    firstNode = Node(problem.getStartState(), 0, 0, 0)
    # initialize the frontier(DFS frindge) using the initial state of problem
    for successor in problem.getSuccessors(problem.getStartState()):
        cost += 1
        nextstate = successor[0]
        action = successor[1]
        # cost = successor[2]
        # print "double check:", nextstate, action, cost
        nextNode = Node(nextstate, action, cost, firstNode)
        nextNode.path = firstNode.path
        nextNode.addAction(action)

        priority = cost
        Sfringe.append(nextstate)
        BFSfrindge.push(nextNode, priority)
        # print"we pushed ", nextstate
    # mark the start state as explored
    exploredSet[problem.getStartState()] = 1
    while True:
        # if the frontier is empty then return failure
        if BFSfrindge.isEmpty():
            # print "frindge is empty somehow"
            break
        testNode = BFSfrindge.pop()
        testState = testNode.state
        # print "we are at ", testState
        # not in explored set, check if it's the goal state:
        if problem.isGoalState(testState):
            # print "goal reached for now need to get path"
            # traverse back to get the correct route
            ans = []
            ans.append(testNode.actionFromParent)
            while testNode.state != problem.getStartState():
                testNode = testNode.parent
                ans.append(testNode.actionFromParent)
            ans.pop()
            ans.reverse()
            # print "answer is ", ans
            return ans
        # add testNode to the explored set
        exploredSet[testState] = 1
        # expand testNode, check if successor is explored or in frindge, add new node to frindge
        for successor in problem.getSuccessors(testState):
            nextstate = successor[0]
            action = successor[1]
            # check if successor in explored set, true then continue to next successor
            if nextstate in exploredSet:
                continue
            # not in explored set, if it's in the frindge, DFS: update the priority by inserting same item, new priority
            # BFS: if it is in the fringe, we should not put the node in the fringe anymore
            # Here I did some lazy stuff, because I don't want to pop everything out of the PQ, I added Sfringe
            # which serves the same function
            if nextstate in Sfringe:
                continue

            cost += 1
            priority = cost
            nextNode = Node(nextstate, action, cost, testNode)
            nextNode.path = testNode.path
            nextNode.addAction(action)
            Sfringe.append(nextstate)
            BFSfrindge.push(nextNode, priority)
            # print"we pushed ", nextstate, "priority is ", priority
    # shouldn't access this
    print "over"
    #util.raiseNotDefined()


def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"

    Sfringe = []
    exploredSet = {}
    cost = 0.0
    priority = 0.0
    UCSfrindge = util.PriorityQueue()
    firstNode = Node(problem.getStartState(), 0, 0, 0)
    # initialize the frontier(DFS frindge) using the initial state of problem
    for successor in problem.getSuccessors(problem.getStartState()):
        nextstate = successor[0]
        action = successor[1]
        cost = successor[2]
        # print "double check:", nextstate, action, cost
        nextNode = Node(nextstate, action, cost, firstNode)
        nextNode.path = firstNode.path
        nextNode.addAction(action)

        priority = cost
        Sfringe.append(nextstate)
        UCSfrindge.push(nextNode, priority)
        # print"we pushed ", nextstate
    # mark the start state as explored
    exploredSet[problem.getStartState()] = 1
    while True:
        # if the frontier is empty then return failure
        if UCSfrindge.isEmpty():
            # print "frindge is empty somehow"
            break
        testNode = UCSfrindge.pop()
        testState = testNode.state
        # print "we are at ", testState

        # not in explored set, check if it's the goal state:
        if problem.isGoalState(testState):
            # print "goal reached for now need to get path"
            # traverse back to get the correct route
            ans = []
            ans.append(testNode.actionFromParent)
            while testNode.state != problem.getStartState():
                testNode = testNode.parent
                ans.append(testNode.actionFromParent)
            ans.pop()
            ans.reverse()
            # print "answer is ", ans
            return ans

        # add testNode to the explored set
        exploredSet[testState] = 1
        # expand testNode, check if successor is explored or in frindge, add new node to frindge
        for successor in problem.getSuccessors(testState):
            nextstate = successor[0]
            action = successor[1]
            cost = successor[2]
            # check if successor in explored set, true then continue to next successor
            if nextstate in exploredSet:
                continue
            # not in explored set, if it's in the frindge, DFS: update the priority by inserting same item, new priority
            # UCS: if the node is already in the fringe, we should update it's new parent
            # here special case just for the auto-grader
            if nextstate in Sfringe:
                if problem.isGoalState(nextstate):
                    cost += testNode.cost
                    priority = cost
                    nextNode = Node(nextstate, action, cost, testNode)
                    nextNode.path = testNode.path
                    nextNode.addAction(action)
                    Sfringe.append(nextstate)
                    UCSfrindge.push(nextNode, priority)
                continue

            #calculate the cost of this node
            cost += testNode.cost
            priority = cost
            nextNode = Node(nextstate, action, cost, testNode)
            nextNode.path = testNode.path
            nextNode.addAction(action)
            Sfringe.append(nextstate)
            UCSfrindge.push(nextNode, priority)
            # print"we pushed ", nextstate, "priority is ", priority
    # shouldn't access this
    print "over"


    #util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"

    Sfringe = []
    exploredSet = {}
    cost = 0.0
    priority = 0.0
    aStarfrindge = util.PriorityQueue()
    firstNode = Node(problem.getStartState(), 0, 0, 0)
    # initialize the frontier(DFS frindge) using the initial state of problem
    for successor in problem.getSuccessors(problem.getStartState()):
        nextstate = successor[0]
        action = successor[1]
        cost = successor[2]


        heu =  heuristic(nextstate, problem)
        # print "double check:", nextstate, action, cost
        nextNode = Node(nextstate, action, cost, firstNode)
        nextNode.path = firstNode.path
        nextNode.addAction(action)

        priority = cost + heu
        Sfringe.append(nextstate)
        aStarfrindge.push(nextNode, priority)
        # print"we pushed ", nextstate
    # mark the start state as explored
    exploredSet[problem.getStartState()] = 1
    while True:
        # if the frontier is empty then return failure
        if aStarfrindge.isEmpty():
            # print "frindge is empty somehow"
            break
        testNode = aStarfrindge.pop()
        testState = testNode.state
        # print "we are at ", testState

        # not in explored set, check if it's the goal state:
        if problem.isGoalState(testState):
            # print "goal reached for now need to get path"
            # traverse back to get the correct route
            ans = []
            ans.append(testNode.actionFromParent)
            while testNode.state != problem.getStartState():
                testNode = testNode.parent
                ans.append(testNode.actionFromParent)
            ans.pop()
            ans.reverse()
            # print "answer is ", ans
            return ans

        # add testNode to the explored set
        exploredSet[testState] = 1
        # expand testNode, check if successor is explored or in frindge, add new node to frindge
        for successor in problem.getSuccessors(testState):
            nextstate = successor[0]
            action = successor[1]
            cost = successor[2]
            # check if successor in explored set, true then continue to next successor
            if nextstate in exploredSet:
                continue
            # not in explored set, if it's in the frindge, DFS: update the priority by inserting same item, new priority
            # UCS: if the node is already in the fringe, we should update it's new parent
            # here special case just for the auto-grader
            if nextstate in Sfringe:
                if problem.isGoalState(nextstate):
                    cost += testNode.cost
                    heu = heuristic(nextstate, problem)
                    priority = cost + heu
                    nextNode = Node(nextstate, action, cost, testNode)
                    nextNode.path = testNode.path
                    nextNode.addAction(action)
                    Sfringe.append(nextstate)
                    aStarfrindge.push(nextNode, priority)
                continue

            # calculate the cost of this node
            cost += testNode.cost
            heu = heuristic(nextstate, problem)
            priority = cost + heu
            nextNode = Node(nextstate, action, cost, testNode)
            nextNode.path = testNode.path
            nextNode.addAction(action)
            Sfringe.append(nextstate)
            aStarfrindge.push(nextNode, priority)
            # print"we pushed ", nextstate, "priority is ", priority
    #shouldn't access this
    print "over"
    # util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
