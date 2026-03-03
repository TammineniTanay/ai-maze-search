AI Maze Search – Classical Search Algorithms
1. Introduction

This project implements classical Artificial Intelligence search algorithms to solve maze navigation problems. The objective is to determine a path from a specified start position to a goal state within a 2D maze environment.

The project was developed as part of CS591 – Advanced Artificial Intelligence and focuses on the implementation and comparative evaluation of uninformed and informed search strategies.

2. Problem Description

The maze is represented as a two-dimensional grid:

% denotes walls.

P denotes the starting position.

. denotes the goal state(s).

The task is to:

Compute a valid path from the start state to the goal.

Compare search strategies in terms of performance.

Extend the formulation to multi-goal search scenarios.

3. Algorithms Implemented
3.1 Depth-First Search (DFS)

Explores nodes in a depth-oriented manner.

Uses a LIFO (stack-based) frontier.

Not guaranteed to find the shortest path.

Lower memory usage compared to breadth-based methods.

3.2 Best-First Search Framework

A generic best-first search algorithm was implemented using a priority queue structure. This framework enables the construction of informed search strategies.

3.3 A* Search

A* search was implemented using the evaluation function:

f(n) = g(n) + h(n)

Where:

g(n) represents the path cost from the start node to node n.

h(n) represents the heuristic estimate to the goal.

The Manhattan distance heuristic was used:

h(n) = |x₁ − x₂| + |y₁ − y₂|

This heuristic is admissible for grid-based movement without diagonal transitions, ensuring optimality of the A* solution.

4. Performance Evaluation

For each maze configuration, the following metrics were recorded:

Path cost

Number of nodes expanded

Maximum fringe size

Maximum tree depth explored

These metrics allow direct comparison between uninformed and informed search strategies.

5. Multi-Goal Search Extension

The problem was extended to handle multiple goal states. The state representation was modified to include:

(current_position, remaining_goals)

This extension increases the complexity of the state space and highlights the importance of efficient heuristic design and repeated-state detection.

6. Project Structure
ai-maze-search/
│
├── Tanay__Tammineni_P1.ipynb
├── Tanay__Tammineni_P1.pdf
├── bigMaze.lay
├── mediumMaze.lay
├── smallMaze.lay
├── openMaze.lay
├── tinySearch.lay
├── smallSearch.lay
├── trickySearch.lay
└── sample maze file.lay
7. Technologies Used

Python

Matplotlib (for visualization)

heapq (priority queue implementation)

Object-oriented design for problem abstraction

8. Learning Outcomes

This project reinforces key concepts in Artificial Intelligence:

Formal problem representation

Graph search techniques

Heuristic design and admissibility

Performance benchmarking of search algorithms

State-space modeling for complex search tasks

9. Author

Tanay Tammineni
Master’s Student – Computer Science
Course: CS591 – Advanced Artificial Intelligence