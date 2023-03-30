#!/usr/bin/env python3
import rospy
import time
import actionlib

import multi_robot.msg


from geometry_msgs.msg import Twist

from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler


import math
PI = 3.1415926535897


roll1 = pitch1 = yaw1 = 0.0
r1x =  r1y = 0

def get_rotation_first_robot (msg):
    global roll1, pitch1, yaw1, r1x, r1y
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll1, pitch1, yaw1) = euler_from_quaternion (orientation_list)
    r1x = msg.pose.pose.position.x
    r1y = msg.pose.pose.position.y

def clipPi(angle):
    if angle >= 1.5*PI:
        angle = angle - 2*PI
    elif angle <= -1.5*PI:
        angle = angle + 2*PI
    return angle
    
def move(px,py):
    point = (px,py)
    global roll1,pitch1,yaw1,r1x,r1y




    #second_velocity_publisher = rospy.Publisher('/second_robot/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()
    #vel_msg2 = Twist()

    #Speed and Distance of motion
    speed = 0.4
    distance = 0
    kps = 0.4
    kpz = 2

    #robot_1 = (1,5) # Initial Point of robot 1

    #points = [(1,0),(1,1),(1,2),(2,2),(2,1),(2,0),(1,0)]

    #while not rospy.is_shutdown():
    #Obtain the current point and next point

    vel_msg.linear.x=0
    vel_msg.linear.y=0
    vel_msg.linear.z=0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0

    rospy.loginfo('Current Point is '+ str(r1x)+str(r1y)+' going to '+str(point[0])+str(point[1]))
    #Turn to the right angle
    angular_speed = speed*2*PI/360

    destination_angle = math.atan2(point[1]-r1y,point[0]-r1x)
    relative_angle = destination_angle - yaw1
    print('Turning with angle {}'.format(relative_angle))

    t0 = rospy.get_time()
    while (abs(yaw1-math.atan2((point[1]-r1y),(point[0]-r1x)))> 0.01) and not rospy.is_shutdown():
        vel_msg.angular.z = kpz*(clipPi(math.atan2((point[1]-r1y),(point[0]-r1x))- yaw1))
        first_velocity_publisher.publish(vel_msg)
        rospy.sleep(0.1) 
    t1 = rospy.get_time()

    if (t1-t0) < 0.5:
        time.sleep(1.2)
        
    vel_msg.angular.z = 0
    first_velocity_publisher.publish(vel_msg)

    #Move Forward the right distance
    distance = math.sqrt((r1x-point[0])**2 + (r1y-point[1])**2)
    print('Moving forward with distance {}'.format(distance))
    


    t0 = rospy.Time.now().to_sec()
    current_distance = 0

    #Loop to move the turtle in an specified distance
    while(distance>0.05) and (distance<2) and not rospy.is_shutdown():
        #Publish the velocity
        vel_msg.linear.x = kps*(distance)
        first_velocity_publisher.publish(vel_msg)
        #Takes actual time to velocity calculus
        t1=rospy.Time.now().to_sec()
        #Calculates distancePoseStamped
        #current_distance= speed*(t1-t0)
        distance = math.sqrt((r1x-point[0])**2 + (r1y-point[1])**2)
        #print(distance)
    #After the loop, stops the robot
    vel_msg.linear.x = 0            #Force the robot to stop
    first_velocity_publisher.publish(vel_msg)
    robot_1 = (r1x,r1y)



class gotoAction(object):
    # create messages that are used to publish feedback/result
    _feedback = multi_robot.msg.gotoFeedback()
    _result = multi_robot.msg.gotoResult()

    def __init__(self, name):
        self._action_name = name
        self._as = actionlib.SimpleActionServer(self._action_name, multi_robot.msg.gotoAction, execute_cb=self.execute_cb, auto_start = False)
        self._as.start()
      
    def execute_cb(self, goal):
        # helper variables
        #r = rospy.Rate(1)
        success = True
        
        self._feedback.sequence = []
        self._feedback.sequence.append(int(r1x))
        self._feedback.sequence.append(int(r1y))
        
        # publish info to the console for the user
        goal_list = list(goal.order)
        # start executing the action
        for i in range(1, len(goal_list)):
            # check that preempt has not been requested by the client
            if self._as.is_preempt_requested():
                rospy.loginfo('%s: Preempted' % self._action_name)
                self._as.set_preempted()
                success = False
                break

            move(goal_list[0],goal_list[1])
            self._feedback.sequence.append(self._feedback.sequence[i] + self._feedback.sequence[i-1])
            # publish the feedback
            self._as.publish_feedback(self._feedback)
            # this step is not necessary, the sequence is computed at 1 Hz for demonstration purposes
            
          
        if success:
            self._result.sequence = self._feedback.sequence
            rospy.loginfo('%s: Succeeded' % self._action_name)
            self._as.set_succeeded(self._result)
        
if __name__ == '__main__':
    rospy.init_node('goto4')
    server = gotoAction(rospy.get_name())
    first_velocity_publisher = rospy.Publisher('/fourth_robot/cmd_vel', Twist, queue_size=10)
    first_velocity_sub = rospy.Subscriber ('/fourth_robot/odom', Odometry, get_rotation_first_robot)
    rospy.spin()