# maze_solving_turtlebot

Maze_solving_turtlebot 

MainNode.py:

This node accounts for the main states that the robot could possibly be in whilst 
encountering different obstacles in the maze. 

LidarProcess.py: 

This node recieves a scan by the Lidar on the turtlebot, and publishes the closes 
overall wall based on the wedge scans. It computes the wedge scans via python 
slicing. 

StateController.py: 

This node, given a processed scan via LidarProcess, publishes the state corresponding to 
the pattern matched. This allows the robot to make a sequenced number of events that
should allow it to make it out of the maze 

Real Life simulation.txt: Provides link to youtube video that shows turtlebot making
it through maze with our code.
