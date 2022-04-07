## <center>Thymio Implementations of Activities</center>

## <center>Elements of Robotics</center>

### <center>Moti Ben-Ari and Francesco Mondada</center>

###### <center>Copyright 2017, 2022 by Moti Ben-Ari and Francesco Mondada</center>

This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

The programs in this archive are implementations of most of the activities in the book "Elements of Robotics", Springer, 2018. The source files are named with the numbers and titles of the activities with extension aesl for programs in the Aseba language and py for programs in the Python language. There are four directories:

- `thymio-aseba`: programs in Aseba for the Thymio robot

- `thymio-python`: programs in Python for the Thymio robot

- `computer-python`: programs in Python for a regular computer

- `print`: LaTeX / TikZ source and pdf for printing surfaces

The programs in Python for a computer are provided when an algorithm is difficult or impossible to implement on the Thymio, as well as for algorithms that can be implemented on the Thymio but are easier to investigate in a simulation.

The Aseba programs were developed in the Aseba Studio Environment, while the Python programs were developed using the Thonny Environment because there is a plugin for connecting it to the Thymio computer.

Values of the internal variables of the Thymio can be read directly in the Aseba Studio environment. On the left of the window is a pane labeled "Variables". Click the box "auto" and the values of the values in the pane will be updated continuously. Of particular importance are the values of the horizontal proximity sensors: `prox.horizontal[i]`, where i=0,1,2,3,4 for the front sensors and i=5,6 for the rear sensors. The values of the ground proximity sensors are in the variables
`prox.ground.delta`.

In Python the values can be read using the tdmclient.tools.gui tool. You will be primarily interested in the proximity sensors and program variables.py shows code that can be included in your program to display the values.

Notation

- no program: This activity does not require an implemention on the robot.

- Python: This activity is implemented as a Python program on a computer.

- also in Python: This activity is implemented both on a robot and on a
  computer.

- variables: This activity can be carried out using only the displayed
  values of the Thymio variables.

- or variables: There is a program for this activity, but it can also be
  carried out using the displayed variables.

- offline computations in Python: The Thymio collects data that is analyzed by a Python program on the computer.

##### List of activities

2.1:  Range of a distance sensor (or variables)<br>
2.2:  Thresholds (program for 2.1 or variables)<br>
2.3:  Reflectivity (program for 2.1 or variables)<br>
2.4:  Triangulation (no program)<br>
2.5:  Measuring the attitude using accelerometers (or variables)<br>
         ...-music<br>
         ...-incline<br>
2.6:  Precision and resolution (variables)<br>
2.7:  Accuracy (variables)<br>
2.8:  Linearity (variables)<br><br>

3.1:  Timid<br>
3.2:  Indecisive<br>
3.3:  Dogged<br>
3.4:  Dogged stop<br>
3.5:  Attractive and repulsive<br>
3.6:  Paranoid<br>
3.7:  Paranoid right left<br>
3.8:  Insecure<br>
3.9:  Driven<br>
3.10: Line following with two sensors<br>
3.11: Different line configurations (program for 3.10)<br>
3.12: Regaining the line after losing it (program for 3.10)<br>
3.13: Sensor configuration (no program)<br>

 For the following activities use file line-gradient{.tex, .pdf} in the print directory<br>

3.14: Line following with one sensor<br>
3.15: Line following with proportional correction<br>
3.16: Line following without a gradient (program for 3.14)<br>
3.17: Line following in practice (no program)<br>
3.18  Braitenberg vehicles<br>
        ...-coward<br>
        ...-aggressive<br>
        ...-love<br>
        ...-explorer<br><br>

4.1:  Consistent<br>
4.2:  Persistent<br>
4.3:  Paranoid alternates direction<br>
4.4:  Search and approach<br>
        ...-nondeterministic<br><br>

5.1:  Velocity over a fixed distance<br>
5.2:  Change of velocity (program for 5.1)<br>
5.3:  Acceleration<br>
5.4:  Computing distance when accelerating (no program)<br>
5.5:  Measuring motion at constant acceleration<br>
5.6:  Distance from speed and time<br>
5.7:  Odometry in two dimensions<br>
5.8:  Odometry errors<br>
5.10: Correcting odometry errors<br>
5.9:  Combined effect of odometry errors (omitted)<br>
5.11: Wheel encoding (program for 5.1)<br>
5.12: A robot that can only rotate (no program)<br>
5.13: Robotic crane<br>
5.14: Robotic crane alternatives (also Python)<br>
5.15: Holonomic and non-holonomic motion (no program)<br><br>

6.1:  Setting the control period (no program)<br>
6.2:  On-off controller<br>
6.3:  Proportional controller<br>
6.4:  PI controller<br>
6.5:  PID controller<br>
6.6:  Ziegler-Nichols tuning (program for 6.5)<br><br>

7.1:  Conditional expressions for wall following<br>
7.2:  Simple wall following<br>
7.3:  Wall following with direction (program for 7.4)<br>
7.4:  Pledge algorithm (also in Python)<br>
7.5:  Line following while reading a code<br>
7.6:  Circular line following while reading a code<br>
         (no program for clocks)<br>
7.7:  Locating the nest<br>

7.8:  Sensing areas of high density (program for 3.14)<br><br>

8.1:  Play the landmark game (no program)<br>
8.2:  Determining position from an angle and a distance<br>
8.3:  Determining position by triangulation<br>
8.4:  Localization with uncertainty in the sensors (also in Python)<br>
8.5:  Localization with uncertainty in the motion<br><br>

9.1:  Probabilistic map of obstacles (program for 8.4)<br>
9.2:  Frontier algorithm (Python)<br>
9.3:  Robotic lawnmower<br>
        ... -landmark<br>
9.4:  Localize the robot from the computed perceptions (Python)<br>
9.5:  Localize the robot from the measured perceptions<br><br>

10.1:  Dijkstra’s algorithm on a grid map (Python)<br>
10.2:  Dijkstra’s algorithm for continuous maps (no program)<br>
10.3:  The A* algorithm (Python)<br>
10.4:  Combining path planning and obstacle avoidance<br><br>

11.1:  Fuzzy logic<br><br>

For the following activities use file image-patterns{.tex, .pdf} in the print directory<br>

12.1: Image enhancement: smoothing (also in Python)<br>
12.2: Image enhancement: histogram manipulation (program for 12.1) (also in Python)<br>
12.3: Detecting an edge (also in Python)<br>
12.4: Detecting a corner (also in Python)<br>
12.5: Detecting a blob (also in Python)<br>
12.6: Recognizing a door<br><br>

13.1:  Artificial neuron for logic gates<br>
       ... not<br>
       ... or-and<br>
13.2:  Analog artificial neuron<br>
       ... one input<br>
       ... two inputs<br><br>
13.3:  ANN for obstacle avoidance: design (no program)<br>
13.4:  ANN for obstacle avoidance: implementation<br>
13.5:  ANN for object attraction<br>
13.6:  Multilayer ANN (also in Python)<br>
13.7   Multilayer ANN for obstacle avoidance<br>
13.8:  ANN with memory<br>
13.9:  ANN for spatial processing (also in Python)<br>
13.10: Hebbian learning for obstacle avoidance<br><br>

For the following activities use file gray-areas{.tex, .pdf} in the print directory<br>

14.1:  Robotic chameleon (offline computations in Python)<br>
14.2:  Robotic chameleon with LDA (program for 14.1, (offline computations in Python)<br>
14.3:  Obstacle avoidance with two sensors (offline computations in Python)<br>
14.4:  Following an object (program for 14.3)<br>
14.5:  Learning by a perceptron (offline computations in Python)<br><br>

15.1: BeeClust algorithm (no program)<br>
15.2: Pulling force by several robots (no program)<br>
15.3: Total force (no program)<br>
15.4: Occlusion-based pushing (no program)<br><br>

16.1:  Forward kinematics<br>
16.2:  Inverse kinematics (program for 16.1, offline computations in Python)<br>
16.3:  Rotation matrices (no program)<br>
16.4:  Homogeneous transforms (no program)<br>
16.5:  Multiple Euler angles (no program)<br>
16.6:  Distinct Euler angles (no program)<br>




