


class Environment:

    def __init__(self, lay, cost):
        self.layout = lay
        self.width = len(self.layout[0])
        self.height = len(self.layout)
        self.reward = [[0] * self.width for _ in xrange(self.height)]
        self.util = [[0] * self.width for _ in xrange(self.height)]
        for x in xrange(self.height):
            for y in xrange(self.width):
                if self.layout[x][y] == 'X':
                    self.reward[x][y] = 0
                elif self.layout[x][y] == '+':
                    self.reward[x][y] = 1
                elif self.layout[x][y] == '-':
                    self.reward[x][y] = -1
                elif self.layout[x][y] == '_':
                    self.reward[x][y] = cost
                else:
                    print "Invalid board layout"
                    exit(1)

    def set_reward(self, reward):
        self.reward = reward


    def out_of_bounds(self, x, y):
        if x >= self.height or x < 0:
            return True
        if y >= self.width or y < 0:
            return True
        return False

    def max_reward(self, x, y, util):
        moves = [[1,0], [0,1], [-1,0], [0,-1]]
        unintended = [[[0,1],[0,-1]],[[1,0],[-1,0]],[[0,1],[0,-1]],[[1,0],[-1,0]]]
        max_reward = float('-inf')
        max_move = [0,0]
        for i in xrange(len(moves)):
            reward = 0
            move = moves[i]
            xn = x + move[0]
            yn = y + move[1]

            xu0 = x + unintended[i][0][0]
            yu0 = y + unintended[i][0][1]

            xu1 = x + unintended[i][1][0]
            yu1 = y + unintended[i][1][1]


            if not self.out_of_bounds(xn,yn) and self.layout[xn][yn] != 'X':
                reward += 0.8 * util[xn][yn]
            else:
                reward += 0.8 * util[x][y]

            if not self.out_of_bounds(xu0,yu0) and self.layout[xu0][yu0] != 'X':
                reward += 0.1 * util[xu0][yu0]
            else:
                reward += 0.1 * util[x][y]

            if not self.out_of_bounds(xu1,yu1) and self.layout[xu1][yu1] != 'X':
                reward += 0.1 * util[xu1][yu1]
            else:
                reward += 0.1 * util[x][y]



            if reward > max_reward:
                max_reward = reward
                max_move = move

        return max_reward, max_move






    def value_iteration(self, gamma):
        util_prev = [[0]*self.width for _ in xrange(self.height)]
        util_curr = [[0]*self.width for _ in xrange(self.height)]
        count = 0
        while True:
            count += 1
            sigma = 0
            for x in xrange(self.height):
                for y in xrange(self.width):
                    util_curr[x][y] = self.reward[x][y]
                    if not self.layout[x][y] == '_':
                        continue
                    max_reward, _ = self.max_reward(x, y, util_prev)
                    util_curr[x][y] += gamma * max_reward
                    diff = abs(util_curr[x][y] - util_prev[x][y])
                    if diff > sigma:
                        sigma = diff
            if sigma < 0.0000001:
                break
            util_prev = util_curr[:]
            util_curr = [[0]*self.width for _ in xrange(self.height)]

        policy = [['*']*self.width for _ in xrange(self.height)]
        for x in xrange(self.height):
            for y in xrange(self.width):
                if self.layout[x][y] == '+':
                    policy[x][y] = '+1'
                elif self.layout[x][y] == '-':
                     policy[x][y] = '-1'
                elif self.layout[x][y] == 'X':
                     policy[x][y] = 'X'
                else:
                    max_reward, move = self.max_reward(x, y, util_curr)
                    if move == [1,0]:
                        policy[x][y] = 'v'
                    elif move == [0,1]:
                        policy[x][y] = '>'
                    elif move == [-1,0]:
                        policy[x][y] = '^'
                    elif move == [0,-1]:
                        policy[x][y] = '<'
        self.util = util_curr[:]
        return policy
