# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    IMP.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Corey <390583019@qq.com>                   +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/12/01 19:48:25 by Corey             #+#    #+#              #
#    Updated: 2018/12/11 10:23:19 by Corey            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import getopt
import copy
import time
import random
import numpy as np
import ISE

SOCIAL_NETWORK = ''
SIZE = 0 # predefined size of seed set
DIFFUSION_MODEL = ''
TIME_BUDGET = 0
N = 1000


def main(graph,model,size,timeLimit):
    nodeSet = set()
    for i in range(graph.vertices):
        nodeSet.add(i+1)
    seeds = []    
    for i in range(SIZE):
        maxNode = 0
        maxMargin = 0
        for node in nodeSet:
            tmp = copy.deepcopy(seeds)
            tmp.append(node)
            result = ISE.iseInterface(graph, tmp, model, N)
            if result > maxMargin:
                maxMargin = result
                maxNode = node
        seeds.append(maxNode)
        nodeSet.remove(maxNode)
    
    for seed in seeds:
        print(seed)
    # print('influence: ', ISE.iseInterface(graph, seeds, model, 10000))


class Graph():
    def __init__(self, vertices=0, edges=0):
        self.vertices = int(vertices)
        self.edges = int(edges)
        self.weightTable = dict()  # weight table (out)
        self.inWeightTable = dict()  # inverse weight table (in)

    def addEdge(self, start, end, weight):
        try:
            self.weightTable[start][end] = weight
        except KeyError:
            self.weightTable[start] = dict()
            self.weightTable[start][end] = weight

        try:
            self.inWeightTable[end][start] = weight
        except KeyError:
            self.inWeightTable[end] = dict()
            self.inWeightTable[end][start] = weight
        pass


    def getInNeighbors(self, node):
        try:
            return self.inWeightTable[node]
        except KeyError:
            return dict()

    def getOutNeighbors(self, node):
        try:
            return self.weightTable[node]
        except KeyError:
            return dict()

    def getWeight(self, start, end):
        try:
            return self.weightTable[start][end]
        except:
            return 0

if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "i:k:m:t:")
    for op, value in opts:
        if op == '-i':
            SOCIAL_NETWORK = value
        if op == '-k':
            SIZE = int(value)
        if op == '-m':
            DIFFUSION_MODEL = value
        if op == '-t':
            TIME_BUDGET = int(value)
    if DIFFUSION_MODEL != 'IC' and DIFFUSION_MODEL != 'LT':
        raise ValueError('Diffusion Model Can Only Be "IC" or "LT"!')
    start_time = time.time()
    try:
        network = open(SOCIAL_NETWORK)
        vertices, edges = network.readline().split()
        graph = Graph(vertices, edges)
        for line in network:
            start, end, weight = int(line.split()[0]), int(
                line.split()[1]), float(line.split()[2])
            graph.addEdge(start, end, weight)
    except IOError:
        print('File Not Found!')
    main(graph,DIFFUSION_MODEL,SIZE,TIME_BUDGET)
    # print('time cost: ', time.time()-start_time)
