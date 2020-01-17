## The search algorithm itself -- it takes a problem, which will give it an initial state and the goal test,
##   the world state itself which gives it the successor states, and an evaluator that evaluates the quality
##   of a node on the search frontier

#  Priority queue code taken from Pacman project -- PriorityQueue supports
#      pop, isEmpty, and push/update
#
#  Client supplies
#    -- a WorldState; a WorldState implements the method successors()
#    -- a Problem which supplies the initial state and goal state checker
#    -- an Evaluator which supplies a method that evaluates a WorldState
#
#    Optional parameters
#       -- limit (integer or None) -- search will terminate after this many iterations
#           (i.e. after visiting this many nodes) whether or not a solution was
#             found).  If None, the search will only terminate if a solution is found or
#           the fringe has been exhausted.
#       -- verbose (integer or None) -- if not None, search will print diagnostic information
#            at the specified number of iterations
#
#   Search returns a 2-tuple -- 
#       -- a sequence of actions
#       -- performance information tuple  
#              number of nodes visited, 
#              process time used
#              number of nodes skipped (because they were previously expanded
#              the largest size of the fringe
#
#      The sequence of actions is None if and only if the search terminated without finding a solution,
#        either due to exhausting the fringe or due to reaching the iteration limit.

from priorityQueue import PriorityQueue
import searchClientInterface
import time

def aStarSearch(problem, evaluator, verbose=None, limit=None):
    startTime = time.process_time()
    fringe = PriorityQueue()
    max_fringe_size = 0
    visited = {}
    initialWorldState = problem.initial()
    initialValue = evaluator.value(initialWorldState, [])
    initialSearchState = SearchState(initialWorldState, [])
    fringe.update(initialSearchState, initialValue)
    numVisited = numSkipped = 0
    while (True):
        if len(fringe.heap) > max_fringe_size:
            max_fringe_size = len(fringe.heap)
        if fringe.isEmpty():
            return (None, (time.process_time() - startTime, numVisited, numSkipped, max_fringe_size))
        nextNode = fringe.pop()   # A search state (state, actions)
        numVisited += 1
        if (limit and numVisited > limit):
            return(None, (time.process_time() - startTime, numVisited, numSkipped, max_fringe_size))
        if (verbose and numVisited % verbose == 0):
            print("Visited " + str(numVisited) + " world is " + str(nextNode._worldState))
            print("Skipped " + str(numSkipped) + " Fringe is size " + str(len(fringe.heap)))
            print("Evaluation is " + str(evaluator.value(nextNode._worldState, nextNode._actions)) + " with actions " + str(len(nextNode._actions)))
        if (problem.isGoal(nextNode.worldState())):
            return (nextNode._actions, (time.process_time() - startTime, numVisited, numSkipped, max_fringe_size))
        if (nextNode._worldState in visited):
            numSkipped += 1
        else:
            visited[nextNode.worldState()] = True
            successors = nextNode.worldState().successors()
            for successor in successors:
                state, action = successor
                actions = list(nextNode.actions())
                actions.append(action)
                newSS = SearchState(state, actions)
                newValue = evaluator.value(state, actions)
                fringe.update(newSS, newValue)
    raise "Impossible search execution path."

##############################################
### SearchState -- this class is used only by the search framework
# Instances of SearchState go on the search fringe -- contains both a WorldState and 
# list of actions so far.  

class SearchState:
    def __str__(self):
        return "{S " + str(self._worldState) + "/" + str(self._actions) + "}"
    
    def __init__(self, worldState, actions):
        self._worldState = worldState
        self._actions = actions
    
    def worldState(self):
        return self._worldState
    
    def actions(self):
        return self._actions

