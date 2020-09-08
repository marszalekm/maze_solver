#!/usr/bin/env python3

import cv2
import numpy as np
import copy
import time
import sys


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
        if ((any(neighbours[i]) > 0) is True
            and maze[y][x] == 0
            and tuple(neighbours[i]) not in closed.keys()) or neighbours[i] == start:
            open.update({tuple(neighbours[i]): []})

    return open


def calculate_distance(dictionary, end):
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


def show_maze_path(path, solution):
    """
    Shows maze and path that was made by algorithm to find exit.
    """
    cv2.namedWindow('solution', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('solution', 1000, 1000)
    maze = cv2.imread(path, 0)
    for point in solution:
        point.reverse()
        maze[point[0]][point[1]] = 175
        cv2.imshow('solution', maze)
        cv2.waitKey(1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def final_path(ppath, maze):
    """
    Generates the shortest way to the exit, knowing the preliminary path.
    """
    tmaze = np.full((len(maze), len(maze[0])), 1)  # temporary maze
    fpath = copy.deepcopy(ppath)  # final path
    moves = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])

    for point in ppath:
        tmaze[point[1]][point[0]] = 0

    flag = 1
    while flag != 0:
        flag = 0
        for point in fpath[1:-1]:
            # loop checks if point is a dead end
            neighbours = (moves + point).tolist()
            deadend = 0
            for i in neighbours:
                if tmaze[i[1]][i[0]] == 1:
                    deadend += 1
            if deadend == 3:
                tmaze[point[1]][point[0]] = 1
                fpath.remove(point)
                flag += 1
            else:
                pass

    return fpath


def find_path(path):
    """
    Actual function used to find end, combination of above functions.
    """
    maze = convert_to_array(path)
    start, end = find_in_and_out(maze)

    open = {}  # points to be evaluated
    closed = {}  # points already evaluated
    ppath = []  # points for creating visualization (preliminary path)
    position = start
    ppath.append(list(position))

    while position != tuple(end):
        open = open_points(position, open, closed, maze, start)
        open = calculate_distance(open, end)
        lowd = lowest_dist(open)
        if lowd not in closed.keys() and position != tuple(end):
            position = lowd
            closed.update({position: open[position]})
            del open[position]
            ppath.append(list(position))

    start = time.time()
    fpath = final_path(ppath, maze)
    print(f'It took {time.time() - start:.5f} seconds to calculate the path.')
    show_maze_path(path, fpath)


find_path(sys.argv[1])
