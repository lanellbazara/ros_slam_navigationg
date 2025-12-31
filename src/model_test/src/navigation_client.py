#!/usr/bin/env python3

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler
from math import pi

class NavigationClient:
    def __init__(self):
        rospy.init_node('navigation_client')
        
        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        rospy.loginfo("Waiting for move_base action server...")
        self.client.wait_for_server()
        rospy.loginfo("Connected to move_base server")

        # Define waypoints (x, y, yaw)
        # Route: (1.0, 1.75) -> (1.0, -1.75) -> (-1.0, -1.75) -> (-1.0, 1.75) -> (1.0, 1.75)
        self.waypoints = [
            (1.0, -1.75, -pi/2),  # Move Down
            (-1.0, -1.75, pi),    # Move Left
            (-1.0, 1.75, pi/2),   # Move Up
            (1.0, 1.75, 0.0)      # Move Right (Back to start)
        ]

    def send_goal(self, x, y, yaw):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        
        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y
        goal.target_pose.pose.position.z = 0.0
        
        q = quaternion_from_euler(0, 0, yaw)
        goal.target_pose.pose.orientation.x = q[0]
        goal.target_pose.pose.orientation.y = q[1]
        goal.target_pose.pose.orientation.z = q[2]
        goal.target_pose.pose.orientation.w = q[3]

        rospy.loginfo(f"Sending goal: x={x}, y={y}, yaw={yaw}")
        self.client.send_goal(goal)
        
        wait = self.client.wait_for_result()
        if not wait:
            rospy.logerr("Action server not available!")
            return False
        
        return self.client.get_result()

    def run(self):
        # Loop through waypoints
        while not rospy.is_shutdown():
            for i, (x, y, yaw) in enumerate(self.waypoints):
                rospy.loginfo(f"Navigating to Waypoint {i+1}")
                result = self.send_goal(x, y, yaw)
                if result:
                    rospy.loginfo(f"Waypoint {i+1} reached!")
                else:
                    rospy.loginfo(f"Failed to reach Waypoint {i+1}")
            
            rospy.loginfo("Route completed!")
            break # Run only once

if __name__ == '__main__':
    try:
        nav = NavigationClient()
        nav.run()
    except rospy.ROSInterruptException:
        pass
