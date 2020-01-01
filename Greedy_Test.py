def greedy(n, lost, reserve):
    answer = 0
    res = [1 for i in range(n)]
    print("도둑맞기전 : ", res)
    for i in lost:
        res[i-1] -= 1
    print("도둑맞은 후 : ", res)
    for i in reserve:
        res[i-1] += 1
    print("예비복 꺼낸 후 :", res)

    for i in range(n):
        if res[i] == 0:
            if i != 0 and res[i-1] > 1:
                res[i-1] -= 1
                res[i] += 1
            elif i+1 != n and res[i+1] > 1:
                res[i+1] -= 1
                res[i] += 1
    print(res)

    while res:
        r = res.pop()
        if r > 0:
            answer += 1
    return answer


print(greedy(5, [2,4], [1,3,5]))
print(greedy(10, [4,8,9,10], [1,3,5,6]))
print(greedy(5, [1,5], [2,4]))




