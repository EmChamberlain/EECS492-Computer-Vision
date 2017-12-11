from Environment import *
from random import randint
import numpy
import os

layout = [
        ['_','_','_','+'],
        ['_','X','_','-'],
        ['_','_','_','_']
    ]





def test0():
    env = Environment(layout, 0.0)
    policy = env.value_iteration(1)
    print policy
    env = Environment(layout, -0.0001)
    policy = env.value_iteration(1)
    print policy
    #[['v', 'v', '>', '+1'], ['v', 'X', '<', '-1'], ['v', 'v', 'v', 'v']]

def problem1():
    step = 0.0001
    highest = 0.0000
    lowest = -2.0000
    curr = highest
    policies = []
    env = Environment(layout, -0.0001)
    policy_curr = env.value_iteration(1)
    policies.append(policy_curr)
    values = [0.0]

    while curr > lowest:
        top = curr - step
        bot = lowest
        mid = bot + ((int((top - bot) / step) / 2) * step)

        while top > bot:
            env = Environment(layout, mid)
            policy = env.value_iteration(1)
            if policy_curr == policy:
                top = mid - step
            else:
                bot = mid + step
            mid = bot + ((int((top - bot) / step) / 2) * step)
        env = Environment(layout, mid)
        policy = env.value_iteration(1)
        if policy not in policies:
            policies.append(policy)
            values.append(round(mid, 4))
        policy_curr = policy[:]
        curr = mid

    with open("generated/P1-output.txt", "w+") as file:
        for i in xrange(len(policies)):
            val = values[i]
            policy = policies[i]
            file.write(str(val) + "\n")
            for row in policy:
                for char in row:
                    file.write(str(char))
                    file.write("\n")

def monte_carlo(env, policy):
    x = 2
    y = 3
    reward = 0
    while env.layout[x][y] == '_':
        reward += env.reward[x][y]
        move_try = [0, 0]
        if policy[x][y] == 'v':
            move_try = [1, 0]
        elif policy[x][y] == '>':
            move_try = [0, 1]
        elif policy[x][y] == '^':
            move_try = [-1, 0]
        elif policy[x][y] == '<':
            move_try = [0, -1]
        else:
            print 'invalid policy: ' + str(policy[x][y])
            exit(1)
        move_actual = [0, 0]
        rand = randint(0,9)
        if rand == 0:
            move_actual = move_try[::-1]
        elif rand == 1:
            move_actual = [i * -1 for i in move_try[::-1]]
        else:
            move_actual = move_try[:]
        if not env.out_of_bounds(x + move_actual[0], y + move_actual[1]) and env.layout[x + move_actual[0]][y + move_actual[1]] != 'X':
            x = x + move_actual[0]
            y = y + move_actual[1]
    if env.layout[x][y] == '+':
        reward += 1
    elif env.layout[x][y] == '-':
        reward -= 1
    else:
        print 'invalid ending location: ' + str(env.layout[x][y])
        exit(1)
    return reward





def problem2():
    env = Environment(layout, -0.04)
    policy = env.value_iteration(1)

    runs_10 = []
    for i in xrange(10):
        runs_10.append(monte_carlo(env, policy))

    runs_100 = []
    for i in xrange(100):
        runs_100.append(monte_carlo(env, policy))

    runs_1000 = []
    for i in xrange(1000):
        runs_1000.append(monte_carlo(env, policy))

    with open("generated/P2-output.txt", "w+") as file:
        file.write(str("Expected utility: " + str(round(env.util[2][3], 3))) + "\n")
        file.write(str("First run: " + str(round(runs_10[0], 3))) + "\n")
        file.write(str("10-run average utility: " + str(round(sum(runs_10)/len(runs_10), 3))) + "\n")
        file.write(str("10-run standard dev: " + str(round(numpy.std(runs_10), 3))) + "\n")
        file.write(str("100-run average utility: " + str(round(sum(runs_100) / len(runs_100), 3))) + "\n")
        file.write(str("100-run standard dev: " + str(round(numpy.std(runs_100), 3))) + "\n")
        file.write(str("1000-run average utility: " + str(round(sum(runs_1000) / len(runs_1000), 3))) + "\n")
        file.write(str("1000-run standard dev: " + str(round(numpy.std(runs_1000),3))) + "\n")

    with open("generated/P2-data-10.txt", "w+") as file:
        for run in runs_10:
            file.write(str(run) + "\n")
    with open("generated/P2-data-100.txt", "w+") as file:
        for run in runs_100:
            file.write(str(run) + "\n")
    with open("generated/P2-data-1000.txt", "w+") as file:
        for run in runs_1000:
            file.write(str(run) + "\n")


def problem3():
    layout_spec = [
        ['_','_','+'],
        ['_','_','_'],
        ['_', '_', '_']
    ]
    reward_spec = [
        [3,-1,10],
        [-1,-1,-1],
        [-1, -1, -1]
    ]

    step = 0.00001
    highest = 0.999
    lowest = 0.001
    curr = highest
    policies = []
    env = Environment(layout_spec, -1)
    env.set_reward(reward_spec)
    policy_curr = env.value_iteration(0.999)
    policies.append(policy_curr)
    values = [0.999]

    while curr > lowest:
        top = curr - step
        bot = lowest
        mid = bot + ((int((top - bot) / step) / 2) * step)

        while top > bot:
            env = Environment(layout_spec, -1)
            env.set_reward(reward_spec)
            policy = env.value_iteration(mid)
            if policy_curr == policy:
                top = mid - step
            else:
                bot = mid + step
            mid = bot + ((int((top - bot) / step) / 2) * step)
        env = Environment(layout_spec, -1)
        env.set_reward(reward_spec)
        policy = env.value_iteration(mid)
        if policy not in policies:
            policies.append(policy)
            values.append(round(mid, 4))
        policy_curr = policy[:]
        curr = mid

    with open("generated/P3-output.txt", "w+") as file:
        for i in xrange(len(policies)):
            val = values[i]
            policy = policies[i]
            file.write(str(val) + "\n")
            for row in policy:
                for char in row:
                    file.write(str(char))
                    file.write("\n")


def main():
    os.chdir("..")
    #test0()
    problem1()
    problem2()
    problem3()



if __name__ == "__main__":
    main()