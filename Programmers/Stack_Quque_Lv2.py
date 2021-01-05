"""
문제 설명
초 단위로 기록된 주식가격이 담긴 배열 prices가 매개변수로 주어질 때, 가격이 떨어지지 않은 기간은 몇 초인지를 return 하도록 solution 함수를 완성하세요.

제한사항
prices의 각 가격은 1 이상 10,000 이하인 자연수입니다.
prices의 길이는 2 이상 100,000 이하입니다.

입출력 예
prices  |   return
[1, 2, 3, 2, 3] | [4, 3, 1, 1, 0]

입출력 예 설명
1초 시점의 ₩1은 끝까지 가격이 떨어지지 않았습니다.
2초 시점의 ₩2은 끝까지 가격이 떨어지지 않았습니다.
3초 시점의 ₩3은 1초뒤에 가격이 떨어집니다. 따라서 1초간 가격이 떨어지지 않은 것으로 봅니다.
4초 시점의 ₩2은 1초간 가격이 떨어지지 않았습니다.
5초 시점의 ₩3은 0초간 가격이 떨어지지 않았습니다.
"""

case = [1, 2, 3, 2, 3]
case = [10000,50000,50001,49999,99999]


def solution(prices):
    answer = []
    pop_box = [prices.pop()]
    answer.append(0)
    while prices:
        sec = 0
        a = prices.pop()
        for i in pop_box:
            if a <= i:
                sec += 1
        pop_box.append(a)
        answer.insert(0, sec)
    return answer


print(case)
print(solution(case))


# todo : 위의 솔루션에서는 모르겠지만 제대로 동작이 안한다 테스트케이스 씨발 존나 적어서 뭐가 문제인지도 모르곘네

def solution(prices):
    answer = [0] * len(prices)

    for i in range(len(prices)-1):
        for j in range(i, len(prices)-1):
            if prices[i] >prices[j]:
                break
            else:
                answer[i] +=1
    return answer
