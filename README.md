# maze_solver

Algorithm finds a way out of the maze. Maze is provided as a black & white image with 1 pixel wall thickness and corridors.
It is based on a very basic idea, that doesn't include any sophisticated method or algorithm for finding a shortest paths etc.

General workflow:
1. Algortihm establishes start and end. Image is converted to an array. 
2. Loop starts and it checks possible point for the next move.
3. All points are stored in 2 lists: already evaluated (AE) and to-be-evaluated points (TBE). 
4. For each of TBE points Euclidean distance to the exit is calculated and the one with lowest is chosen.
5. When it finally reaches an exit, the list of AE points is again evaluated and applied on the maze structure.
6. Now dead ends are removed, just by checking all of the points from AE list.
7. Final path is shonw on the screen.

Done mostly for the purpose of self-development and fun.                      
It would be interesting to compare performance of this script with some real life algorithm e.g. A*.
