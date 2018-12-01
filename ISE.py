# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ISE.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Corey <390583019@qq.com>                   +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/11/26 21:42:36 by Corey             #+#    #+#              #
#    Updated: 2018/12/01 19:44:29 by Corey            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import getopt
import copy
import time
import random
import numpy as np


SOCIAL_NETWORK = ''
SEED_SET = ''
DIFFUSION_MODEL = ''
TIME_BUDGET = 0
N = 10000

opts, args = getopt.getopt(sys.argv[1:], "i:s:m:t:")
for op, value in opts:
    if op == '-i':
        SOCIAL_NETWORK = value
    if op == '-s':
        SEED_SET = value
    if op == '-m':
        DIFFUSION_MODEL = value
    if op == '-t':
        TIME_BUDGET = value
if DIFFUSION_MODEL != 'IC' and DIFFUSION_MODEL != 'LT':
    raise ValueError('Diffusion Model Can Only Be "IC" or "LT"!')

def main():
    try:
        network = open(SOCIAL_NETWORK)
        seed = open(SEED_SET)

        vertices, edges = network.readline().split()
        graph = Graph(vertices,edges)
        for line in network:
            start, end, weight = int(line.split()[0]), int(line.split()[1]),float(line.split()[2])
            edge = Edge(start, end, weight)
            graph.addEdge(edge)

        seeds = []
        for line in seed:
            seeds.append(int(line.split()[0]))

        esti = Estimator(DIFFUSION_MODEL)
        result = 0
        for i in range(N):
            result += esti.estimate(graph, seeds)
        result /= N
        print(result)

    except IOError:
        print('File Not Found!')
        pass
    
    # for debug
    # print(np.where(graph.getWeightsMatrix()>0))
    # print(seeds)
    # print(graph.getOutNeighbors(10))
    

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
        self.__edges = [] # edges list

        # weight matrix
        self.__weight = np.zeros([self.vertices+1,self.vertices+1])
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
    
    def getInNeighbors(self,node):
        result = np.where(self.getWeightsMatrix()[:,node]!=-1)
        return list(result[0])
    
    def getInDegree(self,node):
        return len(self.getInNeighbors(node))

    def getOutNeighbors(self,node):
        result = np.where(self.getWeightsMatrix()[node] != -1)
        return list(result[0])

    def getNeighbors(self,node):
        In = self.getInNeighbors(node)
        Out = self.getOutNeighbors(node)
        result = set(In+Out)
        return list(result)
        


class Estimator():
    def __init__(self, model):
        self.model = model # IC/LT
        pass

    def estimate(self, network, seed):
        if self.model == 'IC':
            result = self.estimate_ic(network, seed)
        elif self.model == 'LT':
            result= self.estimate_lt(network, seed)
        return result 

    def estimate_ic(self, network, seed):
        total_activity = set(seed)
        activity = set(seed)
        while(len(activity)):
            newActivity = set()
            for each_seed in activity:
                neighbors = network.getNeighbors(each_seed)
                inActivity = set(neighbors)-total_activity
                for each_inactivity_neighbor in inActivity:
                    weight = network.getWeightsMatrix()[each_seed, each_inactivity_neighbor]
                    probability = random.random()
                    if probability < weight: # successfully activated
                        newActivity.add(each_inactivity_neighbor)
                        total_activity.add(each_inactivity_neighbor)
            activity = newActivity
        count = len(total_activity)
        return count       

    def estimate_lt(self, network, seed):
        total_activity = set(seed)
        activity = set(seed)
        thresholds = {}
        for i in range(1,network.edges+1):
            threshold = random.random()
            thresholds[i] = threshold
            if threshold == 0:
                activity.add(i)
                total_activity.add(i)
        while(len(activity)):
            newActivity = set()
            for each_seed in activity:
                neighbors = network.getNeighbors(each_seed)
                inActivity = set(neighbors)-total_activity
                for each_inactivity_neighbor in inActivity:
                    itsNeighbors = set(network.getInNeighbors(each_inactivity_neighbor))
                    itsNeighbors = itsNeighbors & total_activity
                    w_total = 0
                    for each_neighbor in itsNeighbors:
                        w_total += network.getWeightsMatrix()[each_neighbor, each_inactivity_neighbor]
                    if w_total >= thresholds[each_inactivity_neighbor]:
                        newActivity.add(each_inactivity_neighbor)
                        total_activity.add(each_inactivity_neighbor)
            activity = newActivity
        count = len(total_activity)
        return count
    




if __name__ == "__main__":
    main()
