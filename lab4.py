import random
import numpy.linalg as l
import copy


G_table = (
    (9985, 9750, 9392, 9057, 8772, 8534, 8332, 8159, 8010, 7880),
    (9669, 8709, 7977, 7457, 7071, 6771, 6530, 6333, 6167, 6025),
    (9065, 7679, 6841, 6287, 5892, 5598, 5365, 5175, 5017, 4884),
    (8412, 6838, 5981, 5440, 5063, 4783, 4564, 4387, 4241, 4118),
    (7808, 6161, 5321, 4803, 4447, 4184, 3980, 3817, 3682, 3568),
    (7271, 5612, 4800, 4307, 3974, 3726, 3535, 3384, 3259, 3154),
    (6798, 5157, 4377, 3910, 3595, 3362, 3185, 3043, 2926, 2829),
    (6385, 4775, 4027, 3584, 3286, 3067, 2901, 2768, 2659, 2568),
    (6020, 4450, 3733, 3311, 3029, 2823, 2666, 2541, 2439, 2353))

t_table = [12.71, 4.303, 3.182, 2.776, 2.571, 2.447, 2.365, 2.306, 2.262, 2.228, 2.201, 2.179, 2.16, 2.145, 2.131,
           2.12, 2.11]

F_table = (
     (164.4, 199.5, 215.7, 224.6, 230.2, 234),
     (18.5, 19.2, 19.2, 19.3, 19.3, 19.3),
     (10.1, 9.6, 9.3, 9.1, 9, 8.9),
     (7.7, 6.9, 6.6, 6.4, 6.3, 6.2),
     (6.6, 5.8, 5.4, 5.2, 5.1, 5),
     (6, 5.1, 4.8, 4.5, 4.4, 4.3),
     (5.5, 4.7, 4.4, 4.1, 4, 3.9),
     (5.3, 4.5, 4.1, 3.8, 3.7, 3.6),
     (5.1, 4.3, 3.9, 3.6, 3.5, 3.4),
     (5, 4.1, 3.7, 3.5, 3.3, 3.2),
     (4.8, 4, 3.6, 3.4, 3.2, 3.1),
     (4.8, 3.9, 3.5, 3.3, 3.1, 3),
     (4.7, 3.8, 3.4, 3.2, 3.0, 2.9, 2.6, 2.4, 2.2),
     (4.6, 3.7, 3.3, 3.1, 3.0, 2.9, 2.5, 2.3, 2.1),
     (4.5, 3.7, 3.3, 3.1, 2.9, 2.8, 2.5, 2.3, 2.1),
     (4.5, 3.6, 3.2, 3.0, 2.9, 2.7, 2.4, 2.2, 2.0))

#variant 110
#           min    max
#       x1  -20    15
#       x2   10    60
#       x3   15    35


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

m = 3
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
    Gt = G_table[f2 - 2][f1 - 1] * 0.0001

    print("Однорідність дисперсії (критерій Кохрена): ")
    print("Gp = {}".format(round(Gp,5)))
    print("Gt = {}".format(round(Gt,5)))
    if Gp < Gt:
        print("Дисперсія однорідна (Gp < Gt)")
        break
    else:
        print("Дисперсія неоднорідна (Gp > Gt), збільшуємо m, повторюємо операції")
        m += 1

S= sum(D) / N
Sb = S/ (N * m)
beta = [(y_regr[0] + y_regr[1] + y_regr[2] + y_regr[3] + y_regr[4] + y_regr[5] + y_regr[6] + y_regr[7]) / N,
        (-y_regr[0] - y_regr[1] - y_regr[2] - y_regr[3] + y_regr[4] + y_regr[5] + y_regr[6] + y_regr[7]) / N,
        (-y_regr[0] - y_regr[1] + y_regr[2] + y_regr[3] - y_regr[4] - y_regr[5] + y_regr[6] + y_regr[7]) / N,
        (-y_regr[0] + y_regr[1] - y_regr[2] + y_regr[3] - y_regr[4] + y_regr[5] - y_regr[6] + y_regr[7]) / N,
        (y_regr[0] + y_regr[1] - y_regr[2] - y_regr[3] - y_regr[4] - y_regr[5] + y_regr[6] + y_regr[7]) / N,
        (y_regr[0] - y_regr[1] + y_regr[2] - y_regr[3] - y_regr[4] + y_regr[5] - y_regr[6] + y_regr[7]) / N,
        (y_regr[0] - y_regr[1] - y_regr[2] + y_regr[3] + y_regr[4] - y_regr[5] - y_regr[6] + y_regr[7]) / N,
        (-y_regr[0] + y_regr[1] + y_regr[2] - y_regr[3] + y_regr[4] - y_regr[5] - y_regr[6] + y_regr[7]) / N]
t = [abs(i) / Sb for i in beta]
t_kr = t_table[f3 - 1]
print(t_kr)
print(t)
t_final = list(filter(lambda x: x > t_kr, t))
f4 = N - len(t_final)
print("\nЗначимі коефіцієнти: "), print_arr(t_final)
print("t: "+str(t))
print("t фінальна: "+str(t_final))
print("Бета: "+str(beta))

f_sum= 0
for i in range(N):
    f_sum+= pow((t[i] - y_regr[i]), 2)
D_ad = (m / (f4)) *f_sum
Fp = D_ad / Sb
print("Fp = {}".format(round(Fp,5)))
Ft = F_table[f3 - 1][f4 - 1]
print("Ft = {}".format(round(Ft,5)))
if Ft > Fp:
    print(f"Ft > Fp\nРівняння регресії адекватно оригіналу при рівні значимості {q}")
else:
    print(f"Ft < Fp\nРівняння регресії неадекватно оригіналу при рівні значимості {q}")


