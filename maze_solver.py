#!/usr/bin/env python3

import cv2
import numpy as np
from matplotlib import pyplot as plt

def convert_to_array(path_to_maze):
    """
    Converts image of maze (wall thickness 1 pixel) to array.
    """
    initial_maze = cv2.imread(path_to_maze, 0)
    maze_reverted = cv2.bitwise_not(initial_maze)
    maze = maze_reverted / 255.0
    return maze

def find_in_and_out(maze):
    """
    Finds start and exit of the maze.
    """
    nr_of_lines = len(maze)
    coords = []

    for y in range(nr_of_lines):
        if y == 0 or y == nr_of_lines - 1:
            try:
                x = list(maze[y]).index(0)
                coord = [int(x), int(y)]
                coords.append(coord)
            except:
                pass
        else:
            if maze[y][0] == 0:
                x = maze[y][0]
                coord = [int(x), int(y)]
                coords.append(coord)
            elif maze[y][-1] == 0:
                x = len(maze) - 1
                coord = [int(x), int(y)]
                coords.append(coord)
            else:
                pass

    start = coords[0]
    end = coords[-1]

    return start, end

def open_points(position, open, closed, maze, start):
    """
    Updates possible and potential points to visit.
    """
    moves = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
    neighbours = (moves + position).tolist()

    for i in range(len(neighbours)):
        x = int(neighbours[i][0])
        y = int(neighbours[i][1])
        if ((any(neighbours[i]) > 0) == True and maze[y][x] == 0 and tuple(neighbours[i]) not in closed.keys()) or neighbours[i] == start:
            open.update({tuple(neighbours[i]) : []})

    return open

def find_nodes(graph):
    """
    Finds nodes of paths, i.e. dead ends and crossings of path.
    """
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
        elif step == 1:
            nodes.append(point)
        else:
            pass

    return nodes

def calculate_distance(dictionary, start, end):
    """
    Calculates and updates distances to end of points in dictionary (open points).
    """
    for point, dist in dictionary.items():
        dist = np.linalg.norm(np.asarray(end) - np.asarray(point))
        dictionary.update({tuple(point): dist})

    return dictionary

def lowest_dist(dictionary):
    """
    Chooses point with lowest distance to end.
    """
    return min(dictionary.keys(), key=(lambda point: dictionary[point]))

def corridor_points(maze):
    """
    Maximum number of points possible to visit (not walls).
    Just to estimate in what extent the maze was evaluated to find exit.
    """
    n_0 = 0
    for x in maze:
        n_0 = list(x).count(0) + n_0

    return n_0

def show_maze_path(path, solution):
    """
    Shows maze and path that was made by algorithm to find exit. CV2 version.
    """

    cv2.namedWindow('solution', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('solution', 500, 500)
    maze = cv2.imread(path, 0)
    for point in solution:
        point.reverse()
        maze[point[0]][point[1]] = 175
        cv2.imshow('solution', maze)
        cv2.waitKey(25)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def show_graph(graph, maze_length):
    """
    Shows graph and path that was made by algorithm to find exit. Matplotlib version.
    """

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

def possible_routes(graph, input_maze):
    """
    All points evaluated by algorithm, with proper path.
    """
    updated_maze = np.full((len(input_maze), len(input_maze[0])), 1)

    for point in graph:
        updated_maze[point[1]][point[0]] = 0

    return updated_maze

def final_path(nodes, graph):



def find_path(path):
    """
    Actual function used to find end, combination of above functions.
    """
    maze = convert_to_array(path)
    start, end = find_in_and_out(maze)

    open = {}  # points to be evaluated
    closed = {}  # points already evaluated
    graph = [] # points for creating visualization
    position = start
    graph.append(list(position))

    while position != tuple(end):
        open = open_points(position, open, closed, maze, start)
        open = calculate_distance(open, start, end)
        lowd = lowest_dist(open)
        if lowd not in closed.keys() and position != tuple(end):
            position = lowd
            closed.update({position : open[position]})
            del open[position]
            graph.append(list(position))

    n_0 = corridor_points(maze)
    percentage = round((len(graph)/n_0 * 100), 2)
    print("Evaluated points:", len(graph))
    print("Points possible to visit:", n_0)
    print("Visited {}% of all points.".format(str(percentage)))
    updated_maze = possible_routes(graph, maze)
    nodes = find_nodes(graph)
    print("Nodes to be evaluated:", nodes)
    show_maze_path(path, graph)
    #show_graph(graph, len(maze))

path = 'mazes/maze1.png'
find_path(path)