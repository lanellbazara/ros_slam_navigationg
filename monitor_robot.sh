#!/bin/bash

echo "Starting ROS Computation Graph..."
rqt_graph &

echo "Starting Data Plotter for Odometry..."
rqt_plot \
 /odom/pose/pose/position/x \
 /odom/pose/pose/position/y \
 /odom/twist/twist/linear/x \
 /odom/twist/twist/linear/y \
 /odom/twist/twist/angular/z &

echo "Tools launched. Please switch to the keyboard control terminal to move the robot."
