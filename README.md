# Maze solver

Algorithm finds a way out of the maze. Maze is provided as a black & white image with 1 pixel wall thickness and corridors.<br/>
It is based on an idea used in A* algorithm, where distance to the exit is calculated for each cell.

General workflow:
* Algorithm establishes start and end. Image is converted to an array. 
* Loop starts and it checks possible point for the next move.
* All points are stored in 2 lists: already evaluated (AE) and to-be-evaluated points (TBE). 
* For each of TBE points Euclidean distance to the exit is calculated and the one with lowest is chosen.
* When it finally reaches an exit, the list of AE points is again evaluated and applied on the maze structure.
* Now dead ends are removed, just by checking all of the points from AE list.
* Final path is shown on the screen.

In order to run the algorithm define path to particular maze as an argument i.e. <br/>``` ./maze_solver.py mazes/maze1.png```

*Done mostly for the purpose of self-development and fun.*
