import random
import numpy.linalg as l
import copy
from scipy.stats import f, t

#variant 110
#           min    max
#       x1  -20    15
#       x2   10    60
#       x3   15    35


def cohren(f1, f2, q=0.05):
    q1 = q / f1
    cohren1 = f.ppf(q=1 - q1, dfn=f2, dfd=(f1 - 1) * f2)
    return round(cohren1/ (cohren1 + f1 - 1),4)
def fisher(f1,f2, q=1-0.05):
    fisher1=f.ppf(q,dfn=f2,dfd=f1)
    return round(fisher1,4)
def student(f3, q=1-0.025):
    student1=t.ppf(q,df=f3)
    return round(student1,4)
def print_arr(arr):
    for i in arr: print(i)

def foo(*args):
    res = [1 for k in range(len(args[0]))]
    for i in range(len(args[0])):
        for j in args:
            res[i] *= j[i]
    return res

def det_getter(num):
    det_i = copy.deepcopy(ms)
    for i in range(N):
        det_i[i][num] = k[i]
    return det_i
def arr_ser(arr):
    return round(sum(arr)/len(arr),4)

x1 = [-20, 15]
x2 = [10, 60]
x3 = [15, 35]

m = 2
N = 8
q = 0.05

x = [[min(x1), min(x1), min(x1), min(x1), max(x1), max(x1), max(x1), max(x1)],
     [min(x2), min(x2), max(x2), max(x2), min(x2), min(x2), max(x2), max(x2)],
     [min(x3), max(x3), min(x3), max(x3), max(x3), min(x3), max(x3), min(x3)]]

x_avg = [(max(x1) + max(x2) + max(x3)) / 3, (min(x1) + min(x2) + min(x3)) / 3]

y_znach = [200 + max(x_avg), 200 + min(x_avg)]
while True:
    y = [[round(random.uniform(min(y_znach), max(y_znach)), 4) for i in range(m)] for j in range(N)]
    y_avg = list(map(arr_ser, y))
    print("\n Матриця планування експерименту \n")
    for i in range(N):
        print("{:<12}  {:<12}  {:<12}".format(str([x[j][i] for j in range(3)]), str([y[i][j] for j in range(m)]), str(y_avg[i])))

    mx = list(map(arr_ser, x))

    forb = ([1 for k in range(N)], x[0], x[1], x[2], foo(x[0], x[1]), foo(x[0], x[2]), foo(x[1], x[2]),foo(x[0], x[1], x[2]))
    # print(forb)
    ms = list(list(sum(foo(forb[i], forb[j])) for j in range(N)) for i in range(N))
    k = [sum(foo(y_avg, forb[i])) for i in range(N)]

    my_det = l.det(ms)

    b = [l.det(det_getter(i)) / my_det for i in range(N)]

    y_regr = [round(
        b[0] + b[1] * x[0][i] + b[2] * x[1][i] + b[3] * x[2][i] + b[4] * x[0][i] * x[1][i] + b[5] * x[0][i] * x[2][i] + b[6] * x[1][i] * x[2][i] + b[7] * x[0][i] * x[1][i] * x[2][i], 4) for i in range(N)]
    print("\ny-ки регресій")
    print_arr(y_regr)

    f1 = m - 1
    f2 = N
    f3 = f1 * f2
    D = []
    for i in range(N):
        tmp = 0
        for num in range(m):
            tmp += (y[i][num] - y_regr[i]) ** 2
        D.append(tmp)

    print("D:"+str(D))

    Gp = max(D) / sum(D)
    Gt = cohren(f1+1,f2)

    print("Однорідність дисперсії (критерій Кохрена): ")
    print("Gp = {}".format(round(Gp,5)))
    print("Gt = {}".format(round(Gt,5)))
    if Gp < Gt:
        print("Дисперсія однорідна (Gp < Gt)")
        S = sum(D) / N
        Sb = S / (N * m)
        beta = [(y_regr[0] + y_regr[1] + y_regr[2] + y_regr[3] + y_regr[4] + y_regr[5] + y_regr[6] + y_regr[7]) / N,
                (-y_regr[0] - y_regr[1] - y_regr[2] - y_regr[3] + y_regr[4] + y_regr[5] + y_regr[6] + y_regr[7]) / N,
                (-y_regr[0] - y_regr[1] + y_regr[2] + y_regr[3] - y_regr[4] - y_regr[5] + y_regr[6] + y_regr[7]) / N,
                (-y_regr[0] + y_regr[1] - y_regr[2] + y_regr[3] - y_regr[4] + y_regr[5] - y_regr[6] + y_regr[7]) / N,
                (y_regr[0] + y_regr[1] - y_regr[2] - y_regr[3] - y_regr[4] - y_regr[5] + y_regr[6] + y_regr[7]) / N,
                (y_regr[0] - y_regr[1] + y_regr[2] - y_regr[3] - y_regr[4] + y_regr[5] - y_regr[6] + y_regr[7]) / N,
                (y_regr[0] - y_regr[1] - y_regr[2] + y_regr[3] + y_regr[4] - y_regr[5] - y_regr[6] + y_regr[7]) / N,
                (-y_regr[0] + y_regr[1] + y_regr[2] - y_regr[3] + y_regr[4] - y_regr[5] - y_regr[6] + y_regr[7]) / N]
        t1 = [abs(i) / Sb for i in beta]
        t_kr = student(f3)
        print(t_kr)
        print(t1)
        t_final = list(filter(lambda x: x > t_kr, t1))
        f4 = N - len(t_final)
        print("\nЗначимі коефіцієнти: "), print_arr(t_final)
        print("t: " + str(t1))
        print("t фінальна: " + str(t_final))
        print("Бета: " + str(beta))

        f_sum = 0
        for i in range(N):
            f_sum += pow((t1[i] - y_regr[i]), 2)
        D_ad = (m / (f4)) * f_sum
        print(f_sum)
        print(D_ad)
        print(Sb)
        Fp = D_ad / Sb
        print("Fp = {}".format(round(Fp, 5)))
        Ft = fisher(f3, f4)
        print("Ft = {}".format(round(Ft, 5)))
        if Ft > Fp:
            print(f"Ft > Fp\nРівняння регресії адекватно оригіналу при рівні значимості {q}")
            break
        else:
            print(f"Ft < Fp\nРівняння регресії неадекватно оригіналу при рівні значимості {q}")
            m+=1
    else:
        print("Дисперсія неоднорідна (Gp > Gt), збільшуємо m, повторюємо операції")
        m += 1

