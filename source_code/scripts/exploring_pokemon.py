#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import os
import roslib
import rospy  
import actionlib  
from actionlib_msgs.msg import *  
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist  
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal  
from nav_msgs.msg import Odometry
from random import sample  
from math import pow, sqrt  

class NavTest():  
    def __init__(self):  
        rospy.init_node('exploring_random', anonymous=True)  
        rospy.on_shutdown(self.shutdown)  

        # 在每个目标位置暂停的时间 (单位：s)
        self.rest_time = rospy.get_param("~rest_time", 2)  

        # 是否仿真？  
        self.fake_test = rospy.get_param("~fake_test", True)  

        # 到达目标的状态  
        goal_states = ['PENDING', 'ACTIVE', 'PREEMPTED',   
                       'SUCCEEDED', 'ABORTED', 'REJECTED',  
                       'PREEMPTING', 'RECALLING', 'RECALLED',  
                       'LOST']  
 
        # 设置目标点的位置  
        # 在rviz中点击 2D Nav Goal 按键，然后单击地图中一点  
        # 在终端中就会看到该点的坐标信息  
        locations = [[],[],[]]  

        locations[0].append( Pose(Point(0.000,-1.25, 0.000),  Quaternion(0.0, 0.0, 0.7273606136495407, 0.6862554463983244)) )
        locations[0].append( Pose(Point(-1.8,-0.2, 0.000),  Quaternion(0.0, 0.0, 0.9999996829318346, 0.0007963267107332633)) )
        locations[0].append( Pose(Point(-3.2, 0.1, 0.000),  Quaternion(0.0, 0.0, -0.706825181105366, 0.7073882691671998))  )
        locations[0].append( Pose(Point(-4.5, -1.6, 0.000),  Quaternion(0.0, 0.0, 0.0, 1.0)) )
        locations[0].append( Pose(Point(-4.5, -2.5, 0.000),  Quaternion(0.0, 0.0, 0.0, 1.0))  )
        locations[0].append( Pose(Point(-4.5, 2.85, 0.000),  Quaternion(0.0, 0.0, 0.0, 1.0))  )
        locations[0].append( Pose(Point(-4.25, 2.8, 0.000),  Quaternion(0.0, 0.0, 0.706825181105366, 0.7073882691671998))  )

        locations[1].append( Pose(Point(-2.2, 2.1, 0.000),  Quaternion(0.0, 0.0, -0.706825181105366, 0.7073882691671998)) )
        locations[1].append( Pose(Point(-0.6, 2.1, 0.000),  Quaternion(0.0, 0.0, -0.706825181105366, 0.7073882691671998)) )
        locations[1].append( Pose(Point(-0.9, 2.85, 0.000),  Quaternion(0.0, 0.0, 0.9999996829318346, 0.0007963267107332633)) )
        locations[1].append( Pose(Point(-0.9, 3.7, 0.000),  Quaternion(0.0, 0.0, 0.9999996829318346, 0.0007963267107332633)) )
        locations[1].append( Pose(Point(-0.9, 5.1, 0.000),  Quaternion(0.0, 0.0, 0.9999996829318346, 0.0007963267107332633)) )
        locations[1].append( Pose(Point(3.78, 4.9, 0.000),  Quaternion(0.0, 0.0, 0.706825181105366, 0.7073882691671998)) )
        locations[1].append( Pose(Point(4.0, 4.2, 0.000),  Quaternion(0.0, 0.0, -0.706825181105366, 0.7073882691671998)) )
        locations[1].append( Pose(Point(3.5, 4.2, 0.000),  Quaternion(0.0, 0.0, 0.9999996829318346, 0.0007963267107332633)) )

        locations[2].append( Pose(Point(2.25, 1.9, 0.000),  Quaternion(0.0, 0.0, 0.9999996829318346, 0.0007963267107332633)) )
        locations[2].append( Pose(Point(2.25, -0.2, 0.000),  Quaternion(0.0, 0.0, 0.9999996829318346, 0.0007963267107332633)) )
        locations[2].append( Pose(Point(2.25, -1.5, 0.000),  Quaternion(0.0, 0.0, 0.9999996829318346, 0.0007963267107332633)) )
        locations[2].append( Pose(Point(3.3, -1.2, 0.000),  Quaternion(0.0, 0.0, 0.9999996829318346, 0.0007963267107332633)) )
        locations[2].append( Pose(Point(0.0, -3.0, 0.000),  Quaternion(0.0, 0.0, -0.706825181105366, 0.7073882691671998))  )
        locations[2].append( Pose(Point(-1.2, -2.7, 0.000),  Quaternion( 0.0, 0.0, 0.706825181105366, 0.7073882691671998)) )
        locations[2].append( Pose(Point(-1.8, -2.6, 0.000),  Quaternion(0.0, 0.0, 0.9999996829318346, 0.0007963267107332633)) )
        locations[2].append( Pose(Point(-2.9, -2.7, 0.000),  Quaternion(0.0, 0.0, 0.9999996829318346, 0.0007963267107332633)) )


        # 发布控制机器人的消息
        self.cmd_vel_pub = list()
        self.cmd_vel_pub.append(rospy.Publisher('tb3_0/cmd_vel', Twist, queue_size=5)) 
        self.cmd_vel_pub.append(rospy.Publisher('tb3_1/cmd_vel', Twist, queue_size=5)) 
        self.cmd_vel_pub.append(rospy.Publisher('tb3_2/cmd_vel', Twist, queue_size=5)) 

        # 订阅move_base服务器的消息 
        self.move_base = list()
        self.move_base.append(actionlib.SimpleActionClient("tb3_0/move_base", MoveBaseAction))
        self.move_base.append(actionlib.SimpleActionClient("tb3_1/move_base", MoveBaseAction))
        self.move_base.append(actionlib.SimpleActionClient("tb3_2/move_base", MoveBaseAction))

        rospy.loginfo("Waiting for move_base action server...") 
         
        n_robot = 3
        # 60s等待时间限制 
        for i in range(n_robot):
            self.move_base[i].wait_for_server(rospy.Duration(60))  
            rospy.loginfo("Connected to move base server tb3_%d", i)  
  
        

        # 保存成功率、运行时间、和距离的变量  
        n_locations = len(locations) 
        # n_goal =0 
        # n_successes = 0  
        i = n_locations  
        #start_time = rospy.Time.now()  
        # running_time = 0  
        location = ""  
        # last_location = ""    
        
        count = 0

        rospy.loginfo("Starting navigation test")  
        sequence = ['1','2','3','4','5','6'] # sample(locations, n_locations)
        count=[0,0,0]  
        # 开始主循环，随机导航  
        while not rospy.is_shutdown():  

             
            for i in range(n_robot):
                
                state = self.move_base[i].get_state()  
                if state == GoalStatus.SUCCEEDED:
                    if count[i] == len(locations[i]):
                        continue
                    os.system('rosrun pokemon_go pokemon_catching%s'%(str(i)))
                    rospy.sleep(1)
                # print(state)
                if state != GoalStatus.ACTIVE :
                    # 设定下一个目标点  
                    self.goal = MoveBaseGoal()  
                    self.goal.target_pose.pose = locations[i][count[i]]  
                    self.goal.target_pose.header.frame_id = 'map'  
                    self.goal.target_pose.header.stamp = rospy.Time.now()  
                    # 存储上一次的位置，计算距离  
                    # last_location = location  

                     # 计数器加1  
                    count[i] += 1  
                    # n_goals += 1  
                    # 让用户知道下一个位置  
                    rospy.loginfo("tb3_"+str(i)+" Going to: " + str(count[i]))  
                     
                    # 向下一个位置进发  
                    self.move_base[i].send_goal(self.goal)  
                    rospy.sleep(1)
                
            
            

            rospy.sleep(self.rest_time)  

#    def update_initial_pose(self, initial_pose):  
#       self.initial_pose = initial_pose  

    def shutdown(self):  
        rospy.loginfo("Stopping the robot...")
        for i in range(3):
            self.move_base[i].cancel_goal()
            rospy.sleep(2)  
            self.cmd_vel_pub[i].publish(Twist())
            rospy.sleep(1)  

def trunc(f, n):  
    slen = len('%.*f' % (n, f))  

    return float(str(f)[:slen])  

if __name__ == '__main__':  
    try:  
        NavTest()  
        rospy.spin()  

    except rospy.ROSInterruptException:  
        rospy.loginfo("Exploring SLAM finished.")
