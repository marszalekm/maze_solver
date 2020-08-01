# maze_solver

Algorithm finds a way out of the maze. Maze is provided as a black & white image with 1 pixel wall thickness and corridors.
It is based on very basic idea, that doesn't include any sophisticated method or algorithm for finding a shortest paths etc.
In first stage it establishes start and end, to then find a path by checking the Euclidean distance to the exit.
It is done in a loop, every step it calculates and checks the next possible moves, keeping a list of evaluated and to-be-evaluated points, to finally reach an exit.
The second stage is the creation of final path, quite primitive phase where dead ends are removed.

Done mostly for the purpose of self-development and fun.
