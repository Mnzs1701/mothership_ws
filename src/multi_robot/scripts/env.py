"""
Env 2D
@author: huiming zhou
"""

MAXNOS =40

class Env:
    def __init__(self):
        self.x_range = 18  # size of background 18 for others
        self.y_range = 18
        # self.motions = [(-1, 0, 1), (0, 1, 1),
        #                 (1, 0, 1), (0, -1, 1), (0, 0, 1)]
        self.motions = [(-1, 0), (0, 1),
                        (1, 0), (0, -1)]#,(1,1),(-1,1),(1,-1),(-1,-1)]
        self.obs = self.obs_map()

    def update_obs(self, obs):
        self.obs = obs

    def obs_map(self):
        """
        Initialize obstacles' positions
        :return: map of obstacles
        """

        x = self.x_range
        y = self.y_range
        obs = set()

        for i in range(x):
            obs.add((i, 0))

        for i in range(x):
            obs.add((i, y - 1))

        for i in range(y):
            obs.add((0, i))


        for i in range(y):
            obs.add((x - 1, i))

        #Recty
        # for i in range(12):
        #     for j in range(12):
        #         obs.add((i+3, j+3))

        # Copy Recty
        # for i in range(12):
        #     obs.add((i+3,10))
        #     obs.add((i+3,7))
        # obs.remove((8,7))
        # obs.add((8,6))

        # Mine
        # for j in range(17):
        #     obs.add((7,j))
        #     obs.add((9,j))

        # obs.remove((9,10))
        # obs.remove((9,9))
        # obs.remove((9,8))

        # # obs.remove((7,10))
        # # obs.remove((7,9))
        # # obs.remove((7,8))

        # obs.add((10,10))
        # obs.add((10,9))
        # obs.add((10,8))
        # # obs.add((6,8))
        # # obs.add((6,9))

        #paper
        # for i in range(3):
        #     for j in range(16):
        #         obs.add((i+1,j+1))

        # for i in range(3):
        #     for j in range(16):
        #         obs.add((i+5,j+1))

        # for i in range(7):
        #         obs.add((i+8,10))

        # for i in range(5):
        #         obs.add((i+12,8))

        # for i in range(6):
        #     obs.remove((6,i+1))
        # obs.remove((1,12))
        # obs.remove((2,12))
        # obs.remove((3,12))
        # obs.remove((5,12))
        # obs.remove((6,12))
        # obs.remove((7,12))
        # obs.remove((7,6))
        # obs.remove((7,4))
        # obs.remove((7,2))
        # obs.remove((5,2))
        # obs.remove((5,4))

        # obs.add((8,7))
        # obs.add((9,7))
        # obs.add((9,6))
        # obs.add((10,6))
        # obs.add((10,8))
        # obs.add((9,3))
        # obs.add((9,1))
        # obs.add((11,5))
        # obs.add((11,3))
        # obs.add((11,1))
        # obs.add((9,5))

        # for i in range(y):
        #     obs.add((1, i))

        # obs.remove((1,10))
        # obs.remove((1,5))

        # for p in range(MAXNOS):
        #     for i in range(x):
        #         obs.add((i, 0, p))

        #     for i in range(x):
        #         obs.add((i, y - 1, p))

        #     for i in range(y):
        #         obs.add((0, i, p))

        #     for i in range(y):
        #         obs.add((1, i, p))

        #     obs.remove((1,10, p))
        #     obs.remove((1,5, p))

        #     for i in range(y):
        #         obs.add((x - 1, i, p))

        #     for k in range(0,3):
        #         for j in range(0,3):
        #             for i in range(j*4+3, j*4+5):
        #                 obs.add((i+1, k*4+3, p))
        #                 obs.add((i+1, k*4+4, p))
        ################################################
        ############### Narrow Corridor ################
        for j in range(17):
            obs.add((7,j))
            obs.add((9,j))

        obs.remove((9,10))
        obs.remove((9,9))
        obs.remove((9,8))
        obs.add((10,10))
        obs.add((10,9))
        obs.add((10,8))
        ################################################
        # for k in range(0,3):
        #     for j in range(0,3):
        #         for i in range(j*4+3, j*4+5):
        #             obs.add((i, k*4+3))
        #             obs.add((i, k*4+4))
        return obs