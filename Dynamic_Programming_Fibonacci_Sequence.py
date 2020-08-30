import time

memo = {0: 0, 1: 1}
i = j = 0


def recursion(n):
    global i
    i += 1
    if n == 0:
        return 0
    elif n == 1:
        return 1
    return recursion(n - 1) + recursion(n - 2)


def dynamicP(n):
    global j
    j += 1
    if n in memo:
        return memo[n]
    memo[n] = dynamicP(n-1) + dynamicP(n-2)
    return memo[n]


num = int(input('Input Int :  '))

print("Input Number : ", num)
start_time = time.time()
print("Fibonacci Recursion (%d) : %.0f | %d번 수행" % (num, int(recursion(num)), i))
end_time = time.time()
print("수행 시간 : %0.6f 초" % (end_time - start_time))
start_time2 = time.time()
print("Fibonacci DynamicP (%d) : %.0f | %d번 수행" % (num, dynamicP(num), j))
end_time2 = time.time()
print("수행 시간 : %.6f 초" % (end_time2 - start_time2))

