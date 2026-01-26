# 2026 CS 4379K / CS 5342 Introduction to Autonomous Robotics, Robotics and Autonomous Systems

## Programming Assignment: Milestone 3 (V1.0)

**Minhyuk Park and Tsz-Chiu Au**

### Introduction

Welcome to CS 4379K / CS 5342. We have prepared a few milestones before the final project, during which you will use a physical robot to execute a mission we provide. The following milestones will give you an idea of how to interact with ROBOTIS’ Turtlebot3 waffle Pi with a Manipulator Arm using the Robot Operating System 2.

The third milestone is about ROS 2 programming. In this milestone, you will try operating a physical robot arm and write a ROS 2 program to control the OpenManipulator on the Turtlebot using a keyboard. The program should be similar to `turtlebot3_teleop_key`, but it will accept a few more keystrokes to control the robot arm. Your program should provide some basic functions, such as setting the arm to some predefined poses and opening/closing the gripper. In addition, your program should read the current configuration of the arm and the gripper and display the information on the screen. Of course, please feel free to add more functionalities to your program.

To do this, you will deploy our pre-configured Docker container that sets up all the software that is required for the assignment.
Please refer to the following video for an explanation of what a Docker container environment is. 

[https://www.youtube.com/watch?v=Gjnup-PuquQ](https://www.youtube.com/watch?v=Gjnup-PuquQ)

Robot Operating System version is associated with Ubuntu Long-Term Support Versions (e.g. Ubuntu 22.04 with Humble). We are using **ROS 2 Humble in a Docker environment** for Remote-PC. You might find the official tutorial on ROS 2 Humble useful in this course:

[https://docs.ros.org/en/humble/Tutorials.html](https://docs.ros.org/en/humble/Tutorials.html)

For all questions regarding milestone assignments and the robot, **you should contact the Doctoral Instructor Assistant via direct message on Slack**. Please do not contact the Instructor with questions regarding the milestone assignments. This is the URL for Slack for this course. 

<https://spring2026txstrobot.slack.com/>

We use vim (vi) for text editing in a terminal environment. Please refer to the tutorial for Vim if you are not familiar with vim environment for editing documents. 
<https://opensource.com/article/19/3/getting-started-vim>

### Assignment requirement

A hardware video demonstration submission is required for Milestone Assignment 3. 

You need to demonstrate that you have a working setup and can operate the turtlebot in simulation by making videos. This will also demonstrate that you have a working setup for working with a physical turtlebot. Refer to the demo requirement section at the end of the milestone assignment on what to include in the video.

**[SUBMISSION RULES]**

* **Individual Submission:** **Every team member must submit the video link(s) separately to Canvas.** If the video is duplicated within a team, that is acceptable; however, this ensures that only active participants who have access to the team’s recordings can receive credit. 

* **Standardized Hosting:** **To manage file sizes, do not upload raw video files (e.g., MP4) directly to Canvas.** Instead, **upload your videos to YouTube (set as "Unlisted")** and submit the links via a document.

### Video Demo Requirements

Your group will **record** one or more video clips. The estimated total length of the video clips is approximately two and a half minutes. **While you do not need to perform complex editing, please keep the total duration to a few minutes to ensure it remains concise.** One group member should narrate the video, explaining each step as it's performed. At the beginning of the first video clip, please show every group member's face and state the names of all group members.

Your recording setup should be organized to show all relevant windows at once: the terminal(s) used for launching nodes, the Gazebo simulation window, and the RViz visualization window.

You do not need to edit the videos, and uploading raw **footage** will suffice. You can split the demonstration into multiple videos **if necessary to show different parts of the requirement.** 

Rules for robot usage will apply for working with the physical Turtlebot3. Please refer to the inventory list given to you separately and the rules for the Robot room usage.

> **Major Changes**
> * **v 1.0.0:** Initial Release, Added ROS2 control investigation section, overhauled programming guide to help students

---

### Part 1: Operation of Physical Turtlebot 3 Arm

**Please be safe and note the following warnings.**

> * The manipulator arm on the Turtlebot is strong enough to even lift the Turtlebot itself. Do not command extreme movements that might damage motors on the manipulator arm.
> * Powering off the OpenCR board will power off and drop the arm instantly. Make sure you hold the arm before powering off the Turtlebot3.
> * Motor wires on the manipulator arm might interfere with the spinning lidar sensor when commanded to be in a certain position. Take care not to damage the wires on the manipulator arm.
> * Please be aware of pinching your body between the robot joints. When the Turtlebot3 Manipulation bringup launches, the OpenMANIPULATOR-X will move to the initial pose. It is recommended to set the OpenMANIPULATOR-X in a similar pose as shown in the image below to avoid any physical damage during the initial pose.
> 
> 

This manual is based on the following manual for humble.

* **(Original URL)** [https://emanual.robotis.com/docs/en/platform/turtlebot3/manipulation/#simulation](https://emanual.robotis.com/docs/en/platform/turtlebot3/manipulation/#simulation)

**Operating Physical Turtlebot 3 Arm**

[Turtlebot Nvidia Jeston] [Remote PC] Make sure Jeston is connected to the small router we provided (small_blue_wifi), along with the remote PC. You should also sync the time for both the remote PC and the NVIDIA Jetson by going through Ubuntu settings. Refer to the end of the instruction for this procedure.

[Turtlebot Nvidia Jeston] The following command will bring up the actual TurtleBot3 hardware with OpenMANIPULATOR-X on it. Open a terminal from the TurtleBot3 SBC. Bring up the TurtleBot3 Manipulation using the following command.

```bash
ros2 launch turtlebot3_manipulation_bringup hardware.launch.py

```

[Remote PC] Enter the command below to launch MoveIt on RViz. The arm should move when you move the blue ball on RViz and click “plan and execute”.

```bash
ros2 launch turtlebot3_manipulation_moveit_config moveit_core.launch.py

```

[Remote PC] To operate the robot with the keyboard teleoperation node, the RViz must be terminated. Then launch the servo server node and teleoperation nodes on a separate terminal window.

```bash
ros2 launch turtlebot3_manipulation_moveit_config servo.launch.py
ros2 run turtlebot3_manipulation_teleop turtlebot3_manipulation_teleop

```

**Note:** A common reason why physical manipulation of the robot arm fails is that the clock between the NVIDIA Jetson and the Remote PC is not synced. If you suspect this, read the error message on the terminal for bringup to verify.

A simple workaround is to open settings for two machines, go to Date and Time, and set both time zones to CDT (Chicago, United States), and click on the time slider for both machines at the same time so that they are updated (synced) to each other within 1s. The accuracy of time itself does not matter; the timestamps for ROS 2 messages between two machines should be within 1s of each other. Because Jetson does not have a Real-Time Clock battery, you should do this every boot.

---

### Part 2: Programming a Command Line Interface for complete teleoperation of Turtlebot3 with OMX Arm

In part 2 of the assignment, you are going to learn how to program a client teleoperation program in ROS2 to interface with the ROBOTIS Turtlebot 3.

You may find this thread useful in creating command-line interfaces in Python.

[https://python-forum.io/thread-4083.html](https://python-forum.io/thread-4083.html)

You also need to learn how to use ROS 2 to command the turtlebot using your own program. Refer to the Appendix for help regarding this process.

Note that your program is expected to run while `turtlebot3_manipulation_bringup hardware.launch.py` is running on Jetson on the turtlebot.

Your script is expected to run on the Remote PC, but it should not matter if your script runs on turtlebot3’s Jetson or the Remote PC. Again, make sure both machines have synced time within 1s of each other (does not need to be accurate) and are on the same local network.

If you cannot get the clock problem solved, run your code on Jetson as a workaround.

It is highly recommended to debug your code in simulation before running your code on hardware. However, you may not complete the requirement for this assignment on the simulator.

**Example interface of your program**

```text
---------------------------
 Teleoperation Control of TurtleBot3 + OpenManipulatorX
 ---------------------------
 w : increase linear velocity
 x : decrease linear velocity
 a : increase angular velocity
 d : decrease angular velocity
 s : base stop

 g : gripper open
 h : gripper close
           
 0 : Extend arm forward
 9 : Home pose
 8 : Custom pose
           
 q to quit
 ---------------------------
 Present Linear Velocity: 0.000, Angular Velocity: 0.000
 Present Arm Joint Angle J1: 0.000 J2: 0.000 J3: 0.000 J4: 0.000
 Present Base Position X: 0.000 Y: 0.000 Z: 0.000
 ---------------------------

```

---

### Video Demo Requirements (3-4 Minute Demonstration)

Please refer to the video submission requirements in the introduction.

Your submission must include two items: the video file and a single .zip file containing all of your source code.

**Part A: Code Walkthrough**
The goal of this part is to explain the design and structure of your program. With your source code visible on the screen, you will guide us through the key components.

* **High-Level Overview:** Start with a brief architectural explanation. What is the overall structure of your code? (e.g., "We created a single ROS2 node with classes for handling user input, publishing commands, and subscribing to robot state.")
* **Show Key Functions:** Point to and briefly explain the specific parts of your code that are responsible for:
* **Base Movement:** The function or code block that creates and publishes relevant messages to the relevant topic.
* **Arm & Gripper Control:** The code that sends goals to the arm and gripper.
* **State Subscription:** How are you listening to the relevant topics to receive real-time wheel, arm, and gripper positions?
* **Terminal UI:** The code you wrote to create the non-scrolling terminal display that continuously updates values in place.



**Part B: Live Program Demonstration**
In this part, you will run your program and demonstrate all of its features with the physical robot. It is highly recommended to run your program on SSH from a Remote PC.

* **Launch Program:** From a standard terminal, run your program. Your custom, non-scrolling interface should appear on the screen.
* **Live Status Display:** As you perform the following actions, point out that the joint angles and gripper status on your terminal display are updating in real-time. Emphasize that the display updates without scrolling new text up the screen.
* **Mobile Base Control:** Using the controls you implemented, demonstrate driving the robot smoothly forward, backward, turning left, and turning right.
* **Manipulator Arm Control:**
* Demonstrate commanding the arm to move between at least three distinct, predefined positions. You must include a "Home" position and an "Extend Forward" position (as if you were to grab an object directly in front of the robot), plus one more of your own design (e.g., a "Ready" or "Wave" position).
* Show the arm moving smoothly from one predefined position to the next.


* **Gripper Control:** While the arm is in an extended position, demonstrate your program's ability to reliably open and close the gripper on command.

---

### Appendix

#### [Guide] ROS2 Programming Guide

**[Optional] Creating a Package for Coding in ROS2**

Suggested Reading: [Create your own package] [https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html)

While not strictly necessary for ROS2 (i.e., you can get away with `python3 yourscript.py`), you might want to create a ROS2 package to follow ROS2 conventions. Navigate to the src directory of your ROS2 workspace and create a new package. For NUC users, you need to create a new ROS2 workspace. Please refer to the suggested reading and initialize your ROS2 workspace first.

This command creates a new directory named `manipulator_control` with the necessary files and folders.

```bash
ros2 pkg create --build-type ament_python manipulator_control --dependencies rclpy control_msgs open_manipulator_msgs

```

Inside the newly created package, save the code above in a file named `controller_node.py` inside the `manipulator_control/manipulator_control` directory.
Open the `setup.py` file located in the `manipulator_control` directory. You need to add an `entry_points` section to let ROS2 know about your executable script.

```python
entry_points={ 'console_scripts': [ 'controller_node = manipulator_control.controller_node:main', ], },

```

Navigate to the root of your workspace and build your package using colcon

```bash
colcon build --packages-select manipulator_control

```

After the build is complete, source your workspace's setup file to make the new package available in your environment. It is suggested to configure your bashrc with the full path to your workspace so that this is sourced upon every terminal startup.

```bash
source install/setup.bash

```

Once the robot model is loaded in Gazebo, open another terminal, source your workspace again, and run your controller node

```bash
# In a second terminal, source and run your node
cd ~/your_ws
source install/setup.bash
ros2 run manipulator_control controller_node

```

**Open Manipulator X Arm Control Documentation**

Reference: “ROS Robot Programming” Chapter 13 by Robotis
[https://www.robotis.us/ros-robot-programming-book-digital-copy/?srsltid=AfmBOoq5eDXDdPVY6gIEhJ889Goef0EndZsfy17A8Q5FPfRbjAXwc4WW](https://www.robotis.us/ros-robot-programming-book-digital-copy/?srsltid=AfmBOoq5eDXDdPVY6gIEhJ889Goef0EndZsfy17A8Q5FPfRbjAXwc4WW)

Before we begin, we would like to introduce you to the ROS 1 programming book from ROBOTIS and refer to their documentation on the Open-Manipulator (Chapter 13). While this book is outdated with information on ROS 1, not 2, it gives us an idea of how the designers designed the robotic arm on the turtlebot.
The robot arm is a 4-degree-of-freedom (DOF) robot arm, with the end effector or gripper being just a single 1 DOF joint arm.

Recall from milestone assignment 2 that we moved around the arm end effector or directly used joint angles under the joint tab in RViz. Behind the scenes, RViz has been interfacing with the bringup program and Moveit 2 planner to plan and give an intermediate state the robot arm should take in sequence so that the arm does not exceed its physical limits or collide with itself.
A critical concept to go over is inverse kinematics and forward kinematics. These two concepts are used to calculate relevant control commands. Note that the unit for joint angles is in radians and task space control is in m.

In summary, from the documentation, we can deduce that we somehow need to provide either target joint angles or target task space coordinates with pitch, roll, and yaw values to control the arm. Similarly, we should also be able to receive relevant joint information and target task space coordinates through the same pipeline. Recall that in RViz, you can either drag the gripper around in 3D space or command specific joint angles on the Joints tab to command the robot arm movement. This means you have already exploited forward and inverse kinematics to plan and move the robotic arm. Availability of both forward and inverse kinematics is a powerful tool for robot programmers.
To make things simple, our course will focus on control through joint space as illustrated on the forward kinematics diagram.
**[Optional]** While not necessary for the set of assignments we are going to give you, if you are interested in forward kinematics results and utilizing the resulting X Y Z gripper location in your program, create a tf buffer, tf transform listener from ROS tf2 packages and look up the transform between ‘base_link’ and ‘link5’ for the transform between the target frame and source frame.

Figure 13-17 shows the basic structure of ROS1 Moveit. As shown in Figure 13-17, the ‘move_group’ node can exchange commands with the user using ROS 1 actions via JointTrajectoryAction. MoveIt also provides built-in publisher and subscriber, such as Joint States Topic and TF, as well as services that allow users to communicate with the ‘move_group’ node. To support moveit, we use manipulation_bringup to provide relevant information to moveit, which in turn communicates with the turtlebot to move the robotic arm based on its plans. The exact system diagram changed with ROS2, but it allows us to get an idea.
It is suggested to read more about MoveIt, the planning framework behind the arm control.

Suggested reading: [Moveit Tutorial]
[https://moveit.picknik.ai/main/index.html](https://moveit.picknik.ai/main/index.html)

**Turtlebot3_manipulation package bringup**

Before controlling the arm named “Open Manipulator X” AND the turtlebot base with any ROS2 program, you need to run the bringup on the Turtlebot3 Single Board Computer, Nvidia Jetson. Bringup acts as a bridge between your ROS2 program and the OpenCR controller board on Turtlebot3.
Please monitor the bringup terminal for errors or crashes, as they can give you hints on debugging your problem with the open manipulator arm. If you do not get messages such as “You can start planning now” or get intermediate errors while operating the robot arm, please make sure that the issue is resolved. A common problem is clock synchronization between ROS 2 machines, as they need to be within 1s of one another.

**ROS2 Communication Programming**

Largely speaking, there are three interfaces, publisher & subscriber, service & client, and action & action client, that you need to be aware of. Below are links to relevant tutorials. It is highly recommended that you read the tutorials from start to finish to get a comprehensive idea of the ROS2 ecosystem.

* Suggested reading: [Publisher & Subscriber] Getting continuous sensor data or other continuous vehicle command: [https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html)
* Suggested reading: [Action Server & Client] Commands that take time to complete for Arm and Gripper: [https://docs.ros.org/en/humble/Tutorials/Intermediate/Creating-an-Action.html](https://docs.ros.org/en/humble/Tutorials/Intermediate/Creating-an-Action.html) [https://docs.ros.org/en/humble/Tutorials/Intermediate/Writing-an-Action-Server-Client/Py.html](https://docs.ros.org/en/humble/Tutorials/Intermediate/Writing-an-Action-Server-Client/Py.html)
* Suggested reading: [rclpy] ROS Client Library for Python: [https://docs.ros.org/en/iron/p/rclpy/api.html](https://docs.ros.org/en/iron/p/rclpy/api.html)
* Suggested reading: [Service and Client] Short, one-off command for tasks such as parameter updates: [https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Service-And-Client.html](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Service-And-Client.html)
* Suggested reading: [Moveit Python API Tutorial] Note that because their robot arm configuration is different from ours, this tutorial will not directly help you with this assignment. [https://moveit.picknik.ai/main/doc/examples/motion_planning_python_api/motion_planning_python_api_tutorial.html](https://moveit.picknik.ai/main/doc/examples/motion_planning_python_api/motion_planning_python_api_tutorial.html)

**ROS2 Fundamentals**

* **Nodes:** You need to build around a class that inherits from Node. A node is the primary building block of a ROS2 system, an executable process that performs a specific task.
* **[Optional] Building and Sourcing:** If you were to use packages for your ROS2 code, you need to be familiar with the `colcon build` command to compile your package and the `source install/setup.bash` command to make their node's executable available to the ROS2 environment.

**ROS2 Communication Paradigms**

Your code would use three different ways to communicate with the robot’s systems and rclpy to facilitate the communication.

1. **Actions (for the Arm and Gripper):** The arm and gripper movement is a process that takes time. For tasks like this, ROS2 uses actions. You need to understand the Action Client/Server model:
* **Goal:** The client (our node) sends a goal to the server (the robot's controller). In our code, the goal is a trajectory, or a sequence of joint positions over time.
* **Feedback:** The server can provide continuous feedback (e.g., the arm's current position) while it's executing the goal.
* **Result:** Once the task is done, the server sends back a final result (e.g., success or an error code).
* **Pipeline:** The ActionClient for FollowJointTrajectory is created, and the `send_joint_goal` function builds and sends the goal.


2. **Services (for Parameter update):** A parameter update is a quick, one-off command. For this, ROS2 uses services. You need to understand the Service Client/Server model:
* **Request:** The client (our node) sends a request to the server.
* **Response:** The server performs the task and sends back a single response. This is a synchronous-style communication. The client usually waits for the response before continuing.
* **Pipeline:** You need to set up the connection to the relevant parameter service, and your function needs to send the request to update the parameter.


3. **rclpy (ROS Client Library for Python) library:**
* **Node and Client Initialization:** You need to understand how to initialize rclpy, create a node class, and create action and service clients in the `__init__` method.
* **Asynchronous Calls (async and future):** Instead of blocking the whole program, asynchronous functions immediately return a "future" object. For example, `rclpy.spin_until_future_complete(self, future)` pauses the execution of that function to wait for the result to come back. This is essential for preventing nodes from freezing.
* **Message Types:** Every ROS2 communication uses a specific message type. You must understand how to import these (from `control_msgs.action` import `FollowJointTrajectory`) and how to create and populate them with data (e.g., creating `JointTrajectoryPoint` and setting its positions).


4. **Publishers and Subscribers (for Continuous Data Streams):** This is for continuous, one-way data flow. A publisher node sends messages to a specific topic (like a radio channel). Any number of subscriber nodes can listen to that topic to receive the messages. The publisher doesn't know or care who is listening, and the subscribers don't know who is publishing. This creates a flexible, decoupled system.
* **The Callback Function (Event-Driven Programming):** You must understand that they do not call this function directly in their main logic. Instead, the ROS2 framework automatically calls it for them in the background whenever a new message is published to the topic. This is a core principle of event-driven programming. The function's job is to take the incoming message (msg) and do something with it.
* **"Spinning" to Process Callbacks:** A ROS2 node doesn't process incoming data by default; it must be told to do so. "Spinning" is that process. `spin_once()` tells the node: "Check for any new messages or service requests right now, execute their callbacks, and then return control to my script." We use this when we want to manually process incoming data at specific points in our code. `spin()` would tell the node: "Continuously check for messages and execute callbacks forever until the node is shut down." This is used when a node's only job is to react to events. Without a spin or `spin_once` call, the `joint_state_callback` would never run, and the subscriber would be useless.
* **Pipeline:** It's perfect for broadcasting sensor data, robot status, or any information that needs to be continuously available to the rest of the system. The robot's hardware drivers are constantly publishing the current state of all joints to the `/joint_states` topic. It is the perfect place to hook into to get real-time position data.



Finally, you need a grasp of some basic robotic arm concepts that are described above, such as joint space. It is recommended for you to utilize parallel computing concepts, such as utilizing multiple threads and synchronization, but it should not be necessary for the simple code required for this course.

**ROS2 Robot Control and Feedback Interface Investigation**
Reference: ROS2 CLI tools
[https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html)

With the theoretical background dialed in, let us try exposing what interface is available for secondary development ourselves using built in ROS2 CLI tools.

The first interface we are going to investigate is the publisher-subscriber interface. ROS 2 breaks complex systems down into many modular nodes. Topics are a vital element of the ROS graph that act as a bus for nodes to exchange messages through publisher-subscriber interface.

Let us try running a rostopic list while running bringup. This could give us some hints on how to interact with the turtlebot.

[Turtlebot Jetson or Remote PC on same network] Run bringup.

```bash
ros2 launch turtlebot3_manipulation_bringup hardware.launch.py

```

While hardware bringup is running on Jetson on Turtlebot3,

[Turtlebot Jetson or Remote PC on same net] Run the ros2 topic list command on a new terminal

```bash
ros2 topic list -t

```

This should expose available topics in ROS2 and their message type. This command is designed to expose available ROS2 topics and their message type.

It should bring up the following.

```text
/arm_controller/joint_trajectory [trajectory_msgs/msg/JointTrajectory]
/arm_controller/state [control_msgs/msg/JointTrajectoryControllerState]
/cmd_vel [geometry_msgs/msg/Twist]
/dynamic_joint_states [control_msgs/msg/DynamicJointState]
/imu_broadcaster/imu [sensor_msgs/msg/Imu]
/joint_states [sensor_msgs/msg/JointState]
/odom [nav_msgs/msg/Odometry]
/parameter_events [rcl_interfaces/msg/ParameterEvent]
/robot_description [std_msgs/msg/String]
/rosout [rcl_interfaces/msg/Log]
/scan [sensor_msgs/msg/LaserScan]
/tf [tf2_msgs/msg/TFMessage]
/tf_static [tf2_msgs/msg/TFMessage]

```

If you do not get the full list and just get the following, check if your hardware bringup is running properly.

```text
/parameter_events [rcl_interfaces/msg/ParameterEvent]
/rosout [rcl_interfaces/msg/Log]

```

We would like you to pay attention to the following topics and message types. We have added some descriptions to make your life easier.

Commanding wheels
`/cmd_vel` `[geometry_msgs/msg/Twist]`

Getting feedback on estimated positions and velocity in the world
`/odom` `[nav_msgs/msg/Odometry]`

Getting feedback on joints, including wheels
`/joint_states` `[sensor_msgs/msg/JointState]`

Controlling Arm
`/arm_controller/joint_trajectory` `[trajectory_msgs/msg/JointTrajectory]`

What is this ROS2 datatype called messages?

Suggested reading: Data passing in ROS2: Understanding and defining msg in ROS2
[https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html)

Let's do a more in-depth investigation of the topics.

[Turtlebot Jetson or Remote PC on same net] Try ros2 topic echo to get the real-time message status of the topic odom

```bash
ros2 topic echo /odom

```

That should output “echo” of your real-time topic information of topic /odom. This exposes the structure and elements of the messages as well.

```yaml
twist:
  twist:
    linear:
      x: 0.0
      y: 0.0
      z: 0.0
    angular:
      x: 0.0
      y: 0.0
      z: 0.0
  covariance:
  - 0.001
  - 0.0
  - 0.0
…

```

[Turtlebot Jetson or Remote PC on same network] You might find the hz command useful to find the rate at which the data is published.

```bash
ros 2 topic hz /odom

```

It should output the measured rate at which information is being produced.

```text
average rate: 49.833
    min: 0.009s max: 0.026s std dev: 0.00517s window: 51

```

[Turtlebot Jetson or Remote PC on same network] Try ros2 topic info on topic odom.

```bash
ros2 topic info /odom

```

It should output the following information about the topic

```text
Type: nav_msgs/msg/Odometry
Publisher count: 1
Subscription count: 0

```

From this, we can see that the topic `/odom` has type `nav_msgs/msg/Odometry`, with 1 publisher active with no subscriber active.

[Turtlebot Jetson or Remote PC on same network] But how about this?

```bash
ros2 topic info /cmd_vel

```

It should output the following information about the topic

```text
Type: geometry_msgs/msg/Twist
Publisher count: 0
Subscription count: 1

```

This topic has no publisher but has an active subscriber.

From our short investigation, we can see that bringup from manufacturer Robotis designed topics `/odom` to be a producer of information, and `/cmv_vel` to be a consumer of the information. You can continue the investigation to get a better picture of the overall turtlebot architecture.

[Turtlebot Jetson or Remote PC on the same network] Lastly, it is highly recommended for you to try out the investigation on other interfaces called services and actions.

```bash
ros2 action list
ros2 action info

ros2 service list
ros2 service type

```

We would leave you with relevant actions you need to pay attention to.

Actions

`/arm_controller/follow_joint_trajectory`
`/gripper_controller/gripper_cmd`

Now, let's move on to how to exploit this information for communication programming.

**FAQ**

**I am getting timeouts on the bringup during arm operations.**
Please use sleep appropriately to give time for your code to execute in the physical world. Also, try to execute only “valid” (i.e., verified to be executable through other means, such as sim and RViz) pose targets. You can also get timeouts if you are trying to give a pose target that is too close to the current position. Try giving distant targets.

**Can I develop my teleoperation program with my own ROS 2 simulator from assignment 1 and bring it over to hardware?**
Yes.

**Can I demo my code on the simulator?**
No.

**Is it necessary for me to create a ROS2 package?**
No. Executing a single Python script is sufficient.

**[Guide] Hints for programming Turtlebot3 Open Manipulator X**

**Hints for Python Imports**

```python
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
# Google message names for message definitions
from geometry_msgs.msg import Twist
from control_msgs.action import FollowJointTrajectory, GripperCommand
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from sensor_msgs.msg import JointState
from builtin_interfaces.msg import Duration

```

**Pseudocode for simple robot procedures**

Note: Some parts of the solution code, such as constructors, are not included here.

```text
// --- Declaration of Variables ---
  // For Base Movement
  DECLARE base_publisher // To send velocity commands
  DECLARE current_linear_velocity = 0.0
  DECLARE current_angular_velocity = 0.0
  DECLARE base_speed_multiplier = 0.05
  DECLARE base_turn_multiplier = 0.186
  DECLARE current_position     // Variable to store the latest position (x, y, z).
  DECLARE current_orientation  // Variable to store the latest orientation (as a quaternion: x,   y, z, w).

  // For Arm and Gripper
  DECLARE arm_action_client     // To send arm trajectory goals
  DECLARE gripper_action_client // To send gripper command goals
  DECLARE joint_state_subscriber // To receive current joint positions
  DECLARE odom_subscriber       // To receive current XYZ positions
  DECLARE arm_joint_names = ["joint1", "joint2", "joint3", "joint4"]
  DECLARE current_arm_angles = [0.0, 0.0, 0.0, 0.0]
  DECLARE arm_angle_step_size = 5 degrees in radians

  // Sends a movement command to the robot's base.
  PROCEDURE PublishBaseVelocity()
  BEGIN
    CREATE a new 'Twist' message.
    SET message.linear.x = current_linear_velocity * base_speed_multiplier.
    SET message.angular.z = current_angular_velocity * base_turn_multiplier.
    PUBLISH the message using base_publisher.
  END PROCEDURE

  // Sends a goal to the arm's action server.
  PROCEDURE SendArmGoal(target_positions, duration)
  BEGIN
    CREATE a new 'FollowJointTrajectory' goal message.
    SET goal.trajectory.joint_names = our arm_joint_names list.
    CREATE a single trajectory point.
    SET point.positions = target_positions.
    SET point.time_from_start = duration.
    ADD the point to the goal's trajectory.
    SEND the goal message asynchronously using the arm_action_client.
  END PROCEDURE

  // Sends a goal to the gripper's action server.
  PROCEDURE SendGripperGoal(target_position)
  BEGIN
    CREATE a new 'GripperCommand' goal message.
    SET goal.command.position = target_position.
    SET goal.command.max_effort = 1.0. // A reasonable default force
    SEND the goal message asynchronously using the gripper_action_client.
  END PROCEDURE

// Callback function for the joint state subscriber.
  PROCEDURE JointStateCallback(message)
  BEGIN
    // Update our record of the arm's current position
    FOR each joint_name in our arm_joint_names list:
      FIND the position of that joint_name in the incoming message.
      UPDATE the corresponding angle in the current_arm_angles list.
    END FOR
  END PROCEDURE

// Callback function for the odom subscriber.
PROCEDURE OdomCallback(incoming_message)
  BEGIN
    SET current_position = incoming_message.pose.pose.position
    SET current_orientation = incoming_message.pose.pose.orientation
  END PROCEDURE

```

You would need to find out how you can get the actual code for the programming requirement. It is highly suggested to use and respect async commands to synchronize your code while waiting for certain actions to finish. If you have further questions, please ask via email.
