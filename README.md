Our nodes include:

MainNode.py:

This node subscribes to /fsm_state and sends continuous Twist messages to the robot
via /cmd_vel according to the received state.

LidarProcess.py: 

This node recieves /scan messages from the Lidar on the turtlebot, and publishes
the minimum overall and individual wedge scans (corresponding to the robot's front, 
front left and right, side left and right, and back left and right). It computes the wedge 
scans via python slicing.

StateController.py: 

This node, given a processed scan through /processed_scan, publishes the state corresponding to 
the pattern matched to /fsm_state. This allows the robot to make a sequenced number of events that
should allow it to make it out of the maze.

Run the nodes via the main.launch file after running roscore on your machine + gazebo or a real
Turtlebot: roslaunch maze_solver main.launch

Real Life simulation.txt: Provides link to youtube video that shows turtlebot making
it through maze with our code.
