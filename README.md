#Leap Motion UR3 Control
This repository provides a software interface for the real-time teleoperation of a Universal Robots UR3 robotic arm using the Leap Motion Controller. It is developed as a native Windows application utilizing C# and C++ for direct hardware communication.

Project Overview
The project enables a user to command the UR3 robot arm through hand gestures and spatial positioning. By capturing skeletal data from the Leap Motion sensor, the application maps human movement to the robot's coordinate system, providing an intuitive "lead-through" experience without the need for a physical teach pendant or ROS middleware.

Key Features
Real-time Teleoperation: Maps hand position and orientation (X, Y, Z, Pitch, Roll, Yaw) to the UR3 end-effector.

Direct TCP/IP Integration: Low-latency communication with the UR3 controller via standard ethernet protocols.

Dedicated GUI: A C#-based Windows interface for monitoring system status, sensor telemetry, and connection management.

State Machine Management: A structured logic system to handle initialization, tracking modes, and safety transitions.

Gesture-Based Control: Ability to trigger robot actions (such as gripper actuation) based on specific hand gestures.

Visual Feedback: Real-time data visualization of hand tracking and robot state.
