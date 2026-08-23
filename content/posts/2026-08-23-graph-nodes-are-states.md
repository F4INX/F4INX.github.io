---
title: "Graph nodes are states"
date: 2026-08-23
lastmod: 2026-08-23
categories: [Graph theory, Algorithms]
url: /posts/graph-nodes-are-states.html
# TODO: fill excerpt and related_posts.
# excerpt: "..."
# related_posts:
#   - "..."
---

## Introduction

When studying graph theory, the first examples proposed to students most often involve maps where nodes are geographical locations, edges physical roads with their distances, and path distances actual travel distances.

However, it is also possible to see nodes are *states*, as outlined in the following examples.

## Example 1: routing problems with constraints

*Inspired by a true problem.*

Imagine a travel problem where travallers should calculate their trip such than then either go through country A, or through country B, or through neither, but must not through both countries.

<!-- TODO: alt text. -->
![alt text](/posts/graph-nodes-are-states/graph-01.svg)

A possible solution to this problem would be to treak the algorithm used to solve this graph: either calculating shortest routes between sub-domains, or calculating the k shortest routes to be able to take alternative paths in the case the shortest path is forbidden, and so on.

A more straight foward way is to consider **states as nodes** and to apply straight the usual algorithms. Here, the states would be like ```(11,none)``` for the starting node, ```(31,A)``` after ```(11,none)->(21,A)```, or ```(31,B)``` after ```(11,none)->(31,B)```, and so on. Note that this graph would be directional, which could surprise people used to the *locations as nodes* approach but is barely noticed for people used to *states as nodes* approach.

The total number of nodes in this approach is multiplied by the number of the states. On the one hand, it can be troublesome for algorithms relying on various arrays to do their job, but this drawback may be overcome by the simplification of the algorithm. On the other hand, this is not at all a problem in cases the graph is stored in a sparse way or lazily evaluated.

## Example 2: true states

While in the previous case the states can be seen as a convenient way to implement a constraint, in lots of cases the nodes are true states. A typical example is the study of a control flow instead a program. But there are more mundane cases.

I recently found this example in my drafts about an ordonancement problem of the repair of various devices, the devices being able to be repaired only one at a time, and each device having a repair time and a cost per time. The example showed the first steps of the application of Djikstra algorithm.

![alt text](/posts/graph-nodes-are-states/djikstra-01.png)

![alt text](/posts/graph-nodes-are-states/djikstra-02.png)

![alt text](/posts/graph-nodes-are-states/djikstra-03.png)

![alt text](/posts/graph-nodes-are-states/djikstra-04.png)

![alt text](/posts/graph-nodes-are-states/djikstra-05.png)

## Conclusion

While a first approach to the analysis of graph with constraints is to handle them with a *locations as nodes* approach and to use various techniques to process the constraints, handling them with a *states as nodes* approaches can lead to simpler algorithms.
