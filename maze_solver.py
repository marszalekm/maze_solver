#!/usr/bin/env python3

import cv2
import numpy as np
from matplotlib import pyplot as plt

class maze_solver:

    def __init__(self, path_to_maze):
        self.path_to_maze = path_to_maze

    def convert_to_array(self):

        initial_maze = cv2.imread(self.path_to_maze, 0)
        maze_reverted = cv2.bitwise_not(initial_maze)
        self.maze = maze_reverted / 255.0

        return self.maze

    def find_in_and_out(self):

        nr_of_lines = len(self.maze)
        self.coords = []

        for y in range(nr_of_lines):
            if y == 0 or y == nr_of_lines - 1:
                try:
                    x = list(self.maze[y]).index(0)
                    coord = [int(x), int(y)]
                    self.coords.append(coord)
                except:
                    pass
            else:
                if self.maze[y][0] == 0:
                    x = self.maze[y][0]
                    coord = [int(x), int(y)]
                    self.coords.append(coord)
                elif self.maze[y][-1] == 0:
                    x = len(self.maze) - 1
                    coord = [int(x), int(y)]
                    self.coords.append(coord)
                else:
                    pass

        self.start = self.coords[0]
        self.end = self.coords[-1]

    def open_points(self, position, open, closed):

        moves = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
        neighbours = (moves + position).tolist()

        for i in range(len(neighbours)):
            x = int(neighbours[i][0])
            y = int(neighbours[i][1])
            if ((any(neighbours[i]) > 0) == True and self.maze[y][x] == 0 and tuple(neighbours[i]) not in closed.keys()) or neighbours[i] == self.start:
                open.update({tuple(neighbours[i]) : []})

    def find_nodes(self, graph):

        moves = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
        nodes = []
        distances = {}

        for point in graph:
            neighbours = (moves + point).tolist()
            step = 0
            for n in neighbours:
                if n in graph:
                    step += 1
            if step > 2:
                nodes.append(point)

        return nodes

    @staticmethod
    def calculate_distance(dictionary, start, end):

        for point, dist in dictionary.items():
            dist = np.linalg.norm(np.asarray(end) - np.asarray(point))
            dictionary.update({tuple(point): dist})

    @staticmethod
    def lowest_dist(dictionary):

        return min(dictionary.keys(), key=(lambda point: dictionary[point]))

    def corridor_points(self):
        n_0 = 0
        for x in self.maze:
            n_0 = list(x).count(0) + n_0

        return n_0

    @staticmethod
    def show_graph(graph, maze_length, open):

        fig, ax = plt.subplots()
        plt.subplots_adjust(left=0.08, top=0.92, bottom=0.08, right=0.75, wspace=0.075, hspace=0.075)
        plt.axis([0, maze_length, 0, maze_length])
        ax.xaxis.tick_top()
        plt.gca().invert_yaxis()
        ax.spines['left'].set_position(('axes', 0))
        ax.spines['bottom'].set_position(('axes', 0))
        for point in graph:
            #print("Position: ", point)
            point = np.array(point)
            x, y = point.T
            plt.scatter(x, y, c='k', marker='s', s=45)
            plt.pause(0.0001)
        plt.show()

    @staticmethod
    def possible_routes(graph, input_maze):

        updated_maze = np.full((len(input_maze), len(input_maze[0])), 1)

        for point in graph:
            updated_maze[point[1]][point[0]] = 0

        return updated_maze

    def find_path(self):

        self.convert_to_array()
        self.find_in_and_out()

        open = {}  # points to be evaluated
        closed = {}  # points already evaluated
        graph = [] # points for creating visualization
        position = self.start
        graph.append(list(position))

        while position != tuple(self.end):
            self.open_points(position, open, closed)
            self.calculate_distance(open, self.start, self.end)
            lowd = self.lowest_dist(open)
            if lowd not in closed.keys() and position != tuple(self.end):
                position = lowd
                closed.update({position : open[position]})
                del open[position]
                graph.append(list(position))

        n_0 = self.corridor_points()
        percentage = round((len(graph)/n_0 * 100), 2)
        print("Evaluated points:", len(graph))
        print("Points possible to visit:", n_0)
        print("Visited {}% of all points.".format(str(percentage)))

        updated_maze = self.possible_routes(graph, self.maze)
        nodes = self.find_nodes(graph)
        print("Nodes to be evaluated:", nodes)
        self.show_graph(graph, len(self.maze), closed)

path = 'mazes/maze1.png'

solve = maze_solver(path)
solve.find_path()