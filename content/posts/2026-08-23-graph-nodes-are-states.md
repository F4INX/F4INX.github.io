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

Imagine a travel problem where travellers should calculate their trip so that they either go through country A, or through country B, or through neither, but must not go through both countries.

![Map with three countries A, B, and a neutral one, connected by roads between nodes 11, 21-23, 31-33, 41-43, and 51.](/posts/graph-nodes-are-states/graph-01.svg)

A possible solution to this problem would be to tweak the algorithm used to solve this graph: either calculating shortest routes between sub-domains, or calculating the k shortest routes to be able to take alternative paths in the case the shortest path is forbidden, and so on.

A more straightforward way is to consider **states as nodes** and to apply the usual algorithms directly. Here, the states would be like ```(11,none)``` for the starting node, ```(31,A)``` after ```(11,none)->(21,A)```, or ```(31,B)``` after ```(11,none)->(31,B)```, and so on. Note that this graph would be directional, which could surprise people used to the *locations as nodes* approach but is barely noticed for people used to the *states as nodes* approach.

The total number of nodes in this approach is multiplied by the number of the states. On the one hand, it can be troublesome for algorithms relying on various arrays to do their job, but this drawback may be overcome by the simplification of the algorithm. On the other hand, this is not at all a problem in cases the graph is stored in a sparse way or lazily evaluated.

## Example 2: true states

While in the previous case the states can be seen as a convenient way to implement a constraint, in lots of cases the nodes are true states. A typical example is the study of a control flow inside a program. But there are more mundane cases.

I recently found this example in my drafts about a scheduling problem for the repair of various devices, the devices being able to be repaired only one at a time, and each device having a repair time and a cost per time unit. The example showed the application of Dijkstra's algorithm.

| Device                | Time | Unit Cost |
|-----------------------|------|-----------|
| Oven                  |   3  |     2     |
| Dishwasher (DiW)      |   2  |     3     |
| Washing machine (WaM) |   5  |     4     |
| Computer (Comp)       |   4  |     9     |
| Television (TV)       |   6  |     5     |

Initial paths:

* (1): {Oven, DiW, WaM, Comp, TV} length 0.

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

### Step 4

Development of (5) length 92.

Paths:

* (15): (5) --42--> {DiW, WaM, TV} length 134
* (16): (5) --28--> {Oven, WaM, TV} length 120
* (17): (5) --70--> {Oven, DiW, TV} length 162
* (18): (5) --84--> {Oven, DiW, WaM} length 176

Shortest unvisited path: (7) length 106.

### Step 5

Development of (7) length 106.

Paths:

* (19): (7) --90--> {Comp, TV} length 196
* (20): (7) --72--> {WaM, TV} length 178
* (21): (7) --108--> {WaM, Comp} length 214

Shortest unvisited path: (4) length 115.

### Step 6

Development of (4) length 115.

Paths:

* (22): (4) --57--> {DiW, Comp, TV} length 172
* (23): (4) --38--> {Oven, Comp, TV} length 153
* (24): (4) --76--> {Oven, DiW, TV} length 191
* (25): (4) --114--> {Oven, DiW, Comp} length 229

Shortest unvisited path: (16) length 120.

### Step 7

Development of (16) length 120.

Paths:

* (26): (16) --33--> {WaM, TV} length 153
* (27): (16) --55--> {Oven, TV} length 175
* (28): (16) --66--> {Oven, WaM} length 186

Shortest unvisited path: (15) length 134.

### Step 8

Development of (15) length 134.

Paths:

* (29): (15) --24--> {WaM, TV} length 158
* (30): (15) --60--> {DiW, TV} length 194
* (31): (15) --72--> {DiW, WaM} length 206

Shortest unvisited path: (6) length 138.

### Step 9

Development of (6) length 138.

Paths:

* (32): (6) --54--> {DiW, WaM, Comp} length 192
* (33): (6) --36--> {Oven, WaM, Comp} length 174
* (34): (6) --90--> {Oven, DiW, Comp} length 228
* (35): (6) --72--> {Oven, DiW, WaM} length 210

Shortest unvisited path: (8) length 146.

### Step 10

Development of (8) length 146.

Paths:

* (36): (8) --48--> {Comp, TV} length 194
* (37): (8) --64--> {Oven, TV} length 210
* (38): (8) --96--> {Oven, Comp} length 242

Shortest unvisited path: (26) length 153.

### Step 11

Development of (26) length 153.

Paths:

* (39): (26) --45--> {TV} length 198
* (40): (26) --54--> {WaM} length 207

Shortest unvisited path: (17) length 162.

### Step 12

Development of (17) length 162.

Paths:

* (41): (17) --30--> {DiW, TV} length 192
* (42): (17) --20--> {Oven, TV} length 182
* (43): (17) --60--> {Oven, DiW} length 222

Shortest unvisited path: (10) length 166.

### Step 13

Development of (10) length 166.

Paths:

* (44): (10) --45--> {WaM, Comp} length 211
* (45): (10) --75--> {Oven, Comp} length 241
* (46): (10) --60--> {Oven, WaM} length 226

Shortest unvisited path: (22) length 172.

### Step 14

Development of (22) length 172.

Paths:

* (47): (22) --34--> {Comp, TV} length 206
* (48): (22) --68--> {DiW, TV} length 240
* (49): (22) --102--> {DiW, Comp} length 274

Shortest unvisited path: (27) length 175.

### Step 15

Development of (27) length 175.

Paths:

* (50): (27) --21--> {TV} length 196
* (51): (27) --42--> {Oven} length 217

Shortest unvisited path: (18) length 176.

### Step 16

Development of (18) length 176.

Paths:

* (52): (18) --27--> {DiW, WaM} length 203
* (53): (18) --18--> {Oven, WaM} length 194
* (54): (18) --45--> {Oven, DiW} length 221

Shortest unvisited path: (28) length 186.

### Step 17

Development of (28) length 186.

Paths:

* (55): (28) --18--> {WaM} length 204
* (56): (28) --30--> {Oven} length 216

Shortest unvisited path: (32) length 192.

### Step 18

Development of (32) length 192.

Paths:

* (57): (32) --32--> {WaM, Comp} length 224
* (58): (32) --80--> {DiW, Comp} length 272
* (59): (32) --64--> {DiW, WaM} length 256

Shortest unvisited path: (41) length 192.

### Step 19

Development of (41) length 192.

Paths:

* (60): (41) --16--> {TV} length 208
* (61): (41) --48--> {DiW} length 240

Shortest unvisited path: (36) length 194.

### Step 20

Development of (36) length 194.

Paths:

* (62): (36) --56--> {TV} length 250
* (63): (36) --84--> {Comp} length 278

Shortest unvisited path: (50) length 196.

### Step 21

Development of (50) length 196.

Paths:

* (64): (50) --30--> {} length 226

Shortest unvisited path: (52) length 203.

### Step 22

Development of (52) length 203.

Paths:

* (65): (52) --14--> {WaM} length 217
* (66): (52) --35--> {DiW} length 238

Shortest unvisited path: (55) length 204.

### Step 23

Development of (55) length 204.

Paths:

* (67): (55) --20--> {} length 224

Shortest unvisited path: (44) length 211.

### Step 24

Development of (44) length 211.

Paths:

* (68): (44) --65--> {Comp} length 276
* (69): (44) --52--> {WaM} length 263

Shortest unvisited path: (56) length 216.

### Step 25

Development of (56) length 216.

Paths:

* (70): (56) --6--> {} length 222

Shortest unvisited path: (54) length 221.

### Step 26

Development of (54) length 221.

Paths:

* (71): (54) --15--> {DiW} length 236
* (72): (54) --10--> {Oven} length 231

Shortest unvisited path: (70) length 222.

### Step 27

Development of (70) length 222.

Paths:

Shortest unvisited path: (34) length 228.

### Step 28

Development of (34) length 228.

Paths:

* (73): (34) --42--> {DiW, Comp} length 270
* (74): (34) --28--> {Oven, Comp} length 256
* (75): (34) --56--> {Oven, DiW} length 284

Shortest unvisited path: (71) length 236.

### Step 29

Development of (71) length 236.

Paths:

* (76): (71) --6--> {} length 242

Shortest unvisited path: (45) length 241.

### Step 30

Development of (45) length 241.

Paths:

* (77): (45) --33--> {Comp} length 274
* (78): (45) --44--> {Oven} length 285

Shortest unvisited path: (73) length 270.

### Step 31

Development of (73) length 270.

Paths:

* (79): (73) --24--> {Comp} length 294
* (80): (73) --48--> {DiW} length 318

Shortest unvisited path: (77) length 274.

### Step 32

Development of (77) length 274.

Paths:

* (81): (77) --36--> {} length 310

## Conclusion

The algorithm terminates after all paths have been developed. The optimal solution is path (70) with a total cost of 222, corresponding to the repair order: Comp, DiW, TV, WaM, Oven.

While a first approach to the analysis of a graph with constraints is to handle them with a *locations as nodes* approach and to use various techniques to process the constraints, handling them with a *states as nodes* approach can lead to simpler algorithms.
