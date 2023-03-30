
from numpy.core.fromnumeric import sort
import env
#import plotting
import os
import sys
import math
#import matplotlib.pyplot as plt

import time


class DStar:
    def __init__(self, s_start, s_goal,max_tries=10):
        self.s_start, self.s_goal, self.max_tries = s_start, s_goal,max_tries

        self.Env = env.Env()
        # self.Plot = plotting.Plotting(self.s_start, self.s_goal)

        self.u_set = self.Env.motions
        self.obs = self.Env.obs
        self.x = self.Env.x_range
        self.y = self.Env.y_range
        # self.fig = plt.figure()

        self.OPEN = set()
        self.t = dict()
        self.PARENT = dict()
        self.h = dict()
        self.k = dict()
        self.path = []
        self.visited = set()
        self.count = 0

    def init(self):
        for i in range(self.Env.x_range):
            for j in range(self.Env.y_range):
                self.t[(i, j)] = 'NEW'
                self.k[(i, j)] = 0.0
                self.h[(i, j)] = float("inf")
                self.PARENT[(i, j)] = None

        self.h[self.s_goal] = 0.0

    def run(self, s_start, s_end):
        """
        MAIN pgm
        """

        self.init()
        self.insert(s_end, 0)

        while True:
            self.process_state()
            if self.t[s_start] == 'CLOSED':
                break

        self.path = self.extract_path(s_start, s_end)

    def extract_path(self, s_start, s_end):
        """
        Give me path
        """
        path = [s_start]
        s = s_start
        while True:
            s = self.PARENT[s]
            path.append(s)
            if s == s_end:
                return path

    def process_state(self):
        s = self.min_state()  # get node in OPEN set with min k value
        # print(s)
        self.visited.add(s)

        if s is None:
            return -1  # OPEN set is empty

        k_old = self.get_k_min()  # record the min k value of this iteration (min path cost)

        # print(k_old)
        # print(self.h[s])
        self.delete(s)  # move state s from OPEN set to CLOSED set
        # k_min < h[s] --> s: RAISE state (increased cost)
        if k_old < self.h[s]:
            for s_n in self.get_neighbor(s):
                if self.h[s_n] <= k_old and \
                        self.h[s] > self.h[s_n] + self.cost(s_n, s):

                    # update h_value and choose parent
                    self.PARENT[s] = s_n
                    self.h[s] = self.h[s_n] + self.cost(s_n, s)

        # s: k_min >= h[s] -- > s: LOWER state (cost reductions)
        if k_old == self.h[s]:
            for s_n in self.get_neighbor(s):
                if self.t[s_n] == 'NEW' or \
                        (self.PARENT[s_n] == s and self.h[s_n] != self.h[s] + self.cost(s, s_n)) or \
                        (self.PARENT[s_n] != s and self.h[s_n] > self.h[s] + self.cost(s, s_n)):

                    # Condition:
                    # 1) t[s_n] == 'NEW': not visited
                    # 2) s_n's parent: cost reduction
                    # 3) s_n find a better parent
                    self.PARENT[s_n] = s
                    self.insert(s_n, self.h[s] + self.cost(s, s_n))
        else:
            for s_n in self.get_neighbor(s):
                if self.t[s_n] == 'NEW' or \
                        (self.PARENT[s_n] == s and self.h[s_n] != self.h[s] + self.cost(s, s_n)):

                    # Condition:
                    # 1) t[s_n] == 'NEW': not visited
                    # 2) s_n's parent: cost reduction
                    self.PARENT[s_n] = s
                    self.insert(s_n, self.h[s] + self.cost(s, s_n))
                else:
                    if self.PARENT[s_n] != s and \
                            self.h[s_n] > self.h[s] + self.cost(s, s_n):

                        # Condition: LOWER happened in OPEN set (s), s should be explored again
                        self.insert(s, self.h[s])
                    else:
                        if self.PARENT[s_n] != s and \
                                self.h[s] > self.h[s_n] + self.cost(s_n, s) and \
                                self.t[s_n] == 'CLOSED' and \
                                self.h[s_n] > k_old:

                            # Condition: LOWER happened in CLOSED set (s_n), s_n should be explored again
                            self.insert(s_n, self.h[s_n])

        return self.get_k_min()

    def min_state(self):
        """
        choose the node with the minimum k value in OPEN set.
        :return: state
        """

        if not self.OPEN:
            return None

        return min(self.OPEN, key=lambda x: self.k[x])

    def get_k_min(self):
        """
        calc the min k value for nodes in OPEN set.
        :return: k value
        """

        if not self.OPEN:
            return -1

        return min([self.k[x] for x in self.OPEN])

    def insert(self, s, h_new):
        """
        insert node into OPEN set.
        :param s: node
        :param h_new: new or better cost to come value
        """

        if self.t[s] == 'NEW':
            self.k[s] = h_new
        elif self.t[s] == 'OPEN':
            self.k[s] = min(self.k[s], h_new)
        elif self.t[s] == 'CLOSED':
            self.k[s] = min(self.h[s], h_new)

        self.h[s] = h_new
        self.t[s] = 'OPEN'
        self.OPEN.add(s)

    def delete(self, s):
        """
        delete: move state s from OPEN set to CLOSED set.
        :param s: state should be deleted
        """

        if self.t[s] == 'OPEN':
            self.t[s] = 'CLOSED'

        self.OPEN.remove(s)

    def modify(self, s):
        """
        start processing from state s.
        :param s: is a node whose status is RAISE or LOWER.
        """
        i=0
        self.modify_cost(s)

        while True and i < self.max_tries:
            i=i+1
            k_min = self.process_state()

            if k_min >= self.h[s]:
                break
            if k_min == -1:
                return -1

    def modify_cost(self, s):
        # if node in CLOSED set, put it into OPEN set.
        # Since cost may be changed between s - s.parent, calc cost(s, s.p) again

        if self.t[s] == 'CLOSED':
            self.insert(s, self.h[self.PARENT[s]] +
                        self.cost(s, self.PARENT[s]))

    def get_neighbor(self, s):
        nei_list = set()

        for u in self.u_set:
            s_next = tuple([s[i] + u[i] for i in range(2)])
            if s_next not in self.obs:
                nei_list.add(s_next)

        return nei_list

    def cost(self, s_start, s_goal):
        """
        Calculate Cost for this motion
        :param s_start: starting node
        :param s_goal: end node
        :return:  Cost for this motion
        :note: Cost function could be more complicate!
        """

        if self.is_collision(s_start, s_goal):
            return float("inf")

        return math.hypot(s_goal[0] - s_start[0], s_goal[1] - s_start[1])

    def is_collision(self, s_start, s_end):
        if s_start in self.obs or s_end in self.obs:
            return True

        if s_start[0] != s_end[0] and s_start[1] != s_end[1]:
            if s_end[0] - s_start[0] == s_start[1] - s_end[1]:
                s1 = (min(s_start[0], s_end[0]), min(s_start[1], s_end[1]))
                s2 = (max(s_start[0], s_end[0]), max(s_start[1], s_end[1]))
            else:
                s1 = (min(s_start[0], s_end[0]), max(s_start[1], s_end[1]))
                s2 = (max(s_start[0], s_end[0]), min(s_start[1], s_end[1]))

            if s1 in self.obs or s2 in self.obs:
                return True

        return False

    # def plot_path(self, path):
    #     px = [x[0] for x in path]
    #     py = [x[1] for x in path]
    #     # plt.plot(px, py, linewidth=2)
    #     # plt.plot(self.s_start[0], self.s_start[1], "bs")
    #     # plt.plot(self.s_goal[0], self.s_goal[1], "gs")
    #     # self.fig = plt.figure()

    # def plot_visited(self, visited):
    #     color = ['gainsboro', 'lightgray', 'silver', 'darkgray',
    #              'bisque', 'navajowhite', 'moccasin', 'wheat',
    #              'powderblue', 'skyblue', 'lightskyblue', 'cornflowerblue']

    #     if self.count >= len(color) - 1:
    #         self.count = 0

    #     # for x in visited:
    #         # plt.plot(x[0], x[1], marker='s', color=color[self.count])



class multiRobot:
    def __init__(self):
        # self.s1_start = (2, 10)
        # self.s1_goal = (3, 5)
        # self.s2_start = (1, 10)
        # self.s2_goal = (7, 5)
        # self.s3_start = (2, 5)
        # self.s3_goal = (8, 5)
        # self.s4_start = (1, 5)
        # self.s4_goal = (7, 6)
        self.Env = env.Env()
        self.starts = list()
        self.goals = list()
        self.nosRobos = 0

    def goalEndPoints(self,robos):
        self.nosRobos = len(robos)
        for i in range(self.nosRobos):
            self.starts.append(tuple(robos[i][0]))
            self.goals.append(tuple(robos[i][1]))
        # print(self.starts)
        # print(self.goals)
        # self.Plot = plotting.Plotting(self.starts, self.goals)

    def clearPoints(self):
        self.starts = []
        self.goals = []
        # print(self.starts)
        # print(self.goals)
        # self.Plot = plotting.Plotting(self.starts, self.goals)

    def pathplanner(self):
        dstarAlgoList = list()
        for i in range(self.nosRobos):
            dstarAlgoList.append(DStar(self.starts[i], self.goals[i]))
            dstarAlgoList[i].run(self.starts[i], self.goals[i])
        return dstarAlgoList


    # def plot_path(self, path):
    #     px = [x[0] if x[0] else None for x in path]
    #     py = [x[1] if x[1] else None for x in path]
        # py = [x[1] for x in path]
        # self.Plot.plot_grid("Multi-Robot-Kardeplan")
        #plt.plot(px, py, linewidth=2)
        # plt.plot(self.s_start[0], self.s_start[1], "bs")
        # plt.plot(self.s_goal[0], self.s_goal[1], "gs")

    # def plot_visited(self, visited):
    #     color = ['gainsboro', 'lightgray', 'silver', 'darkgray',
    #              'bisque', 'navajowhite', 'moccasin', 'wheat',
    #              'powderblue', 'skyblue', 'lightskyblue', 'cornflowerblue']

    #     if self.count >= len(color) - 1:
    #         self.count = 0

        #for x in visited:
            #plt.plot(x[0], x[1], marker='s', color=color[self.count])


    def rePlan(self,start,goal,robo,obstacle,max_try = 50):
        s = start
        robo.obs.add((obstacle[0], obstacle[1]))
        # print("obs")
        # print(robo.obs)
        i = 0
        while s != robo.s_goal and i != -1 and i!=None:
            if robo.is_collision(s, robo.PARENT[s]):
                i = robo.modify(s)
                continue
            s = robo.PARENT[s]

        if i == -1:
            robo.path = robo.extract_path(start,goal)
            index = robo.path.index((obstacle[0], obstacle[1]))
            robo.path.insert(index,robo.path[index-1])
            # print("Adding Wait state at index:", index)
            return
        # print(i)
        robo.path = robo.extract_path(start,goal)


    def multiRobotPlanningNinjaTechnique(self, maxTry=10):
        dstar = self.pathplanner()
        # numberPoints = max(len(dstar[2].path),len(dstar[1].path),len(dstar[3].path),len(dstar[0].path))

        for _ in range(2):
            numberPoints = max(len(dstar[i].path) for i in range(self.nosRobos))
            # toRetNumberPoints = max(len(dstar[i].path) for i in range(self.nosRobos))
            # leastPoint = min(len(dstar[i].path) for i in range(self.nosRobos))

                # PADDING
            for i in range(self.nosRobos):
                dstar[i].path += [dstar[i].path[-1]] * \
                    (numberPoints - len(dstar[i].path))
                # print("obs")
                # print(dstar[i].obs)
                # print(dstar[i].path)
                # print(dstar[i].path[-1])
                collide = 1
            for i in range(self.nosRobos):
                for j in range(i+1, self.nosRobos):
                    collide = 1
                    nosTry = 0
                    while collide == 1:
                        if nosTry<maxTry:
                            for k in range(numberPoints-1):
                                # print(i,j,k)
                                # print("DSTAR",dstar[i].path)
                                # print("DSTAR", dstar[j].path)

                                if(dstar[i].path[k] == dstar[j].path[k]):
                                    # print("Collision" , i , j)
                                    # print(dstar[i].path[k], dstar[j].path[k])
                                    if (dstar[j].path[k] == self.goals[j]):
                                        self.rePlan(
                                            self.starts[i], self.goals[i], dstar[i], dstar[i].path[k])
                                        dstar[i].path += [dstar[i].path[-1]] * \
                                            (numberPoints - len(dstar[i].path))
                                        # print("Robot",j,"cant move")

                                    else:
                                        self.rePlan(
                                            self.starts[j], self.goals[j], dstar[j], dstar[j].path[k])
                                        dstar[j].path += [dstar[j].path[-1]] * \
                                            (numberPoints - len(dstar[j].path))
                                    # print(dstar[i].path)
                                    collide = 1
                                    break

                                if(dstar[i].path[k] == dstar[j].path[k+1] and dstar[i].path[k+1] == dstar[j].path[k]):
                                    # print("Collision Interchange", i, j)
                                    # print(dstar[i].path[k], dstar[i].path[k+1])
                                    if dstar[j].path[k] == self.goals[j]:
                                        # print("Robot",j,"cant move")
                                        self.rePlan(
                                            self.starts[i], self.goals[i], dstar[i], dstar[i].path[k])
                                        dstar[i].path += [dstar[i].path[-1]] * \
                                            (numberPoints - len(dstar[i].path))

                                    else:
                                        self.rePlan(
                                            self.starts[j], self.goals[j], dstar[j], dstar[j].path[k])
                                        dstar[j].path += [dstar[j].path[-1]] * \
                                            (numberPoints - len(dstar[j].path))
                                    # print(dstar[j].path)
                                    collide = 1
                                    break

                                # elif (dstar[i].path[k] != dstar[j].path[k]) and (dstar[i].path[k] != (0, 0)) and (dstar[i].path[k] != dstar[j].path[k+1] and dstar[i].path[k+1] != dstar[j].path[k]):
                                elif (dstar[i].path[k] != dstar[j].path[k]) and (dstar[i].path[k] != dstar[j].path[k+1] and dstar[i].path[k+1] != dstar[j].path[k]):
                                    collide = 0
                            nosTry = nosTry + 1
                        else:
                            # print("Cant Find Solution")
                            # print("##################")
                            return [],0


        # print("FINAL PAKA")
        finalPath = list()
        #plt.cla()
        for i in range(self.nosRobos):
            finalPath.append(dstar[i].path)
            # print(dstar[i].path)
            # self.plot_path(dstar[i].path)

        toRetNumberPoints = max(len(dstar[i].path) for i in range(self.nosRobos))
        # plt.show()
        #plt.savefig("img/"+str(time.time())+'.png')
        return finalPath, toRetNumberPoints



def main():
    instance1 = multiRobot()
    # instance1.goalEndPoints([[(3, 10), (4, 5)],
    #                         [(2, 10), (8, 5)]]
    #                         )

    # # recty coordinates
    # instance1.goalEndPoints([[(5, 16), (15, 15)],[(11,15),(16,9)],[(1,9),(7,1)],[(2,4),(11,2)]])

    # recty coordinates
    # instance1.goalEndPoints([[(5, 16), (15, 15)],[(11,15),(16,9)],[(1,9),(7,1)],[(2,4),(11,2)]])

    #recty copy
    # instance1.goalEndPoints([[(2,10),(15,10)],[(3,9),(14,8)],[(2,7),(15,7)],[(3,8),(14,9)]])

    # mine
    # instance1.goalEndPoints([[(8, 16), (8, 1)], [(8, 2), (8, 16)]])

    # instance1.goalEndPoints([[(4, 16), (2, 12)],
    #                          [(1, 12), (10, 7)],
    #                          [(3, 12), (16, 10)],
    #                          [(10, 7), (4, 10)],
    #                          [(6, 1), (9, 15)],
    #                          [(8,6),(4,2)]])  #

    # instance1.goalEndPoints([[[2, 10], [4, 10]], [[1, 10], [4, 5]], [[2, 5], [5, 5]], [[1, 5], [8, 5]]]
    #                         )
    # instance1.goalEndPoints([[(3, 10), (4, 5)],
    #                         [(2, 10), (8, 5)],
    #                         [(3, 5), (4, 10)]]
    #                         )
    # instance1.goalEndPoints([[(3, 10), (4, 5)],
    #                         [(2, 10), (8, 5)],
    #                         [(3, 5), (4, 10)],
    #                         [(2, 5), (8, 6)]]
    #                         )
    # instance1.goalEndPoints([[(3, 10), (4, 5)],
    #                         [(4, 10), (4, 6)],
    #                         [(2, 10), (8, 5)],
    #                         [(3, 5), (4, 10)],
    #                         [(2, 5), (8, 6)]]
    #                         )
    # instance1.goalEndPoints([[(2,10),(4,10)],
    #                         [(3,10),(5,1)],
    #                         [(6,7),(2,6)],
    #                         [(2,9),(7,6)]])


    # instance1.goalEndPoints([[(3, 10), (4, 5)],
    #                         [(4, 10), (4, 6)],
    #                         [(7, 10), (3, 10)],
    #                         [(4, 5), (10, 6)],
    #                         [(2, 10), (8, 5)],
    #                         [(3, 5), (4, 10)],
    #                         [(2, 5), (8, 6)]]
    #                         )
    # instance1.goalEndPoints([[(3, 10), (4, 5)],
    #                         [(4, 10), (4, 6)],
    #                         [(7, 10), (3, 10)],
    #                         [(4, 5), (10, 6)],
    #                         [(8, 5), (5, 6)],
    #                         [(2, 10), (8, 5)],
    #                         [(10, 11), (11, 1)],
    #                         [(12, 6), (9, 10)],
    #                         [(9, 9), (14, 6)],
    #                         [(3, 5), (4, 10)]]
    #                         )
    instance1.multiRobotPlanningNinjaTechnique()
    # s_start = (1, 5)
    # s_goal = (10, 10)
    # dstar = DStar(s_start, s_goal)
    # dstar.run(s_start, s_goal)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
