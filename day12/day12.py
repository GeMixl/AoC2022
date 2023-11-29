###############################################################
# Advent of Code 2022                                         #
# Day 12 https://adventofcode.com/2021/day/12                 #
# Puzzle input at https://adventofcode.com/2022/day/12/input  #
###############################################################


import numpy as np
from dataclasses import dataclass
import heapq
import networkx as nx

@dataclass
class Network:
    start_idx = None
    goal_idx = None
    counter: int = 0
    nodes = []
    queue = []

    class Node:
        def __init__(self, idx, value, cost, neigh, pos):
            self.idx = idx
            self.cost = cost
            self.value = value
            self.position = pos
            self.neighbor = [i for i in neigh]
            self.predecessor = None
            self.path_cost = 9999
            self.not_visited = True

    def set_up_nodes_for_hiking(self, arr, start, goal):
        height, width = arr.shape
        self.start_idx = start[0]*width + start[1]
        self.goal_idx = goal[0]*width + goal[1]
        for i in range(height):
            for j in range(width):
                n = []
                for x in range(max(0, j - 1), min(width, j + 2)):
                    if (x != j) and ((arr[i][x] - arr[i][j]) <= 1):
                        n.append(i*width+x)
                for y in range(max(0, i - 1), min(height, i + 2)):
                    if (y != i) and ((arr[y][j] - arr[i][j]) <= 1):
                        n.append(y*width+j)
                self.nodes.append(self.Node(i*width+j, arr[i][j], 1, tuple(n), (i, j)))
        self.nodes[self.start_idx].path_cost = 0
        self.queue.append([0, self.start_idx])

    def find_path(self, data, start, goal):

        self.set_up_nodes_for_hiking(data, start, goal)

        while self.queue:
            min_dist, next_node = heapq.heappop(self.queue)
            if self.nodes[next_node].not_visited:
                self.nodes[next_node].not_visited = False
                for n in self.nodes[next_node].neighbor:
                    if (self.nodes[next_node].path_cost + self.nodes[n].cost) < self.nodes[n].path_cost and self.nodes[n].not_visited:
                        self.nodes[n].path_cost = self.nodes[next_node].path_cost + self.nodes[n].cost
                        self.nodes[n].predecessor = next_node
                        heapq.heappush(self.queue, [self.nodes[n].path_cost, n])
        return self.nodes[self.goal_idx].path_cost


def read_input(filename: str) -> []:
    with (open(filename, "r") as fs):
        input = np.array([[ord(px) for px in line.strip()] for line in fs.readlines()])
        start_position = tuple(*np.argwhere(input == ord('S')))
        goal_position = tuple(*np.argwhere(input == ord('E')))
        input[input == ord('S')] = ord('a')
        input[input == ord('E')] = ord('z')
        input = input - 96
    return {'grid': input,
            'start_pos': start_position,
            'goal_pos': goal_position
            }


def solve_part_i(input):
    myNetwork = Network()
    myGrid = input['grid']
    myStartPosition = input['start_pos']
    myGoalPosition = input['goal_pos']
    myPathCost = myNetwork.find_path(myGrid, myStartPosition, myGoalPosition)
    return myPathCost


if __name__ == "__main__":
    filename = "input_day12.txt"
    print("--- Part One ---")
    print(solve_part_i(read_input(filename)))

    print("--- Part Two ---")
    H = np.array([[*x.strip()] for x in open('input_day12.txt')])
    S = tuple(*np.argwhere(H == 'S'))
    H[S] = 'a'
    E = tuple(*np.argwhere(H == 'E'))
    H[E] = 'z'
    G = nx.grid_2d_graph(*H.shape, create_using=nx.DiGraph)
    G.remove_edges_from([(a, b) for a, b in G.edges if ord(H[b]) - ord(H[a]) > 1])
    p = nx.shortest_path_length(G, target=E)
    print(min(p[a] for a in p if H[a] == 'a'))

