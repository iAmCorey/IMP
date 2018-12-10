# IMP
# Overview
Influence Maximization Problem (IMP) is the problem of finding a small subset of nodes (referred to as seed set) in a social network that could maximize the spread of influence.
The influence spread is the expected number of nodes that are influenced by the nodes in the seed set in a cascade manner.



# File Description
executable estimator - ISE.py
executable solver - IMP.py

# Usage

## Task1: influence spread computation

`python ISE.py –i <social network> -s <seed set> -m <diffusion model> -t <time budget>`

<social network> is the absolute path of the social network file

<seed set> is the absolute path of the seed set file

<diffusion model> can only be IC or LT

<time budget> is a positive number which indicates how many seconds(in Wall clock time, range: [60s, 1200s]) your algorithm can spend on this instance. 

e.g. `python ISE.py -i network.txt -s seeds.txt -m LT -t 120`

Output:

-    The value of the estimated influence spread

## Taks2: influence maximization

`python IMP.py –i <social network> -k <predefined size of the seed set> -m <diffusion model> -t <time budget>`

<social network> is the absolute path of the social network file

<predefined size of the seed set> is a positive integer

<diffusion model> can only be IC or LT

<time budget> is a positive number which indicates how many seconds (in Wall clock time, range: [60s, 1200s]) your algorithm can spend on this instance. 

e.g. `python IMP.py -i network.txt -k 10 -m LT -t 120`

Output: 

-   The seed set found by your algorithm.

-   The format of the seed set output should be as follows: each line contains a node index. An example is also included in the package.

# Input:

-   A graph *G=(V,E)*
-   A predefined seed set cardinality *k*
-   A predefined stochastic diffsion model - *IC/LT*

# Output: 

A *size-k* seed set S' with the maximal 𝜎(𝑆) for any *size-k* seed set S ⊆ 𝑉  



# Stochastic Diffusion Models

Diffusion process: At round 0, S中的所有node变成active，其余是inactive，每一轮，每个actived node都会active它的neighbors，直到所有nodes都activated，process end.s

## Independent Cascade(IC)

一个node u active它的neighbor v的几率与weight w(u,v)成比例。

w(u,v) = v 的 in-degree 的倒数

## Linear Threshold(LT)

一开始，每一个node都有一个random threshold 𝜃（在[0,1]之间）。在round t(t>0)，一个inactive node v，如果它的所有activated neighbors u 与v的w(u,v)加起来>= 𝜃，那v就会activated。

w(u,v) = v 的 in-degree 的倒数