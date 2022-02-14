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

    def reset(self):
        self.open_list = []
        self.closed_list = []
        self.parentOf = {}
        self.f_costs = {self.start.coord: 0}
        self.path_to_dest = deque()
        self.remove_astar_path()
        return

    def remove_astar_path(self):
        x,y= np.where(self.world == 254)
        for i in range(len(x)):
            self.world[x[i]][y[i]] = 0
        return

    def set_start(self, start_coord):
        self.start = grid_cell(start_coord)
        self.f_costs = {start_coord: 0} # set the initial f_cost
        return

    def run_a_star(self, boundary_threshold=1):
        # add start to open
        bisect.insort(self.open_list, self.start)
        while True:
            current = self.popLowestCostNode()
            self.closed_list.append(current)

            if current == self.end:
                break
            for neighbor in self.neighborsOf(current):
                if boundary_threshold == 0:
                    boundary_threshold = 1 # edge case, for the first run of A*, consider the threshold of 1
                    
                if self.isNotTraversible(neighbor, boundary_threshold) or neighbor in self.closed_list:
                    continue

                # calculate f cost of node
                g_tmp = self.f_costs[current.coord] + 1
                h_tmp = utils.linear_distance(neighbor.coord, self.end.coord)
                f_tmp = g_tmp + h_tmp

                if self.hasFoundShorterPathToNode(neighbor, f_tmp) or neighbor not in self.open_list:
                    self.f_costs[neighbor.coord] = f_tmp
                    self.parentOf[neighbor.coord] = current.coord
                    neighbor.score = f_tmp
                    if neighbor in self.open_list:
                        #remove node from open_list and readd it with updated order
                        self.open_list.remove(neighbor)

                    neighbor.score = f_tmp
                    bisect.insort(self.open_list, neighbor)
                    
        while True:
            coord = current.coord
            self.world[coord[0]][coord[1]] = 254  # Uncomment out if you want to see the created path
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


    def isNotTraversible(self, node, boundary_threshold):
        x = node.coord[0]
        y = node.coord[1]
        if x < 0 or x >= self.x_dim or y < 0 or y >= self.y_dim:
            # out of bounds
            return True
        elif self.world[x][y] >= boundary_threshold:
            # ran into wall
            return True
        return False

    def get_x_length(self):
        return len(self.world)

    def get_y_length(self):
        return len(self.world[0])

    def get_distance_to_closest_barrier(self, location, direction):
        x = location[0]
        y = location[1]
        if direction == utils.direction.NORTH or direction == utils.direction.SOUTH:
            path = self.world[x][:]
            z = y
        else:
            path = self.world[:][y]
            z = x
        direction_sign = (((direction + 1) // 2) % 2 * 2 - 1) * -1
        # +1  -> North or East
        # -1 -> South or West
        distance_count = 1
        query_location = z + distance_count * direction_sign
        while query_location >= 0 and  query_location < len(path) :
            value_at_distance = path[query_location]
            if value_at_distance == 0 or value_at_distance == 254:
            # find the ditance to the next barrier in path (grid world entry is greater than 0)
                distance_count += 1
                query_location = z + distance_count * direction_sign
                continue
            break
            
        return distance_count

    def remove_barriers_in_path(self, location, direction):
        x = location[0]
        y = location[1]
        direction_sign = (((direction + 1) // 2) % 2 * 2 - 1) * -1
        
        if direction == utils.direction.NORTH or direction == utils.direction.SOUTH:
            x_min =  x - 1
            if x_min < 0:
                x_min = 0

            x_max = x+2
            if x_max > len(self.world):
                x_max = x_max - 1

            if direction == utils.direction.NORTH:
                y_min = y+1
                y_max = len(self.world[0])
            else:
                y_min = 0
                y_max = y

            for i in range(x_min, x_max):
                self.world[i][y_min:y_max] = 0
                
        else: # East or West
            y_min = y - 1
            if y_min < 0:
                y_min = 0
            y_max = y+2
            if y_max > len(self.world[0]):
                y_max = y_max - 1

            if direction == utils.direction.EAST:
                x_min = x+1
                x_max = len(self.world)
            else:
                x_min = 0
                x_max = x

            for i in range(y_min, y_max):
                self.world[x_min:x_max][i] = 0

            return
        

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
