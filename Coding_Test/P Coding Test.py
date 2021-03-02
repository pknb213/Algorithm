from timeit import default_timer as timer
from datetime import timedelta
from collections import Counter


def flip(ch):
    return '1' if (ch == '0') else '0'


def getFlipWithStartingCharcter(_str, expected):
    flipCount = 0
    for i in range(len(_str)):
        if (_str[i] != expected):
            flipCount += 1
        expected = flip(expected)
    return flipCount


def minFlipToMakeStringAlternate(_str):
    return min(getFlipWithStartingCharcter(_str, '0'),
               getFlipWithStartingCharcter(_str, '1'))


def solution(data):
    data = map(lambda x: str(x), data)
    res = "".join(data)
    # print(res)
    return min(getFlipWithStartingCharcter(res, '0'),
               getFlipWithStartingCharcter(res, '1'))


in_data = [1,1,0,1,1]
st = timer()
print(solution(in_data))
print(">>", timedelta(seconds=timer() - st))


def solution2(arr):
    # write your code in Python 3.6
    maxOn = 0
    momentCount = 0

    for pos, bulb in enumerate(arr):
        maxOn = max(maxOn, bulb)
        if maxOn == pos+1:
            momentCount += 1
    return momentCount


in_data = [2,1,3,5,4]
st = timer()
print(solution2(in_data))
print(">>", timedelta(seconds=timer() - st))

from collections import Counter


def solution3(arr):
    c = Counter(arr)
    if len(c) == 1:
        return -1
    hashMap = {}
    n = len(arr)
    res = 0
    sum1 = 0
    for i in range(n):
        sum1 += arr[i]

        if sum1 == 0:
            res += 1

        al = []
        if sum1 in hashMap:
            al = hashMap.get(sum1)
            res += len(al)
        al.append(i)
        hashMap[sum1] = al
    return res


in_data = [2,-2,3,0,4,-7]
st = timer()
print(solution3(in_data))
print(">>", timedelta(seconds=timer() - st))