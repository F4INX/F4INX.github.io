---
title: "Graph nodes are states"
date: 2026-09-16
lastmod: 2026-09-16
categories: [Graph theory, Algorithms]
url: /posts/graph-nodes-are-states.html
excerpt: "Nodes of a graph are often seen as locations. However, seeing them as states can offer interesting solutions in cases where the paths are constrained."
---

## Introduction

When studying graph theory, the first examples proposed to students most often involve maps where nodes are geographical locations, edges physical roads with their distances, and path distances actual travel distances.

However, it is also possible to see nodes as *states*, as outlined in the following examples.

## Example 1: routing problems with constraints

*Inspired by a true problem.*

Imagine a travel problem where travellers should calculate their trip such that they either go through country A, or through country B, or through neither, but must not go through both countries.

![Map with three countries A, B, and a neutral one, connected by roads between nodes 11, 21-23, 31-33, 41-43, and 51.](/posts/graph-nodes-are-states/graph-01.svg)

A possible solution to this problem would be to tweak the algorithm used to solve this graph: either calculating shortest routes between sub-domains, or calculating the k shortest routes to be able to take alternative paths in the case the shortest path is forbidden, and so on.

A more straightforward way is to consider **states as nodes** and to apply the usual algorithms directly. Here, the states would be like ```(11,none)``` for the starting node, ```(31,A)``` after ```(11,none)->(21,A)```, or ```(31,B)``` after ```(11,none)->(31,B)```, and so on. Note that this graph would be directional, which could surprise people used to the *locations as nodes* approach but is barely noticed for people used to *states as nodes* approach.

The total number of nodes in this approach is multiplied by the number of the states. On the one hand, it can be troublesome for algorithms relying on various arrays to do their job, but this drawback may be overcome by the simplification of the algorithm. On the other hand, this is not at all a problem in cases the graph is stored in a sparse way or lazily evaluated.

## Example 2: true states

While in the previous case the states can be seen as a convenient way to implement a constraint, in lots of cases the nodes are true states. A typical example is the study of a control flow inside a program. But there are more mundane cases.

I recently found this example in my drafts about a scheduling problem for the repair of various devices, the devices being able to be repaired only one at a time, and each device having a repair time and a cost per time unit. The example showed the first steps of the application of Dijkstra's algorithm.

| Device          | Time | Unit Cost |
|-----------------|------|-----------|
| Oven            |   3  |     2     |
| Dishwasher      |   2  |     3     |
| Washing machine |   5  |     4     |
| Computer        |   4  |     9     |
| Television      |   6  |     5     |

Initial paths:
* (1): {Ov, DiW, WaM, Comp, TV} length 0.

![Initial node of the Dijkstra graph: the set of broken devices {Oven, Dishwasher, Washing machine, Computer, Television} with five outgoing edges to the subsets obtained by repairing one device, each labelled with the waiting cost for the repaired device and the remaining devices.](/posts/graph-nodes-are-states/djikstra-01.svg)

### Step 1

Development of (1) of length 0.

Paths:

* (2): (1) -> {DiW, WaM, Comp, TV} length 69
* (3): (1) -> {Oven, WaM, Comp, TV} length 46
* (4): (1) -> {Oven, DiW, Comp, TV} length 115
* (5): (1) -> {Oven, WaM, DiW, TV} length 92
* (6): (1) -> {Oven, WaM, DiW, Comp} length 138

Shortest unvisited path: (3) length 46.

### Step 2

Development of (3) length 46.

Paths:

* (7): (3) --60--> {WaM, Comp, TV} length 106
* (8): (3) --100--> {Oven, Comp, TV} length 146
* (9): (3) --80--> {Oven, WaM, TV} length 126
* (10): (3) --120--> {Oven, WaM, Comp} length 166

Shortest unvisited path: (2) length 69.

### Step 3

Development of (2) length 69.

Paths:

* (11): (2) --42--> {WaM, Comp, TV} length 111
* (12): (2) --105--> {DiW, Comp, TV} length 174
* (13): (2) --84--> {DiW, WaM, TV} length 153
* (14): (2) --126--> {DiW, WaM, Comp} length 195

Shortest unvisited path: (5) length 92.

## Conclusion

While a first approach to the analysis of graph with constraints is to handle them with a *locations as nodes* approach and to use various techniques to process the constraints, handling them with a *states as nodes* approach can lead to simpler algorithms.
