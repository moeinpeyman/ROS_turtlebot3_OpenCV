# ROS_turtlebot3_OpenCV
Turtlebot3 detects and follows a ball using OpenCV in ROS gazebo 


In this repository, you can find a Python code that receives the camera image of a turtlebot3 waffle and turns the robot to detect and follow the ball, then push it into the yellow goal.For ball control, two fixed arms are also added to the robot.

1) For preparing the system first follow the TurtleBot3 - ROBOTIS e-Manual.
https://emanual.robotis.com/docs/en/platform/turtlebot3/simulation/#gazebo-simulation

2) clone the repository
3) replace turtlebot3_waffle.urdf.xacro
4) launch Turtlebot3
    $ export TURTLEBOT3_MODEL=burger
    $ roslaunch turtlebot3_gazebo turtlebot3_empty_world.launch
5) run the code
    $ python3 ball_goal.py
    
    
 



