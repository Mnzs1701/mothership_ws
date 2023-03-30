#! /usr/bin/env python3

import enum

from numpy import sometrue
import rospy

import random
from elasticCollision import multiRobot
import sys

import time

import actionlib                # Brings in the SimpleActionClient
import multi_robot.msg          # Brings in the messages used by the goto action, including the



def goto_client(finalPath):
    # Creates the SimpleActionClient, passing the type of the action
    # (gotoAction) to the constructor.
    # points1 = [(3,10),(3,9),(3,8),(3,7),(3,6),(4,6),(4,5)]
    # points2 = [(2,10),(2,9),(2,8),(3,8),(3,7),(3,6),(3,5)]
    # points3 = [(3,5),(3,6),(3,7),(2,7),(2,8),(2,9),(3,9)]
    # points4 = [(2,5),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6)]

    points1 = finalPath[0]
    points2 = finalPath[1]
    print(points1[0])
    # points3 = finalPath[2]
    # points4 = finalPath[3]



    client1 = actionlib.SimpleActionClient('goto1', multi_robot.msg.gotoAction)
    client2 = actionlib.SimpleActionClient('goto2', multi_robot.msg.gotoAction)
    # client3 = actionlib.SimpleActionClient('goto3', multi_robot.msg.gotoAction)
    # client4 = actionlib.SimpleActionClient('goto4', multi_robot.msg.gotoAction)

    # Waits until the action server has started up and started
    # listening for goals.
    client1.wait_for_server()
    client2.wait_for_server()
    # client3.wait_for_server()
    # client4.wait_for_server()

    for i in range(len(points1)):
        # Creates a goal to send to the action server.
        goal = multi_robot.msg.gotoGoal()
        goal.order = []
        x1,y1 = points1[i]
        goal.order.append(x1)
        goal.order.append(y1)
        client1.send_goal(goal)


        goal2 = multi_robot.msg.gotoGoal()
        goal2.order = []
        x2,y2 = points2[i]
        goal2.order.append(x2)
        goal2.order.append(y2)
        client2.send_goal(goal2)

        # goal3 = multi_robot.msg.gotoGoal()
        # goal3.order = []
        # x3,y3 = points3[i]
        # goal3.order.append(x3)
        # goal3.order.append(y3)
        # client3.send_goal(goal3)

        # goal4 = multi_robot.msg.gotoGoal()
        # goal4.order = []
        # x4,y4 = points4[i]
        # goal4.order.append(x4)
        # goal4.order.append(y4)
        # client4.send_goal(goal4)

        client1.wait_for_result()
        client2.wait_for_result()
        # client3.wait_for_result()
        # client4.wait_for_result()

    
        # Prints out the result of executing the action
        result1 = client1.get_result()  # A gotoResult
        print(result1)

        result2 = client2.get_result()  # A gotoResult
        print(result2)

        # result3 = client3.get_result()  # A gotoResult
        # print(result1)

        # result4 = client4.get_result()  # A gotoResult
        # print(result2)
    return True

def reOrder(listPOI):
    indexRobot = list(range(len(listPOI)))
    random.shuffle(indexRobot)
    return indexRobot

def maxPathLength(arena, solution, poi):
    arena.clearPoints()
    arena.goalEndPoints([poi[i] for i in solution])
    finalPath, numberPoints = arena.multiRobotPlanningNinjaTechnique(maxTry = 2)
    if numberPoints == 0:
        numberPoints = float("inf")
    return finalPath, numberPoints


def getNeighbours(solution):
    neighbours = []
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            neighbour = solution.copy()
            neighbour[i] = solution[j]
            neighbour[j] = solution[i]
            neighbours.append(neighbour)
    return neighbours


def getBestNeighbour(arena, neighbours, poi):
    bestPath, bestPathLength = maxPathLength(arena, neighbours[0], poi)
    bestNeighbour = neighbours[0]
    # print("###################")
    for neighbour in neighbours:
        # print("Neighbour",neighbour)
        currentPath, currentPathLength = maxPathLength(arena, neighbour, poi)
        # print(currentPathLength)
        if currentPathLength < bestPathLength:
            bestPathLength = currentPathLength
            bestNeighbour = neighbour
            bestPath = currentPath
    return bestNeighbour, bestPathLength, bestPath


def hillClimbing(poi,maxTry=10):
    instance1 = multiRobot()
    st = time.time()
    currentNeighbourOrder = reOrder(poi)
    currentPathSoution, currentPathLength = maxPathLength(
        instance1, currentNeighbourOrder, poi)
    neighbours = getNeighbours(currentNeighbourOrder)
    # print("Neighbours",neighbours)
    bestNeighbourOrder, bestNeighbourLength, bestPathSolution = getBestNeighbour(instance1, neighbours,poi)
    # print("Best Neighbour", bestNeighbourOrder)
    # print("Best Neighbour Length", bestNeighbourLength)
    # print("###################")
    sameVar = 0
    while (bestNeighbourLength <= currentPathLength and sameVar < maxTry and bestNeighbourLength != 0):
        currentNeighbourOrder = bestNeighbourOrder
        currentPathLength = bestNeighbourLength
        currentPathSoution = bestPathSolution
        neighbours = getNeighbours(currentNeighbourOrder)
        bestNeighbourOrder, bestNeighbourLength, bestPathSolution = getBestNeighbour(
            instance1, neighbours, poi)
        # print("New Neighbour", bestNeighbourOrder)
        # print("New Neighbour Path length",bestNeighbourLength)
        sameVar = sameVar + 1
        # print("Iteration Nos",sameVar)
    print(time.time()-st)
    print("Result")
    
    return currentPathSoution, currentPathLength, currentNeighbourOrder

import time

def unshuffleRobots(robotPath, currentOrder):
    unshuffled = [None]*len(robotPath)
    zeroed = [[None]*len(robotPath),[None]*len(robotPath)]
    for ind,i in enumerate(currentOrder):
        unshuffled[i] = robotPath[ind]
    for _,bot in enumerate(unshuffled):
        something = []
        for ind,i in enumerate(bot):
            something.append(((i[0]-bot[0][0]),(i[1]-bot[0][1])))
        zeroed[_] = something
    return zeroed


def plan():

    ##########################################
    ######## Narrow Corridor #################
    poi = [[(8,16),(8,1)],[(8,2),(8,16)]]
    ##########################################


    ##########################################
    ###########    Plus Sign    ##############
    # poi = [[(8,1),(9,8)],[(1,8),(8,9)]]
    ##########################################
    # poi = [[[2, 10], [4, 10]], [[1, 5], [8, 5]], [[1, 10], [4, 5]],
    #        [[2, 5], [5, 5]]] # points of interest

    # poi = [[(2,10),(4,10)],
    #     [(3,10),(5,1)],
    #     [(6,7),(2,6)],
    #     [(2,9),(7,6)]]

    # poi = [[[2, 10], [4, 10]], [[1, 5], [8, 5]], [[1, 10], [4, 5]],
    #        [[2, 5], [5, 5]]] # points of interest

    # poi = [[(2,10),(4,10)],
    #     [(3,10),(5,1)],
    #     [(6,7),(2,6)],
    #     [(2,9),(7,6)]]
    # poi = [[(8, 16), (8, 2)], [(8, 2), (8, 16)],[(2, 2), (2, 3)],[(3, 3), (3, 4)]]
    #recty
    # poi = [[(5, 16), (15, 15)],
    #        [(11, 15), (16, 9)],
    #        [(1, 9), (7, 1)],
    #        [(2, 4), (11, 2)]]

    #recty copy
    # poi = [[(2, 10), (15, 10)],
    #        [(3, 9), (14, 8)],
    #        [(2, 7), (15, 7)],
    #        [(3, 8), (14, 9)]]

    # paper
    # poi = [[(4, 16), (2, 12)],
    #        [(1, 12), (10, 7)],
    #        [(3, 12), (16, 10)],
    #        [(10, 7), (4, 10)],
    #        [(6, 1), (9, 15)],
    #        [(8, 6), (4, 2)]]
    return hillClimbing(poi,5)
    #print(time.time()-st)



if __name__ == '__main__':
    out = plan()
    finalPath = unshuffleRobots(out[0], out[2])
    print(finalPath)
    try:
        # Initializes a rospy node so that the SimpleActionClient can
        # publish and subscribe over ROS.
        rospy.init_node('goto_client_py')
        # print(finalPath)
        result = goto_client((finalPath)) 
        # print("Result:", result)
    except rospy.ROSInterruptException:
        print("program interrupted before completion", file=sys.stderr)