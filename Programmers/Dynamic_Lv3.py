"""
아래와 같이 5와 사칙연산만으로 12를 표현할 수 있습니다.

12 = 5 + 5 + (5 / 5) + (5 / 5)
12 = 55 / 5 + 5 / 5
12 = (55 + 5) / 5

5를 사용한 횟수는 각각 6,5,4 입니다. 그리고 이중 가장 작은 경우는 4입니다.
이처럼 숫자 N과 number가 주어질 때, N과 사칙연산만 사용해서 표현 할 수 있는 방법 중 N 사용횟수의 최솟값을 return 하도록 solution 함수를 작성하세요.

제한사항
N은 1 이상 9 이하입니다.
number는 1 이상 32,000 이하입니다.
수식에는 괄호와 사칙연산만 가능하며 나누기 연산에서 나머지는 무시합니다.
최솟값이 8보다 크면 -1을 return 합니다.
입출력 예
N	number	return
5	12	4
2	11	3
입출력 예 설명
예제 #1
문제에 나온 예와 같습니다.

예제 #2
11 = 22 / 2와 같이 2를 3번만 사용하여 표현할 수 있습니다.
"""


def solution(N, number):
    answer = 0
    # 연산자는 +, -, /, * 4개, 괄호 사용, NN과 같이 붙이기 가능
    # NN은 N*N 보다 항상 크다. 1000*1000 = 1000,000이고 10,001,000이다.
    # 내 생각은 N으로 만들수있는 작은 수의 최소 값를 다이나믹 저장하고 가장 크게 만드는 방법중 하나로 풀기보기?
    # ( N / N ) = 1,  ( N + N ) / N = 2, (N + N + N) / N = 3
    # NN / N = ? , 88 / 8 = 11, 1010 / 10 = 101, 2424 / 24 = 101, 99 / 9 = 11, 100100 / 100 = 1001
    # 10011001 / 1001 = 10001
    # (NN + N) / N =?, (44 + 4) / 4 => 48 / 4 = 12, (88 + 8) / 8 => 96 / 8 = 12, (1010 + 10) / 10 => 1020 / 10 = 102
    # ex) N = 11, num = 24000 => 111111 / 11
    dic = {}
    for i in range(4, 0, -1):
        n = int(str(N)*i)
        dic[n] = i
        # print(n)
        if n > number:
            continue
        for j in range(2, 9):
            if n*j > number:
                continue
            else:
                dic[n*j] = dic[n] + j
                print(n*j)
        print(dic)

    return answer


def solution2(N, number):
    S = [{N}]
    print(S, type(S), type(S[0]))
    for i in range(2, 9):
        print("> i : ", i)
        lst = [int(str(N) * i)]
        print("lst : ", lst)
        for X_i in range(0, int(i / 2)):
            print(">> Loop : ", 0, "~", int(i/2))
            for x in S[X_i]:
                print(">>> Loop : ", S[X_i])
                for y in S[i - X_i - 2]:
                    print(">>>> y : ", y)
                    lst.append(x + y)
                    lst.append(x - y)
                    lst.append(y - x)
                    lst.append(x * y)
                    if x != 0: lst.append(y // x)
                    if y != 0: lst.append(x // y)
        if number in set(lst):
            return i
        S.append(lst)
        print(S)
    return -1

test_case = [5, 12]
# print(solution(test_case[0], test_case[1]))
print(solution2(test_case[0], test_case[1]))

