# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    IMP.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Corey <390583019@qq.com>                   +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/12/01 19:48:25 by Corey             #+#    #+#              #
#    Updated: 2018/12/01 20:02:18 by Corey            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import getopt
import copy
import time
import random
import numpy as np

SOCIAL_NETWORK = ''
SIZE = 0 # predefined size of seed set
DIFFUSION_MODEL = ''
TIME_BUDGET = 0
N = 10000

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


def main():
    try:
        network = open(SOCIAL_NETWORK)

        vertices, edges = network.readline().split()
        graph = Graph(vertices, edges)
        for line in network:
            start, end, weight = int(line.split()[0]), int(
                line.split()[1]), float(line.split()[2])
            edge = Edge(start, end, weight)
            graph.addEdge(edge)


        print(graph.getWeightsMatrix())

    except IOError:
        print('File Not Found!')

class Edge():
    def __init__(self, start, end, weight):
        self.start = start
        self.end = end
        self.weight = weight
        pass


class Graph():
    def __init__(self, vertices=0, edges=0):
        self.vertices = int(vertices)
        self.edges = int(edges)
        self.__edges = []  # edges list

        # weight matrix
        self.__weight = np.zeros([self.vertices+1, self.vertices+1])
        self.__weight[self.__weight == 0] = -1
        # -1 represents no edge, others represent the weight of the edge.
        pass

    def addEdge(self, edge):
        self.__edges.append(edge)
        self.__weight[edge.start, edge.end] = edge.weight
        pass

    def getEdges(self):
        return copy.deepcopy(self.__edges)

    def getWeightsMatrix(self):
        return copy.deepcopy(self.__weight)

    def getInNeighbors(self, node):
        result = np.where(self.getWeightsMatrix()[:, node] != -1)
        return list(result[0])

    def getInDegree(self, node):
        return len(self.getInNeighbors(node))

    def getOutNeighbors(self, node):
        result = np.where(self.getWeightsMatrix()[node] != -1)
        return list(result[0])

    def getNeighbors(self, node):
        In = self.getInNeighbors(node)
        Out = self.getOutNeighbors(node)
        result = set(In+Out)
        return list(result)


if __name__ == "__main__":
    main()
