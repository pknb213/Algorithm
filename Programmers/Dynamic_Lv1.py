"""
0-1 Knapsack Problem (Fractional Knapsack 문제는 자를수 있는 개념)
배낭 문제는 무게 제한이 50인 배낭에 다음과 같은 세 개의 물건을 넣는 문제입니다.
넣은 물건들의 가치(v) 합이 최대가 되면 됩니다.
문제는 세 물건의 무게(w)를 합치면 60이라 다 넣지는 못한다는 겁니다.
이 문제 이름이 0/1인 이유는 물건을 쪼개서 넣지는 못하고,
선택지가 통째로 넣거나 아예 안 넣거나 두 개밖에 없기 때문입니다.

물건의 가치와 무게로 나타낸다.
1 : 60가치, 10kg   2 : 100가치, 20kg   3 : 120가치, 30kg
"""
item = [[1, 6, 1], [2, 10, 2], [3, 12, 3], [4, 5, 4], [5, 30, 5]]
limit_weight = 5
"""
i / w | 0 | 1 | 2 | 3 | 4 | 5
0     | 0 | 0 | 0 | 0 | 0 | 0
1     | 0 | 6 | 6 | 6 | 6 | 6
2     | 0 | 6 |10 |16 |16 |16
3     | 0 | 6 |10 |16 |18 |22   
"""


def sol(_item, cap):
    print(_item)
    mem = [[0 for x in range(cap + 1)] for x in range(len(item) + 1)]
    print(mem)
    # 보석을 안뽑는 0의 경우 부터 보석의 수까지 len(_item) + 1 (안뽑는 경우때문에 1케이스 늠)
    for i in range(len(_item) + 1):
        print(i, "|", end=" ")
        # 무게를 0부터 제한조건 까지 모든 케이스, 루프 무게가 0인 케이스도 해서 + 1 늠
        for j in range(cap + 1):
            # 보석 없이 또는 제한이 0일땐 아무것도 못하므로 0으로 채운다.
            if i == 0 or j == 0:
                mem[i][j] = 0
                print(0, end=" | ")
            # 무게가 제한 보다 작거나 같을 경우 실행, 전에 있던 가치와 이번의 가치를 합산한 것과 전의 가치 중 큰 것 선택
            elif _item[i-1][2] <= j:
                mem[i][j] = max(_item[i-1][1] + mem[i-1][j-_item[i-1][2]], mem[i-1][j])
                print(mem[i][j], end=" | ")
            #
            else:
                mem[i][j] = mem[i-1][j]
                print(mem[i][j], end=" || ")
        print("\n", end="")
    print(mem)
    return mem[i][j]


print(sol(item, limit_weight))
