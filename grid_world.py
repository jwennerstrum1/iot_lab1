# reference: https://youtu.be/-L-WgKMFuhE?t=587
# g-cst = distance from starting node (captures how long the path is)
# h-cst = distance from the end node
# f-cst = g-cst + h-cst

import utils
import numpy as np
import math
import pdb
import bisect
from collections import deque

class grid_world:

    def __init__(self, world, start, end):
        self.open_list = [] # SORTED list of open nodes
        self.closed_list = [] # UNSORTED list of open nodes
        self.parentOf = {} # Dictionary between coordinates (TUPLE) and coordinates (TUPLE)
        self.x_dim = len(world)
        self.y_dim = len(world[0])
        self.start = grid_cell(start)
        self.end = grid_cell(end)
        self.world = world
        self.f_costs = {start: 0} # Dictionary between coordinates (TUPLE) and value (double)
        self.path_to_dest = deque()


    def run_a_start(self):
        # add start to open
        bisect.insort(self.open_list, self.start)
        while True:
            current = self.popLowestCostNode()
            self.closed_list.append(current)

            if current == self.end:
                break
            for neighbor in self.neighborsOf(current):
                if self.isNotTraversible(neighbor) or neighbor in self.closed_list:
                    continue

                # calculate f cost of node
                g_tmp = self.f_costs[current.coord] + 1
                h_tmp = self.linearDistance(neighbor, self.end)
                f_tmp = g_tmp + h_tmp

                if self.hasFoundShorterPathToNode(neighbor, f_tmp) or neighbor not in self.open_list:
                    self.f_costs[neighbor.coord] = f_tmp
                    self.parentOf[neighbor.coord] = current.coord
                    if neighbor not in self.open_list:
                        neighbor.score = f_tmp
                        bisect.insort(self.open_list, neighbor)
        while True:
            coord = current.coord
            self.world[coord[0]][coord[1]] = 2
            self.path_to_dest.append(coord)
            if current == self.start:
                break
            current = grid_cell(self.parentOf[current.coord])
        return

    
    def hasFoundShorterPathToNode(self, node, newCost):
        if node.coord in self.f_costs:
            costOnRecord = self.f_costs[node.coord]
            if newCost < costOnRecord:
                return True
        return False

    def linearDistance(self, p1, p2):
        x1 = p1.coord[0]
        y1 = p1.coord[1]
        x2 = p2.coord[0]
        y2 = p2.coord[1]
        dist = math.sqrt((y2 - y1)** 2 + (x2 - x1)**2)
        return dist
    

    def popLowestCostNode(self):
        item = self.open_list.pop()
        return item

    def neighborsOf(self, node):
        x = node.coord[0]
        y = node.coord[1]

        north = grid_cell((x, y+1))
        west  = grid_cell((x-1, y))
        south = grid_cell((x, y-1))
        east  = grid_cell((x+1, y))

        return [north,west,south,east]


    def isNotTraversible(self, node):
        x = node.coord[0]
        y = node.coord[1]
        if x < 0 or x >= self.x_dim or y < 0 or y >= self.y_dim:
            # out of bounds
            return True
        elif self.world[x][y] == 1:
            # ran into wall
            return True
        return False

    

class grid_cell:
    def __init__(self, tup, score=-1):
      self.coord = tup
      self.score = score

    def __eq__(self, other):
        if (self.coord == other.coord):
            return True
        return False
    def __le__(self, other):
        # we want the lowest cost node to appear last in the list
        if (self.score >= other.score):
            return True
        return False
    def __lt__(self, other):
        # we want the lowest cost node to appear last in the list
        if (self.score > other.score):
            return True
        return False  
