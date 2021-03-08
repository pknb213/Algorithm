from timeit import default_timer as timer
from datetime import timedelta
from collections import deque
st = timer()
from collections import Counter

def soultion(_list):
    c = Counter(_list)
    print("C :", c)
    mv = c.most_common(1)[0]
    print("Most:", mv)
    print("len:", len(_list), "round:", round(len(_list)/2))
    if mv[1] > round(len(c))/2:
        return mv[0]
    else:
        return -1

print(soultion([2, 3, 4, 5, 9, 9, 9, 9, 9, 9, 100]))
print(timedelta(seconds=timer() - st),"\n\n")

st = timer()
def soultion2(n,r,c):
    def move(x, y, n):
        if y < (n - 1):
            return max(0, x - 1), y + 1
        return x + 1, y

    def zigzag(n):
        x, y = 0, 0
        size = n * n
        for _ in range(size):
            yield y, x
            if (x + y) & 1:
                x, y = move(x, y, n)
            else:
                y, x = move(y, x, n)

    # test code
    i, n = 1, 5
    mat = [[0 for x in range(n)] for y in range(n)]
    for (y, x) in zigzag(n):
        mat[y][x], i = i, i + 1

    from pprint import pprint
    pprint(mat)

print(soultion2(5,3,2))
print(timedelta(seconds=timer() - st),"\n\n")


# st = timer()
# def soultion3(mtx):
#     n = len(mtx)
#     dp = [[0 for _ in range(n)] for __ in range(n)]
#     print(dp)
#     for j in range(n):
#         for i in range(n):
#             if i == 0 and j == 0:
#                 dp[i][j] = 0
#             else:
#                 dp[i][j] = max()
#
#     return 1
#
# print(">>", soultion3([[1, -7, -2, 1, -1], [2, 3, 0, -1, -2], [1, -1, 6, -1, -2], [-1, 1, -2, 0, 4], [-10, 5, -3, -1, 1]]))
# print(timedelta(seconds=timer() - st),"\n\n\n")


st = timer()
from collections import deque
import re
def soultion4(str_list):
    for text in str_list:
        print(text)
        t = re.match(".gif", text)
        print(t)

print(">>", soultion4(
    ['burger.letters.com - - [01/Jul/1995:00:00:11 -0400] "GET /shuttle/countdown/liftoff.html HTTP/1.0" 304 0',
     'burger.letters.com - - [01/Jul/1995:00:00:12 -0400] "GET /images/NASA-logosmall.gif HTTP/1.0" 304 0']))



print(timedelta(seconds=timer() - st))


