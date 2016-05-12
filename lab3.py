from __future__ import division
import math
import matplotlib.pyplot as plt


def u0x(x):
    return math.pow(1 + x, 4) / 121


def ut0(t):
    return 1 / math.pow(11 - 10 * t, 2)


def ut1(t):
    return 16 / math.pow(11 - 10 * t, 2)


def solution(t, steps_l):
    x = [i / (steps_l) for i in range(0, steps_l + 1)]
    return [math.pow(1+x[i], 4) / math.pow(11-10*t, 2) for i in range(0, steps_l + 1)]


def solve(steps_l, precision):
    ulist = [[0 for i in range(0, steps_l + 1)]]
    next1 = [0 for i in range(0, steps_l + 1)]

    h = 1 / steps_l
    time = 0
    timestep = 0

    listtau = [math.fabs(u0x(1 / steps_l * i)) for i in range(0, steps_l+1)]

    while time < 1:
        tau = h / max(listtau) / 2
        #print(tau)
        if time + tau >= 1:
            tau = 1 - time

        for i in range(0, steps_l+1):
            ulist[timestep][i] = u0x(1/steps_l * i)
            next1[i] = u0x(1 / steps_l * i)

        next2 = compute(next1, next1, steps_l, tau, time)
        temp = next1

        while max(reldif(temp, next2)) >= precision:
            temp = next2
            next2 = compute(next1, next2, steps_l, tau, time)



        time += tau
        timestep += 1
        ulist.append(next2)
        listtau = modlist(next2)

    return ulist


def compute(ref, list, steps_l, tau, time):
    h = 1 / steps_l
    nextlist = [0 for i in range(0, steps_l + 1)]
    #nextlist[0] = ut0(time+tau)
    #nextlist[steps_l] = ut1(time+tau)

    a = [0] + [-tau*(math.sqrt(list[i]) + math.sqrt(list[i-1]))/2/h/h for i in range(1, steps_l)] + [0] #check this
    b = [0] + [-tau*(math.sqrt(list[i+1]) + math.sqrt(list[i]))/2/h/h for i in range(1, steps_l)] + [0] #check this
    c = [1] + [1 - a[i] - b[i] for i in range(1, steps_l)] + [1] #check this
    f = [ut0(time+tau)] + [ref[i] for i in range(1, steps_l)] + [ut1(time+tau)] #check this time + tau
    b_1 = [b[0]]
    f_1 = [f[0]]
    for i in range(1, steps_l+1):
        b_1.append(b[i]/(c[i]-a[i]*b_1[i-1]))
        f_1.append((f[i]-a[i]*f_1[i-1])/(c[i]-a[i]*b_1[i-1]))

    nextlist[steps_l] = f_1[steps_l]
    for i in reversed(range(0, steps_l)):
        nextlist[i] = f_1[i] - b_1[i]*nextlist[i+1]

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
    steps_l = 100
    precision = math.pow(10, -4)

    func = solve(steps_l, precision)
    print(func[len(func)-1])
    print(solution(1, steps_l))

    p_funcs = plt.figure("Exact and numerical solutions")
    ax_p_funcs = p_funcs.add_subplot(111)
    ax_p_funcs.plot([i / (steps_l+1) for i in range(0, steps_l+1)], func[len(func)-1], marker="o")
    ax_p_funcs.plot([i / (steps_l + 1) for i in range(0, steps_l + 1)], solution(1, steps_l), marker="^")
    plt.show()

    return


if __name__ == '__main__':
    main()