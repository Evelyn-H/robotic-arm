from math import *

h = 8.4 + 1

def d(a1, a2, l1 = 10, l2 = 11):
    return l2 * sin(radians(a1)) + l1 * sin(radians(a1+a2))


def a2(a1, h):
    return degrees(acos( (h-cos(radians(a1))*10.7) / 10.4 )) - a1


def D(a1, a0):
    return d(a1, a2(a1, h)) * cos(radians(a0))

D(45, 30)


def search(target, f, min, max, tolerance = 0.1):
    fmin = f(min)
    fmax = f(max)

    if fmin > fmax:
        min, max = max, min

    mid = (min + max) / 2
    fmid = f(mid)

    if abs(fmid - target) < tolerance:
         return mid

    if fmid < target:
        return search(target, f, mid, max, tolerance)
    else:
        return search(target, f, min, mid, tolerance)


r = search(16, lambda x: D(45, x), 0, 45)
print(r)
print(D(45, r))
