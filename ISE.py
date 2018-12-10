# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ISE.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Corey <390583019@qq.com>                   +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/11/26 21:42:36 by Corey             #+#    #+#              #
#    Updated: 2018/12/10 17:36:55 by Corey            ###   ########.fr        #
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
        TIME_BUDGET = int(value)
if DIFFUSION_MODEL != 'IC' and DIFFUSION_MODEL != 'LT':
    raise ValueError('Diffusion Model Can Only Be "IC" or "LT"!')

def main(model, n):
    try:
        start_time = time.time()
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

        # print(graph.getWeight(9,5))
        esti = Estimator(model)

        once_start = time.time()
        result = esti.estimate(graph, seeds)
        once_time = time.time()-once_start

        for i in range(n-1):
            result += esti.estimate(graph, seeds)
            if (time.time()-start_time) > (TIME_BUDGET-(once_time+1)):
                result /= (i+1)
                print(result)
                return
        result /= n
        print(result)
        print('time cost: ',time.time()-start_time)

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
        self.weightTable = dict()  # weight table (out)   
        self.inWeightTable = dict()  # inverse weight table (in)
        pass

    def addEdge(self, edge):
        try:
            self.weightTable[edge.start][edge.end] = edge.weight
        except KeyError:
            self.weightTable[edge.start] = dict()
            self.weightTable[edge.start][edge.end] = edge.weight

        try:
            self.inWeightTable[edge.end][edge.start] = edge.weight
        except KeyError:
            self.inWeightTable[edge.end] = dict()
            self.inWeightTable[edge.end][edge.start] = edge.weight
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
    def getWeight(self,start,end):
        try:
            return self.weightTable[start][end]
        except:
            return 0
    
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
                neighbors = network.getOutNeighbors(each_seed).keys()
                inActivity = set(neighbors)-total_activity
                for each_inactivity_neighbor in inActivity:
                    weight = network.getWeight(each_seed,each_inactivity_neighbor)
                    # weight = network.getWeightsMatrix()[each_seed, each_inactivity_neighbor]
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
                neighbors = network.getOutNeighbors(each_seed).keys()
                inActivity = set(neighbors)-total_activity
                for each_inactivity_neighbor in inActivity:
                    itsNeighbors = set(network.getInNeighbors(each_inactivity_neighbor).keys())
                    itsNeighbors = itsNeighbors & total_activity
                    w_total = 0
                    for each_neighbor in itsNeighbors:
                        w_total += network.getWeight(each_neighbor, each_inactivity_neighbor)
                    if w_total >= thresholds[each_inactivity_neighbor]:
                        newActivity.add(each_inactivity_neighbor)
                        total_activity.add(each_inactivity_neighbor)
            activity = newActivity
        count = len(total_activity)
        return count

if __name__ == "__main__":
    main(DIFFUSION_MODEL, N)
