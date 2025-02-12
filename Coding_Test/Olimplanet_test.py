"""
1. Syntax Checker (Required)
괄호가 올바르게 쓰였는지 확인하는 로직을 만들려고 합니다.
괄호는 대괄호, 중괄호, 소괄호 세가지가 있으며
주어지는 스트링이 괄호가 올바르게 사용되었으며 true, 아니면 false를 리턴하는 함수를 작성하세요.
예시:
input	output
[[(){}]]	true
(()))	false
)(())[]{}	false
({[}])	false
[{(([{[]}]))}]	true
"""
import sys
from datetime import timedelta
from timeit import default_timer as timer
sys.setrecursionlimit(8000)


def Soultion(_str):
    from collections import deque
    _str = deque(_str)
    st = []
    while _str:
        _s = _str.popleft()
        if _s in [']', '}', ')'] and len(st):
            if (_s == ']' and st.pop() == '[') or (_s == '}' and st.pop() == '{') or (_s == ')' and st.pop() == '('):
                pass
            else:
                return False
        else:
            st.append(_s)
        # print(st, " - ", _str)
    if not len(st):
        return True
    return False


Syntext = "[{(([{[]}]))}]"
st = timer()
print("1 >>", Soultion(Syntext))
print(timedelta(seconds=timer() - st))
"""
2. Raccoon (Required)
너구리 한 쌍은 한 달 후에 다른 새끼 너구리 한 쌍을 낳습니다. 
이 새끼 너구리 한 쌍은 한 달 동안 성체가 되며 
성체가 된 너구리 한 쌍은 다시 한 달 후에 다른 새끼 너구리 한 쌍을 낳습니다. 
이미 성체가 된 너구리 부부는 달마다 새끼 너구리를 한 쌍씩 낳는다고 가정할 때, 
n달 후의 너구리 수를 구하는 함수를 작성하세요. (단, 이 너구리들은 죽지 않습니다.)
예시:
input(n달후)	output(마리 수)
0	2
1	4
2   6 (새끼 한쌍 크는 중)
3   10 (새끼 두쌍 크는중)
4	16
"""
def Soultion(_int):
    # F0 = 2, F1 = 4, Fn+2 = Fn + Fn+1
    # Todo : DP로 결과 값을 가지고 있으면 더욱 메모리 효율성이 좋아짐
    class Deco:
        def __init__(self, func):
            self.function = func
            self.cache = {}

        def __call__(self, *args):
            if args not in self.cache:
                self.cache[args] = self.function(*args)
            return self.cache[args]

    @Deco
    def pibonachi(i):
        res = 2 if i == 0 else 4 if i == 1 else pibonachi(i-1) + pibonachi(i-2)
        # print(i, ":", res)
        return res
    return pibonachi(_int)


Month = 8
st = timer()
print("\n2 >> ", Soultion(Month))
print(timedelta(seconds=timer() - st), "\n")
"""
3. 집뷰가 필요한 이유 (Optional)
오프라인 매장이 문을 닫아서 상담원들은 직접 고객을 만나러 각지를 방문해야 하는 상황이 되었습니다. 
이들이 최소한의 이동시간으로 고객을 만날 수 있도록 최소 이동시간을 구하는 함수를 작성하세요. 
입력은 고객 수만큼의 방문지 리스트가 주어지며, 
각 방문지에서는 다른 방문지로 이동할 시에 소요되는 이동시간이 다시 리스트로 주어집니다. 
(단, 방문지의 수는 10명 미만으로 주어집니다) 
예시: [ [0, 611, 648], [611, 0, 743], [648, 743, 0] ]
정답: 1259

[ [0, 326, 503, 290], [326, 0, 225, 395], [503, 225, 0, 620], [290, 395, 620, 0] ]
정답: 841
"""
def Soultion(_graph):
    from itertools import permutations
    cases = list(permutations([i for i in range(len(_graph))], len(_graph)))
    costs = {}
    for c in cases:
        start = c[0]
        cost = 0
        for i in range(len(c) - 1):
            cost += _graph[c[i]][c[i+1]]
        if start in costs:
            if costs[start] > cost:
                costs[start] = cost
        else:
            costs[start] = cost
    #     print(cost)
    # print(costs)
    return min(costs.values())


HomeList = [[0, 326, 503, 290], [326, 0, 225, 395], [503, 225, 0, 620], [290, 395, 620, 0]]
st = timer()
print("\n3 >>", Soultion(HomeList))
print(timedelta(seconds=timer() - st))






