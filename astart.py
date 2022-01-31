# reference: https://youtu.be/-L-WgKMFuhE?t=587
# g-cst = distance from starting node (captures how long the path is)
# h-cst = distance from the end node
# f-cst = g-cst + h-cst

import utils
import numpy as np
import math
import pdb


filename = 'test_map.txt'
# pdb.set_trace()
world = utils.readArrayFromFile(filename)
start = (0, 0)
end = (0, 4)


class grid_world:

    def __init__(self, world, start, end):
        self.open_list = []
        self.closed_list = []
        self.parentOf = {}
        self.f_costs = {}
        self._x_dim = len(world)
        self._y_dim = len(world[0])
        self.start = start
        self.end = end
        self.world = world

    def run_a_start(self):
        # add start to open
        open_list.append(self.start)
        while True:
            current = getLowestCostNode()
            open_list.remove(current)
            closed_list.append(current)

            if current == end:
                break
            for neighbor in neighborsOf(current):
                if isNotTraversible(neighbor) or neighbor in closed_list:
                    continue

                # calculate f cost of node
                g_tmp = f_costs[current] + 1
                h_tmp = linearDistance(neighbor, end)
                f_tmp = g_tmp + h_tmp

                if hasFoundShorterPathToNode(neighbor, f_tmp) or neighbor not in open_list:
                    f_costs[nieghbor] = f_tmp
                    parentOf[neighbor] = current
                    if neighbor not in open_list:
                        open_list.append(neighbor) # TODO: must add and sort list


    def hasFoundShorterPathToNode(self, node, newCost):
        if node in self.f_costs:
            costOnRecord = self.f_costs[node]
            if newCost < costOnRecord:
                return True
        return False

    def linearDistance(self, p1, p2):
        x1 = p1[0]
        y1 = p1[1]
        x2 = p1[0]
        y2 = p1[1]
        dist = math.sqrt((y2 - y1)** 2 + (x2 - x2)**2)
        return dist
    

    def getLowestCostNode(self,):
        item = self.open_list[-1]
        self.open_list.pop()
        return item

    def neighborsOf(self, node):
        x = node[0]
        y = node[1]

        north = (x, y+1)
        west  = (x-1, y)
        south = (x, y-1)
        east  = (x+1, y)
        return [north,west,south,east]


    def isNotTraversible(self, node):
        x = node[0]
        y = node[1]
        if x < 0 or x >= self.x_dim or y < 0 or y >= self.y_dim:
            # out of bounds
            return True
        elif self.world[x][y] == 1:
            # ran into wall
            return True
        return False

    

class grid_cell:
    def __init__(self, tup, score):
      self.coord = tup
      self.score = score

    def __eq__(self, other):
        if (self.coord == other.coord):
            return True
        return False
    def __le__(self, other):
        if (self.score <= other.score):
            return True
        return False
    def __lt__(self, other):
        if (self.score <= other.score):
            return True
        return False  
