from __future__ import division
import math
import matplotlib.pyplot as plt


def u0x(x):
    return math.pow(1 + x, 4) / 121


def ut0(t):
    return 1 / math.pow(11 - 10 * t, 2)


def ut1(t):
    return 16 / math.pow(11 - 10 * t, 2)


def solve(steps_l, precision):
    ulist = [[0 for i in range(0, steps_l + 1)]]
    next1 = [0 for i in range(0, steps_l + 1)]

    h = 1 / steps_l
    time = 0
    timestep = 0

    listtau = [math.fabs(u0x(1 / steps_l * i)) for i in range(0, steps_l+1)]

    while time < 1:
        tau = h / max(listtau) / 2

        if time + tau >= 1:
            tau = 1 - time

        for i in range(0, steps_l+1):
            ulist[timestep][i] = u0x(1/steps_l * i)
            next1[i] = u0x(1 / steps_l * i)

        next2 = compute(next1, next1, steps_l, tau, time)

        while max(reldif(next1, next2)) >= precision:
            next2 = compute(next1, next2, steps_l, tau, time)

        time += tau
        timestep += 1
        ulist.append(next2)
        listtau = modlist(next2)

    return ulist


def compute(ref, list, steps_l, tau, time):
    h = 1 / steps_l
    nextlist = [0 for i in range(0, steps_l + 1)]

    nextlist[0] = ut0(time)
    nextlist[steps_l] = ut1(time)
    for i in range(1, steps_l):
        a = list[i + 1]
        b = list[i]
        c = list[i - 1]
        nextlist[i] = ref[i] + tau * ((math.sqrt(math.fabs(a)) + math.sqrt(math.fabs(b))) / 2 / (h * h) * (a - b) - (math.sqrt(math.fabs(c)) + math.sqrt(math.fabs(b))) / 2 / (h * h) * (b - c))
    return nextlist


def modlist(list):
    res = []
    for i in range(0, len(list)):
        res.append(math.fabs(list[i]))
    return res


def dot10(list):
    n = len(list)
    res = []
    for i in range(0, 11):
        res.append(list[int((n-1)/10*i)])
    return res


def reldif(list1, list2):
    res = []
    temp1 = dot10(list1)
    temp2 = dot10(list2)
    for i in range(0, 11):
        res.append(math.fabs(temp1[i] - temp2[i]) / math.fabs(temp2[i]))
    return res


def main():
    steps_l = 64
    precision = math.pow(10, -4)

    func = solve(steps_l, precision)
    print(func)

    return


if __name__ == '__main__':
    main()