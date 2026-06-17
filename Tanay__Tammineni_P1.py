#!/usr/bin/env python
# coding: utf-8

# #Team Members - AI NEXUS
# 
# 1. Tanay Tammineni, S02065959, graduate
# 
# 2. Vidya rani vallala, S02066899, graduate
# 
# 3. Supriya Bollareddy, S02050758, graduate
# 
# 4. Lahari Maddukuri, S02050755, graduate
# 
# 5. Narendra Dhulipalla, S02049657, graduate
# 
# 6. Gayatri Vattuluri, S02059506, graduate
# 
# 
# 

# # Maze Search
# 
# 
# 
# 
# 
# 
# 
# 

# Reference : Textbook online repository files (search4e.ipynb) in
# aima-python, or similar files in other folders, such as aima-java.

# #Problem:
# 
# In order to expedite the process of creating specialized problem domains, we begin by establishing an abstract class that serves as the foundation for specifying particular problems. This abstract class provides the foundation for creating several subclasses that are suited to different problem domains. When algorithms require heuristic evaluation functions, the problem class is assigned a default h function that is initially set to zero. The following subclasses are still free to define their own default h function, which takes into account the particularities of their domain. Furthermore, its architecture promotes flexibility and extensibility, allowing for the easy incorporation of innovative approaches to problem-solving and heuristic evaluation techniques. As a result, the abstract class acts as a versatile framework that encourages modular design and effective problem-solving techniques in a variety of contexts.
# 
# 
# The `Problem` class defines an abstract framework for formal problem representation, offering methods for actions, results, and heuristic evaluation. Subclasses must override these methods to define specific problem domains and associated problem-solving strategies.
# 

# In[34]:


import matplotlib.pyplot as plt
import random
import heapq
import math
import sys
from collections import defaultdict, deque, Counter
from itertools import combinations


class Problem(object):
    """The abstract class for a formal problem. A new domain subclasses this,
    overriding `actions` and `results`, and perhaps other methods.
    The default heuristic is 0 and the default action cost is 1 for all states.
    When yiou create an instance of a subclass, specify `initial`, and `goal` states
    (or give an `is_goal` method) and perhaps other keyword args for the subclass."""

    def __init__(self, initial=None, goal=None, **kwds):
        self.__dict__.update(initial=initial, goal=goal, **kwds)

    def actions(self, state):        raise NotImplementedError
    def result(self, state, action): raise NotImplementedError
    def is_goal(self, state):        return state == self.goal
    def action_cost(self, s, a, s1): return 1
    def h(self, node):               return 0

    def __str__(self):
        return '{}({!r}, {!r})'.format(
            type(self).__name__, self.initial, self.goal)


# #Node
# 
# A node in a search tree that is utilized by different search methods is represented by the `Node` class. It contains data like the node's depth in the search tree, the current state, the parent node, the action performed from the parent node to reach the current state, and the cumulative path cost.
# 
# - {state}: Describes the problem's existing situation.
# - {parent}: Indicates the parent node that is used to access the current node.
# - {action}: Indicates the step the parent node took to get to the current state.
# - {path_cost}: Indicates the total amount of money spent from the starting point to the present.
# - {depth}: Shows how far down the node is in the search tree, or how many steps were needed to get to the current state fromthe initial state.

# In[35]:


class Node:
    "A Node in a search tree."
    def __init__(self, state, parent=None, action=None, path_cost=0,depth=0):
        self.__dict__.update(state=state, parent=parent, action=action, path_cost=path_cost,depth=depth)

    def __repr__(self): return '<{}>'.format(self.state)
    def __len__(self): return 0 if self.parent is None else (1 + len(self.parent))
    def __lt__(self, other): return self.path_cost < other.path_cost


failure = Node('failure', path_cost=math.inf)
cutoff  = Node('cutoff',  path_cost=math.inf)


def expand(problem, node):
    "Expand a node, generating the children nodes."
    s = node.state
    for action in problem.actions(s):
        s1 = problem.result(s, action)
        cost = node.path_cost + problem.action_cost(s, action, s1)
        yield Node(s1, node, action, cost,node.depth + 1)


def path_actions(node):
    "The sequence of actions to get to this node."
    if node.parent is None:
        return []
    return path_actions(node.parent) + [node.action]


def path_states(node):
    "The sequence of states to get to this node."
    if node in (cutoff, failure, None):
        return []
    return path_states(node.parent) + [node.state]

# #QUEUES
# 
# 
# Search algorithms provide queues such as `PriorityQueue}, which retains things together while continuously eliminating the item with the lowest f(item) score, and `deque}, which follows a last-in-first-out (LIFO) order. These data structures control the sequence in which nodes are examined during the search process, enabling various search strategies like depth-first search, breadth-first search, and A* search. Furthermore, the search algorithm's efficacy and efficiency in locating the best solutions are influenced by the data structure selection.
# 

# In[36]:



LIFOQueue = list

# #PriorityQueue
# 
# By giving each of its constituents a distinct priority number, a priority queue essentially creates several queue types. It performs effective heap-related actions by using the `heapq` module, making sure that things with higher priority numbers are handled first. This makes it possible to quickly construct a variety of algorithms, where the exploration order of nodes is determined by their priority, such as Dijkstra's algorithm and A* search. Priority Queues are an essential part of many optimization and search methods because heap data structures allow for quick element insertion and retrieval.
# 

# In[37]:


import heapq

class PriorityQueue:
    """A queue in which the item with minimum f(item) is always popped first."""

    def __init__(self, items=(), key=lambda x: x):
        self.key = key
        self.items = []
        for item in items:
            self.add(item)

    def add(self, item):
        """Add item to the queuez."""
        pair = (self.key(item), item)
        heapq.heappush(self.items, pair)

    def pop(self):
        """Pop and return the item with min f(item) value."""
        return heapq.heappop(self.items)[1]

    def top(self): return self.items[0][1]

    def __len__(self): return len(self.items)


# #Plotting function
# 
# A maze expressed as a 2D array can be shown using the `maze_plot` function. Matplotlib is used to generate a graphical depiction of the maze. The program iterates through every maze cell, designating particular characters—for example, '%' for walls, 'P' for the player's position, and '.' for the objective. The plot is then expanded to include the corresponding shapes: green circles represent the player's position, blue rectangles represent the walls, and red dotted circles represent the objective. It also modifies the plot's boundaries to match the maze's dimensions and maintains an equal aspect ratio. Lastly, to indicate the borders of the maze, it paints a blue dotted line around the outside. The plot that results offers a graphic representation of the maze layout, helping users understand its structure and aiding in pathfinding or exploration algorithms.

# In[38]:


import matplotlib.pyplot as plt

def maze_plot(maze):
    fig, ax = plt.subplots()

    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == '%':
                ax.add_patch(plt.Rectangle((j, i), 1, 1, facecolor='blue'))
            elif maze[i][j] == 'P':
                ax.add_patch(plt.Circle((j + 0.5, i + 0.5), 0.25, facecolor='green'))
            elif maze[i][j] == '.':
                ax.add_patch(plt.Circle((j + 0.5, i + 0.5), 0.25, facecolor='red', linestyle='dotted'))

    ax.set_xlim(0, len(maze[0]))
    ax.set_ylim(len(maze), 0)
    ax.set_aspect('equal')

    ax.plot([0, 0, len(maze[0]), len(maze[0]), 0],
            [0, len(maze), len(maze), 0, 0],
            color='blue', linestyle='dotted')

    plt.show()


# In[39]:


class SearchResult:
    def __init__(self, node, max_fringe_size):
        self.node = node
        self.max_fringe_size = max_fringe_size

# #DFS algorithm
# 
# One popular method for navigating and exploring labyrinth data structures is depth-first search (DFS). It works by following a path as far down as it can go before turning around. In other words, it follows one path until it comes to a stop, at which point it goes back to the most recent intersection to investigate possibilities that haven't yet been considered. Until the target is located or the entire maze has been thoroughly investigated, this iterative procedure is carried out. DFS is an essential tool for pathfinding and problem-solving in a variety of disciplines and is crucial to both computer science and graph theory.
# 

# In[40]:


def dfs(problem):
    node = Node(problem.initial)
    if problem.is_goal(problem.initial):
        return SearchResult(node, 0)
    frontier = LIFOQueue([node])
    reached = {problem.initial}
    max_fringe_size = 0
    while frontier:
        node = frontier.pop()
        max_fringe_size = max(max_fringe_size, len(frontier))
        for child in expand(problem, node):
            s = child.state
            if problem.is_goal(s):
                return SearchResult(child, max_fringe_size)
            if s not in reached:
                reached.add(s)
                frontier.append(child)

    return SearchResult(failure, max_fringe_size)



# #A* algorithm
# 
# The A* algorithm, also called "A-star," is a sophisticated method for pathfinding and graph traversal that works especially well for figuring out the shortest route between two nodes in a weighted graph. This algorithm combines the ideas of Dijkstra's algorithm—which finds the shortest path without using any specific heuristics—with the concepts of heuristic search, which uses well-informed estimations or heuristics to direct the exploration. By combining these components, A* quickly finds the best path while taking into account the estimated distance to the objective node as well as the cost spent. It does this by striking a balance between exploration and exploitation. Because of its hybrid character, A* is an algorithm that is widely used in a variety of industries and makes pathfinding and optimization tasks in a wide range of applications efficient.
# 

# In[41]:


def best_first_search(problem, f):
    "Search nodes with minimum f(node) value first."
    node = Node(problem.initial)
    if problem.is_goal(problem.initial):
        return SearchResult(node, 0)
    frontier = PriorityQueue([node], key=f)
    reached = {problem.initial: node}
    max_fringe_size = 0
    while frontier:
        max_fringe_size = max(max_fringe_size, len(frontier))
        node = frontier.pop()
        if problem.is_goal(node.state):
            return SearchResult(node, max_fringe_size)
        for child in expand(problem, node):
            s = child.state
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child
                frontier.add(child)
    return SearchResult(failure, max_fringe_size)


# In[42]:



import math


def g(n): return n.path_cost

def astar_search(problem):
    """Search nodes with minimum f(n) = g(n) + h(n), using Manhattan distance as the heuristic."""
    def h(node):
        """Manhattan distance from the current position to the goal as the heuristic function."""
        current_state = node.state
        goal_state = problem.goal
        distance = abs(current_state[0] - goal_state[0]) + abs(current_state[1] - goal_state[1])
        return distance

    return best_first_search(problem, f=lambda n: g(n) + h(n))



# #Maze Problem
# 
# Finding a way from a starting point to a predetermined destination through a labyrinth is a challenge that is captured by the `Maze_Problem class. Its methods are overridden, expressly to make them suitable for maze navigation, and it derives from the {Problem} class. The beginning point, the objective position, and the maze itself are the three parameters passed to the class constructor. Using the cardinal directions (north, south, east, and west) as a guide, the `actions` method finds all possible paths from a given state inside the maze, avoiding the walls indicated by '%'. To make it easier to navigate the maze, the `result` method calculates the state that is reached after doing a specific action from a specific state. Further, a textual representation of the maze is made possible using the `__str__ method. In general, the class `Maze_Problem` provides a framework for solving maze navigation problems, enabling the exploration and navigation of complex maze structures in a systematic manner using various search algorithms.

# In[43]:


class Maze_Problem(Problem):
    """The problem of searching a path through a maze from start to goal."""

    def __init__(self, maze, start, goal):
        self.maze = maze
        Problem.__init__(self, initial=start, goal=goal)

    def actions(self, state):
        "Return the actions that can be executed in the given state."
        row, col = state
        actions = []
        if row > 0 and self.maze[row-1][col] != '%': actions.append('N')
        if row < len(self.maze)-1 and self.maze[row+1][col] != '%': actions.append('S')
        if col > 0 and self.maze[row][col-1] != '%': actions.append('W')
        if col < len(self.maze[row])-1 and self.maze[row][col+1] != '%': actions.append('E')
        return actions

    def result(self, state, action):
        "Return the state that results from executing the given action in the given state."
        row, col = state
        if action == 'N': return (row-1, col)
        if action == 'S': return (row+1, col)
        if action == 'W': return (row, col-1)
        if action == 'E': return (row, col+1)
        assert False, 'Not a valid action: {}'.format(action)

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.maze])





# #Report
# 
# 
# A summary of statistics for every searcher method used to solve a given set of issues is what the `report` function is intended to offer. It writes out the name of each searcher after iterating over all of the ones in the `searchers` list. It generates a `CountCalls` object for each problem in the `problems` list to monitor attribute access counts, and it assigns the problem solving task to the corresponding searcher algorithm. During the search process, it updates counters with pertinent data like the quantity of actions executed, the cost of the path, and the size of the fringe. It publishes out specific counts for each problem along with the path to solution if the {verbose` argument is set to `True}. It reports the highest tree depth searched across all problems after processing them all problems for each searcher algorithm. A helper function called `report_counts` is used within `report` to produce one line of the counts report, which includes information about the solution path, number of expanding nodes, and maximum size of the fringe during the search. The efficiency of various search algorithms may be thoroughly analyzed and compared across numerous problem instances thanks to this modular design.
# 
# 
# 

# In[44]:



class CountCalls:
    """Delegate all attribute gets to the object, and count them in ._counts"""
    def __init__(self, obj):
        self._object = obj
        self._counts = Counter()

    def __getattr__(self, attr):
        "Delegate to the original object, after incrementing a counter."
        self._counts[attr] += 1
        return getattr(self._object, attr)

def report(searchers, problems,solution_path, verbose=True):
    """Show summary statistics for each searcher (and on each problem unless verbose is false)."""
    for searcher in searchers:
        print(searcher.__name__ + ':')
        total_counts = Counter()
        max_depth = 0
        for p in problems:
            prob   = CountCalls(p)
            soln   = searcher(prob)
            counts = prob._counts;
            max_depth = max(max_depth, soln.node.depth)
            if soln.node == failure:
                counts.update(actions=0, cost=0, fringe_size=soln.max_fringe_size)
            else:
                counts.update(actions=len(path_states(soln.node)), cost=soln.node.path_cost, fringe_size=soln.max_fringe_size)
            total_counts += counts
            if verbose: report_counts(counts, solution_path )
        #report_counts(total_counts, solution_path)
        print(f"Maximum tree depth searched: {max_depth}")


def report_counts(counts, name):
    """Print one line of the counts report."""
    #print("Path cost is",counts['cost'],"\n")
    print("Solution path is ",name,"\n")
    print("Number of nodes expanded",counts['result'],"\n")
    print("Maximum size of finge",counts['fringe_size'],"\n")




# #sample maze file.lay
# 
# **Depth-First-Search for small maze**

# In[69]:



with open("/content/sample maze file.lay", "r") as sampleMazefile:
    maze=list(sampleMazefile)


start = None
goal = None
mutiple_goals={}
k=0
for i in range(len(maze)):
    maze[i] = maze[i].replace("\n", "")
    for j in range(len(maze[i])):
        if maze[i][j] == 'P':
            start = (i, j)
        elif maze[i][j] == '.':
            goal= (i, j)
            mutiple_goals[k]=goal
            k=k+1
print("Start","Goal")
print(start,goal)
maze_plot(maze)
for a in range(k):
  problem = Maze_Problem(maze, start, mutiple_goals[a])
  solution_node = dfs(problem)

  if solution_node.node == failure:
    print("No solution")
  else:
    dfs_solution_path = path_states(solution_node.node)
    li=[]
    print(' ')
    print(" path to reach from ",start,"to ",mutiple_goals[a]," is")
    print(' ')
    print(dfs_solution_path )
    print(' ')
    for i in range(len(maze)):
        maze_store = ''
        for j in range(len(maze[i])):
            if (i, j) in dfs_solution_path :
                maze_store += '.'
            else:
                maze_store += maze[i][j]
        print(maze_store)
        li.append(maze_store)
  print(' ')
  print(' ')
  maze_plot(li)

# #smallMaze.lay

# **Depth-First-Search for small maze**

# In[45]:



with open("/content/smallMaze.lay", "r") as smallMazefile:
    maze=list(smallMazefile)


start = None
goal = None
mutiple_goals={}
k=0
for i in range(len(maze)):
    maze[i] = maze[i].replace("\n", "")
    for j in range(len(maze[i])):
        if maze[i][j] == 'P':
            start = (i, j)
        elif maze[i][j] == '.':
            goal= (i, j)
            mutiple_goals[k]=goal
            k=k+1
print("Start","Goal")
print(start,goal)
maze_plot(maze)
for a in range(k):
  problem = Maze_Problem(maze, start, mutiple_goals[a])
  solution_node = dfs(problem)

  if solution_node.node == failure:
    print("No solution")
  else:
    dfs_solution_path = path_states(solution_node.node)
    li=[]
    print(' ')
    print(" path to reach from ",start,"to ",mutiple_goals[a]," is")
    print(' ')
    print(dfs_solution_path )
    print(' ')
    for i in range(len(maze)):
        maze_store = ''
        for j in range(len(maze[i])):
            if (i, j) in dfs_solution_path :
                maze_store += '.'
            else:
                maze_store += maze[i][j]
        print(maze_store)
        li.append(maze_store)
  print(' ')
  print(' ')
  maze_plot(li)

# #Report for Depth-First-Search for small Maze

# In[46]:


print("Report for Depth-First-Search for small Maze")
print(' ')

report([dfs], [problem],dfs_solution_path)

# #A* search for small Maze

# In[48]:



with open("/content/smallMaze.lay", "r") as smallMazefile:
    maze=list(smallMazefile)



start = None
goal = None
mutiple_goals={}
k=0
for i in range(len(maze)):
    maze[i] = maze[i].replace("\n", "")
    for j in range(len(maze[i])):
        if maze[i][j] == 'P':
            start = (i, j)
        elif maze[i][j] == '.':
            goal= (i, j)
            mutiple_goals[k]=goal
            k=k+1
print(start,goal)
maze_plot(maze)
for a in range(k):
  problem = Maze_Problem(maze, start, mutiple_goals[a])
  solution_node = astar_search(problem)
  if solution_node.node == failure:
    print("No solution")
  else:
    astar_solution_path = path_states(solution_node.node)
    li=[]
    print(' ')
    print(" path to reach from ",start,"to ",mutiple_goals[a]," is")
    print(' ')
    print(astar_solution_path )
    print(' ')
    for i in range(len(maze)):
        maze_store = ''
        for j in range(len(maze[i])):
            if (i, j) in astar_solution_path :
                maze_store += '.'
            else:
                maze_store += maze[i][j]
        print(maze_store)
        li.append(maze_store)
  maze_plot(li)


# #Report for A* Search for small Maze

# In[49]:


print("Report for A* Search for small Maze")
print(' ')

report([astar_search], [problem],astar_solution_path)

# #bigMaze.lay

# **Depth-First-Search for big maze**

# In[50]:




with open("/content/bigMaze.lay", "r") as bigMazefile:
    maze=list(bigMazefile)


start = None
goal = None
mutiple_goals={}
k=0
for i in range(len(maze)):
    maze[i] = maze[i].replace("\n", "")
    for j in range(len(maze[i])):
        if maze[i][j] == 'P':
            start = (i, j)
        elif maze[i][j] == '.':
            goal= (i, j)
            mutiple_goals[k]=goal
            k=k+1
print(start,goal)
maze_plot(maze)
for a in range(k):
  problem = Maze_Problem(maze, start, mutiple_goals[a])
  solution_node = dfs(problem)
  if solution_node.node == failure:
    print("No solution")
  else:
    dfs_solution_path = path_states(solution_node.node)
    li=[]
    print(' ')
    print(" path to reach from ",start,"to ",mutiple_goals[a]," is")
    print(' ')
    print(dfs_solution_path )
    print(' ')
    for i in range(len(maze)):
        maze_store = ''
        for j in range(len(maze[i])):
            if (i, j) in dfs_solution_path :
                maze_store += '.'
            else:
                maze_store += maze[i][j]
        print(maze_store)
        li.append(maze_store)
  print(' ')
  print(' ')
  maze_plot(li)



# #Report for Depth-First-Search for big Maze

# In[51]:



print("Report for Depth-First-Search for big Maze")
print(' ')

report([dfs], [problem],dfs_solution_path)


# #A* search for big Maze

# In[52]:



with open("/content/bigMaze.lay", "r") as bigMazefile:
    maze=list(bigMazefile)



start = None
goal = None
mutiple_goals={}
k=0
for i in range(len(maze)):
    maze[i] = maze[i].replace("\n", "")
    for j in range(len(maze[i])):
        if maze[i][j] == 'P':
            start = (i, j)
        elif maze[i][j] == '.':
            goal= (i, j)
            mutiple_goals[k]=goal
            k=k+1
print(start,goal)
maze_plot(maze)
for a in range(k):
  problem = Maze_Problem(maze, start, mutiple_goals[a])
  solution_node = astar_search(problem)

  if solution_node.node == failure:
    print("No solution")
  else:
    astar_solution_path = path_states(solution_node.node)
    li=[]
    print(' ')
    print(" path to reach from ",start,"to ",mutiple_goals[a]," is")
    print(' ')
    print(astar_solution_path )
    print(' ')
    for i in range(len(maze)):
        maze_store = ''
        for j in range(len(maze[i])):
            if (i, j) in astar_solution_path :
                maze_store += '.'
            else:
                maze_store += maze[i][j]
        print(maze_store)
        li.append(maze_store)
  maze_plot(li)



# #Report for A* Search for big Maze

# In[53]:


print("Report for A* Search for big Maze")
print(' ')

report([astar_search], [problem],astar_solution_path)

# #mediumMaze.lay

# **Depth-First-Search for medium maze**

# In[54]:


with open("/content/mediumMaze.lay", "r") as mediumMazefile:
    maze=list(mediumMazefile)


start = None
goal = None
mutiple_goals={}
k=0
for i in range(len(maze)):
    maze[i] = maze[i].replace("\n", "")
    for j in range(len(maze[i])):
        if maze[i][j] == 'P':
            start = (i, j)
        elif maze[i][j] == '.':
            goal= (i, j)
            mutiple_goals[k]=goal
            k=k+1
print(start,goal)
maze_plot(maze)
for a in range(k):
  problem = Maze_Problem(maze, start, mutiple_goals[a])
  solution_node = dfs(problem)
  if solution_node.node == failure:
    print("No solution")
  else:
    dfs_solution_path = path_states(solution_node.node)
    li=[]
    print(' ')
    print(" path to reach from ",start,"to ",mutiple_goals[a]," is")
    print(' ')
    print(dfs_solution_path )
    print(' ')
    for i in range(len(maze)):
        maze_store = ''
        for j in range(len(maze[i])):
            if (i, j) in dfs_solution_path :
                maze_store += '.'
            else:
                maze_store += maze[i][j]
        print(maze_store)
        li.append(maze_store)
  print(' ')
  print(' ')
  maze_plot(li)


# #Report for Depth-First-Search for medium Maze

# In[55]:


print("Report for Depth-First-Search for medium Maze")
print(' ')

report([dfs], [problem],dfs_solution_path)

# #A* search for medium Maze

# In[56]:


with open("/content/mediumMaze.lay", "r") as mediumMazefile:
    maze=list(mediumMazefile)


start = None
goal = None
mutiple_goals={}
k=0
for i in range(len(maze)):
    maze[i] = maze[i].replace("\n", "")
    for j in range(len(maze[i])):
        if maze[i][j] == 'P':
            start = (i, j)
        elif maze[i][j] == '.':
            goal= (i, j)
            mutiple_goals[k]=goal
            k=k+1
print(start,goal)
maze_plot(maze)
for a in range(k):
  problem = Maze_Problem(maze, start, mutiple_goals[a])
  solution_node = astar_search(problem)
  if solution_node.node == failure:
    print("No solution")
  else:
    astar_solution_path = path_states(solution_node.node)
    li=[]
    print(' ')
    print(" path to reach from ",start,"to ",mutiple_goals[a]," is")
    print(' ')
    print(astar_solution_path )
    print(' ')
    for i in range(len(maze)):
        maze_store = ''
        for j in range(len(maze[i])):
            if (i, j) in astar_solution_path :
                maze_store += '.'
            else:
                maze_store += maze[i][j]
        print(maze_store)
        li.append(maze_store)
  maze_plot(li)


# #Report for A* Search for medium Maze

# In[57]:


print("Report for A* Search for medium Maze")
print(' ')

report([astar_search], [problem],astar_solution_path)

# #openMaze.lay

# **Depth-First-Search for open maze**

# In[58]:


with open("/content/openMaze.lay", "r") as openMazefile:
    maze=list(openMazefile)



start = None
goal = None
mutiple_goals={}
k=0
for i in range(len(maze)):
    maze[i] = maze[i].replace("\n", "")
    for j in range(len(maze[i])):
        if maze[i][j] == 'P':
            start = (i, j)
        elif maze[i][j] == '.':
            goal= (i, j)
            mutiple_goals[k]=goal
            k=k+1
print(start,goal)
maze_plot(maze)
for a in range(k):
  problem = Maze_Problem(maze, start, mutiple_goals[a])
  solution_node = dfs(problem)
  if solution_node.node == failure:
    print("No solution")
  else:
    dfs_solution_path = path_states(solution_node.node)
    li=[]
    print(' ')
    print(" path to reach from ",start,"to ",mutiple_goals[a]," is")
    print(' ')
    print(dfs_solution_path )
    print(' ')
    for i in range(len(maze)):
        maze_store = ''
        for j in range(len(maze[i])):
            if (i, j) in dfs_solution_path :
                maze_store += '.'
            else:
                maze_store += maze[i][j]
        print(maze_store)
        li.append(maze_store)
  print(' ')
  print(' ')
  maze_plot(li)


# #Report for Depth-First-Search for open Maze

# In[59]:


print("Report for Depth-First-Search for open Maze")
print(' ')

report([dfs], [problem],dfs_solution_path)

# #A* search for open Maze

# The A* algorithm stands out among search algorithms such as Breadth-First Search (BFS) and Depth-First Search (DFS) for finding the shortest path to a goal state. While BFS and DFS can be effective for exploring and reaching a goal state, they do not guarantee the discovery of the shortest path. A* combines the advantages of both informed and uninformed search by using a heuristic to prioritize the most promising paths. This makes it particularly efficient in finding the optimal solution, as it evaluates nodes based on both the cost to reach them and an estimate of the remaining cost to the goal. Consequently, A* not only reaches the goal state but does so via the shortest path, making it a powerful tool for pathfinding in various applications such as robotics, game development, and navigation systems.

# In[60]:


with open("/content/openMaze.lay", "r") as openMazefile:
    maze=list(openMazefile)



start = None
goal = None
mutiple_goals={}
k=0
for i in range(len(maze)):
    maze[i] = maze[i].replace("\n", "")
    for j in range(len(maze[i])):
        if maze[i][j] == 'P':
            start = (i, j)
        elif maze[i][j] == '.':
            goal= (i, j)
            mutiple_goals[k]=goal
            k=k+1
print(start,goal)
maze_plot(maze)
for a in range(k):
  problem = Maze_Problem(maze, start, mutiple_goals[a])
  solution_node = astar_search(problem)
  if solution_node.node == failure:
    print("No solution")
  else:
    astar_solution_path = path_states(solution_node.node)
    li=[]
    print(' ')
    print(" path to reach from ",start,"to ",mutiple_goals[a]," is")
    print(' ')
    print(astar_solution_path )
    print(' ')
    for i in range(len(maze)):
        maze_store = ''
        for j in range(len(maze[i])):
            if (i, j) in astar_solution_path :
                maze_store += '.'
            else:
                maze_store += maze[i][j]
        print(maze_store)
        li.append(maze_store)
  maze_plot(li)


# #Report for A* Search for open Maze

# In[61]:


print("Report for A* Search for open Maze")
print(' ')

report([astar_search], [problem],astar_solution_path)

# #smallSearch.lay

# **Depth-First-Search**

# In[62]:


import string
with open("/content/smallSearch.lay", "r") as smallSearchfile:
    maze=list(smallSearchfile)

start = None
goal = None
mutiple_goals={}
k=0
Final_path=[]
for i in range(len(maze)):
    maze[i] = maze[i].replace("\n", "")
    for j in range(len(maze[i])):
        if maze[i][j] == 'P':
            start = (i, j)
        elif maze[i][j] == '.':
            goal= (i, j)
            mutiple_goals[k]=goal
            k=k+1
print(start,mutiple_goals)
maze_plot(maze)
for a in range(k):
  problem = Maze_Problem(maze, start, mutiple_goals[a])
  solution_node = dfs(problem)
  print(' ')


  if solution_node.node == failure:
    print("No solution")
  else:
    dfs_solution_path = path_states(solution_node.node)
    Final_path+=dfs_solution_path
    li=[]
    print(' ')
    print(" path to reach from ",start,"to ",mutiple_goals[a]," is")
    print(' ')
    print(dfs_solution_path )
    print(' ')
    for i in range(len(maze)):
        maze_store = ''
        for j in range(len(maze[i])):
            if (i, j) in dfs_solution_path :
                maze_store += '.'
                maze[i] = list(maze[i])
                maze[i][j]= '.'
            else:
                maze_store += maze[i][j]
        print(maze_store)
        li.append(maze_store)
  maze_plot(li)
  start=mutiple_goals[a]
  maze=maze
  print(' ')
  report([dfs], [problem],dfs_solution_path)
li=[]
for i in range(len(maze)):
  maze_store = ''
  for j in range(len(maze[i])):
    if (i, j) in Final_path :
      maze_store += '.'
    else:
      maze_store += maze[i][j]
  print(maze_store)
  li.append(maze_store)
print("overall path")
maze_plot(li)
print("final path from starting point to the last goal",Final_path)

# A* search for smallSearch

# In[63]:


import string
with open("/content/smallSearch.lay", "r") as smallSearchfile:
    maze=list(smallSearchfile)

start = None
goal = None
mutiple_goals={}
k=0
Final_path=[]
for i in range(len(maze)):
    maze[i] = maze[i].replace("\n", "")
    for j in range(len(maze[i])):
        if maze[i][j] == 'P':
            start = (i, j)
        elif maze[i][j] == '.':
            goal= (i, j)
            mutiple_goals[k]=goal
            k=k+1
print(start,mutiple_goals)
maze_plot(maze)
for a in range(k):
  problem = Maze_Problem(maze, start, mutiple_goals[a])
  solution_node= astar_search(problem)
  print(' ')


  if solution_node.node == failure:
    print("No solution")
  else:
    astar_solution_path = path_states(solution_node.node)
    Final_path+=astar_solution_path
    li=[]
    print(' ')
    print(" path to reach from ",start,"to ",mutiple_goals[a]," is")
    print(' ')
    print(astar_solution_path )
    print(' ')
    for i in range(len(maze)):
        maze_store = ''
        for j in range(len(maze[i])):
            if (i, j) in astar_solution_path :
                maze_store += '.'
                maze[i] = list(maze[i])
                maze[i][j]= '.'
            else:
                maze_store += maze[i][j]
        print(maze_store)
        li.append(maze_store)
  maze_plot(li)
  start=mutiple_goals[a]
  maze=maze
  print(' ')
  report([astar_search], [problem],astar_solution_path)
li=[]
for i in range(len(maze)):
  maze_store = ''
  for j in range(len(maze[i])):
    if (i, j) in Final_path :
      maze_store += '.'
    else:
      maze_store += maze[i][j]
  print(maze_store)
  li.append(maze_store)
print("overall path")
maze_plot(li)
print("final path from starting point to the last goal",Final_path)


# #trickySearch.lay

# **Depth-First-Search**

# In[64]:



with open("/content/trickySearch.lay", "r") as trickySearchfile:
    maze=list(trickySearchfile)


start = None
goal = None
mutiple_goals={}
k=0
Final_path=[]
for i in range(len(maze)):
    maze[i] = maze[i].replace("\n", "")
    for j in range(len(maze[i])):
        if maze[i][j] == 'P':
            start = (i, j)
        elif maze[i][j] == '.':
            goal= (i, j)
            mutiple_goals[k]=goal
            k=k+1
print(start,mutiple_goals)
maze_plot(maze)
for a in range(k):
  problem = Maze_Problem(maze, start, mutiple_goals[a])
  solution_node = dfs(problem)
  print(' ')


  if solution_node.node == failure:
    print("No solution")
  else:
    dfs_solution_path = path_states(solution_node.node)
    Final_path+=dfs_solution_path
    li=[]
    print(' ')
    print(" path to reach from ",start,"to ",mutiple_goals[a]," is")
    print(' ')
    print(dfs_solution_path )
    print(' ')
    for i in range(len(maze)):
        maze_store = ''
        for j in range(len(maze[i])):
            if (i, j) in dfs_solution_path :
                maze_store += '.'
                maze[i] = list(maze[i])
                maze[i][j]= '.'
            else:
                maze_store += maze[i][j]
        print(maze_store)
        li.append(maze_store)
  maze_plot(li)
  start=mutiple_goals[a]
  maze=maze
  print(' ')
  report([dfs], [problem],dfs_solution_path)
li=[]
for i in range(len(maze)):
  maze_store = ''
  for j in range(len(maze[i])):
    if (i, j) in Final_path :
      maze_store += '.'
    else:
      maze_store += maze[i][j]
  print(maze_store)
  li.append(maze_store)
print("overall path")
maze_plot(li)
print("final path from starting point to the last goal",Final_path)


# #A* search

# In[65]:



with open("/content/trickySearch.lay", "r") as trickySearchfile:
    maze=list(trickySearchfile)


start = None
goal = None
mutiple_goals={}
k=0
Final_path=[]
for i in range(len(maze)):
    maze[i] = maze[i].replace("\n", "")
    for j in range(len(maze[i])):
        if maze[i][j] == 'P':
            start = (i, j)
        elif maze[i][j] == '.':
            goal= (i, j)
            mutiple_goals[k]=goal
            k=k+1
print(start,mutiple_goals)
maze_plot(maze)
for a in range(k):
  problem = Maze_Problem(maze, start, mutiple_goals[a])
  solution_node = astar_search(problem)
  print(' ')


  if solution_node.node == failure:
    print("No solution")
  else:
    astar_solution_path = path_states(solution_node.node)
    Final_path+=astar_solution_path
    li=[]
    print(' ')
    print(" path to reach from ",start,"to ",mutiple_goals[a]," is")
    print(' ')
    print(astar_solution_path )
    print(' ')
    for i in range(len(maze)):
        maze_store = ''
        for j in range(len(maze[i])):
            if (i, j) in astar_solution_path :
                maze_store += '.'
                maze[i] = list(maze[i])
                maze[i][j]= '.'
            else:
                maze_store += maze[i][j]
        print(maze_store)
        li.append(maze_store)
  maze_plot(li)
  start=mutiple_goals[a]
  maze=maze
  print(' ')
  report([astar_search], [problem],astar_solution_path)
li=[]
for i in range(len(maze)):
  maze_store = ''
  for j in range(len(maze[i])):
    if (i, j) in Final_path :
      maze_store += '.'
    else:
      maze_store += maze[i][j]
  print(maze_store)
  li.append(maze_store)
print("overall path")
maze_plot(li)
print("final path from starting point to the last goal",Final_path)


# #tinySearch.lay

# #Depth-First-Search

# In[66]:



with open("/content/tinySearch.lay", "r") as tinySearchfile:
    maze=list(tinySearchfile)


start = None
goal = None
mutiple_goals={}
k=0
Final_path=[]
for i in range(len(maze)):
    maze[i] = maze[i].replace("\n", "")
    for j in range(len(maze[i])):
        if maze[i][j] == 'P':
            start = (i, j)
        elif maze[i][j] == '.':
            goal= (i, j)
            mutiple_goals[k]=goal
            k=k+1
print(start,mutiple_goals)
maze_plot(maze)
for a in range(k):
  problem = Maze_Problem(maze, start, mutiple_goals[a])
  solution_node = dfs(problem)
  print(' ')


  if solution_node.node == failure:
    print("No solution")
  else:
    dfs_solution_path = path_states(solution_node.node)
    Final_path+=dfs_solution_path
    li=[]
    print(' ')
    print(" path to reach from ",start,"to ",mutiple_goals[a]," is")
    print(' ')
    print(dfs_solution_path )
    print(' ')
    for i in range(len(maze)):
        maze_store = ''
        for j in range(len(maze[i])):
            if (i, j) in dfs_solution_path :
                maze_store += '.'
                maze[i] = list(maze[i])
                maze[i][j]= '.'
            else:
                maze_store += maze[i][j]
        print(maze_store)
        li.append(maze_store)
  maze_plot(li)
  start=mutiple_goals[a]
  maze=maze
  print(' ')
  report([dfs], [problem],dfs_solution_path)
li=[]
for i in range(len(maze)):
  maze_store = ''
  for j in range(len(maze[i])):
    if (i, j) in Final_path :
      maze_store += '.'
    else:
      maze_store += maze[i][j]
  print(maze_store)
  li.append(maze_store)
print("overall path")
maze_plot(li)
print("final path from starting point to the last goal",Final_path)


# A* search for tinySearch including report for each goal state

# In[67]:



with open("/content/tinySearch.lay", "r") as tinySearchfile:
    maze=list(tinySearchfile)

start = None
goal = None
mutiple_goals={}
k=0
Final_path=[]
for i in range(len(maze)):
    maze[i] = maze[i].replace("\n", "")
    for j in range(len(maze[i])):
        if maze[i][j] == 'P':
            start = (i, j)
        elif maze[i][j] == '.':
            goal= (i, j)
            mutiple_goals[k]=goal
            k=k+1
print(start,mutiple_goals)
maze_plot(maze)
for a in range(k):
  problem = Maze_Problem(maze, start, mutiple_goals[a])
  solution_node = astar_search(problem)
  print(' ')


  if solution_node.node == failure:
    print("No solution")
  else:
    astar_solution_path = path_states(solution_node.node)
    Final_path+=astar_solution_path
    li=[]
    print(' ')
    print(" path to reach from ",start,"to ",mutiple_goals[a]," is")
    print(' ')
    print(astar_solution_path )
    print(' ')
    for i in range(len(maze)):
        maze_store = ''
        for j in range(len(maze[i])):
            if (i, j) in astar_solution_path :
                maze_store += '.'
                maze[i] = list(maze[i])
                maze[i][j]= '.'
            else:
                maze_store += maze[i][j]
        print(maze_store)
        li.append(maze_store)
  maze_plot(li)
  start=mutiple_goals[a]
  maze=maze
  print(' ')
  report([astar_search], [problem],astar_solution_path)
li=[]
for i in range(len(maze)):
  maze_store = ''
  for j in range(len(maze[i])):
    if (i, j) in Final_path :
      maze_store += '.'
    else:
      maze_store += maze[i][j]
  print(maze_store)
  li.append(maze_store)
print("overall path")
maze_plot(li)
print("final path from starting point to the last goal",Final_path)


# In[ ]:



