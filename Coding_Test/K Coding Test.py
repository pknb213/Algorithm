from datetime import timedelta
from timeit import default_timer as timer
import random


def solution(nums):
    tp = tuple((i, bin(i).count('1')) for i in nums if '1' in bin(i))
    print(tp)
    print(sorted(tp, key=lambda x: x[1]))
    # a = sorted(sorted(dic.items(), key=lambda x: x[1]))
    # print(a)
    # return [key for (key, value) in sorted(dic.items(), key=lambda x: (x[1], x[0]))]
    return [i[0] for i in sorted(tp, key=lambda x: (x[1], x[0]))]


st = timer()
# [random.randint(1, 1e9) for i in range(10000000)], [1, 2, 3, 4, 5, 6], [1563164, 231315, 321354, 7841351],
parms = [[65, 33792, 82, 526344, 622592, 324, 324]]
for i in parms:
    print(">", solution(i))
    print(timedelta(seconds=timer() - st))
print("ALL:", timedelta(seconds=timer() - st))

"""

"""

a = [(1, 2), (2, 1), (3, 3), (1, 2), (3, 2)]
print(a)
print(sorted(a, key=lambda x: (x[1], x[0])))
