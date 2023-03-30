#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist

from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler


import math
PI = math.pi


def get_rotation_first_robot (msg):
    global roll1, pitch1, yaw1, r1x, r1y
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll1, pitch1, yaw1) = euler_from_quaternion (orientation_list)
    r1x = msg.pose.pose.position.x
    r1y = msg.pose.pose.position.y

def PID(Kp, Ki, Kd, MV_bar=0):
    # initialize stored data
    prevError = 0
    timeError = -100
    I = 0

    # initial control
    MV = MV_bar

    while True:
        # yield MV, wait for new t, PV, SP
        t, PV, SP = yield MV

        # PID calculations
        e = SP - PV

        P = Kp*e
        I = I + Ki*e*(t - timeError)
        D = Kd*(e - prevError)/(t - timeError)

        MV = MV_bar + P + I + D

        # update stored data for next iteration
        prevError = e
        timeError = t

def clipPi(angle):
    if angle >= 1.5*PI:
        angle = angle - 2*PI
    elif angle <= -1.5*PI:
        angle = angle + 2*PI
    return angle

def move():
    global roll1,pitch1,yaw1,r1x,r1y


    roll1 = pitch1 = yaw1 = 0.0
    r1x =  r1y = 0



    # Starts a new node
    rospy.init_node('multi_robot_path_planning', anonymous=True)


    first_velocity_publisher = rospy.Publisher('/third_robot/cmd_vel', Twist, queue_size=10)
    first_velocity_sub = rospy.Subscriber ('/third_robot/odom', Odometry, get_rotation_first_robot)


    #second_velocity_publisher = rospy.Publisher('/second_robot/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()
    #vel_msg2 = Twist()

    #Speed and Distance of motion
    speed = 0.5
    distance = 0
    kps = 0.8
    kpz = 2

    robot_1 = (0,0) # Initial Point of robot 1
    robot_2 = (0,1) # Initial Point of robot 2

    points = [(6, 7), (6, 6), (5, 6), (4, 6), (3, 6), (2, 6), (2, 6), (2, 6), (2, 6), (2, 6), (2, 6), (2, 6), (2, 6), (2, 6)]

    controller = PID(0.1, 0, 0)
    controller.send(None)
    #while not rospy.is_shutdown():
    for i in range(1): # Considering only the first robot
        #Obtain the current point and next point
        for point in points:
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
            # if relative_angle > 0:
            #     vel_msg.angular.z = -abs(kpz*angular_speed)
            # else:
            #      = abs(kpz*angular_speed)

            # t0 = rospy.Time.now().to_sec()
            # #current_angle = yaw

            while (abs(yaw1-math.atan2((point[1]-r1y),(point[0]-r1x)))> 0.01) and not rospy.is_shutdown():
                t_pid = rospy.Time.now().to_sec()#New ERROR yaaay
                # print("y",(point[1]-r1y))
                # print("x",(point[0]-r1x))
                # print("yaw",yaw1)
                # print((math.atan2((point[1]-r1y),(point[0]-r1x)) - yaw1))
                vel_msg.angular.z = kpz*(clipPi(math.atan2((point[1]-r1y),(point[0]-r1x))- yaw1))
                # print(vel_msg.angular.z)
                first_velocity_publisher.publish(vel_msg)
                rospy.sleep(0.1)


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

            robot_1 = (point[0],point[1])

if __name__ == '__main__':
    try:
        #Testing our function
        move()
    except rospy.ROSInterruptException: pass