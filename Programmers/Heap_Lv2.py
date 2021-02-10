"""
매운 것을 좋아하는 Leo는 모든 음식의 스코빌 지수를 K 이상으로 만들고 싶습니다. 모든 음식의 스코빌 지수를 K 이상으로 만들기 위해 Leo는 스코빌 지수가 가장 낮은 두 개의 음식을 아래와 같이 특별한 방법으로 섞어 새로운 음식을 만듭니다.

섞은 음식의 스코빌 지수 = 가장 맵지 않은 음식의 스코빌 지수 + (두 번째로 맵지 않은 음식의 스코빌 지수 * 2)
Leo는 모든 음식의 스코빌 지수가 K 이상이 될 때까지 반복하여 섞습니다.
Leo가 가진 음식의 스코빌 지수를 담은 배열 scoville과 원하는 스코빌 지수 K가 주어질 때, 모든 음식의 스코빌 지수를 K 이상으로 만들기 위해 섞어야 하는 최소 횟수를 return 하도록 solution 함수를 작성해주세요.

제한 사항
scoville의 길이는 2 이상 1,000,000 이하입니다.
K는 0 이상 1,000,000,000 이하입니다.
scoville의 원소는 각각 0 이상 1,000,000 이하입니다.
모든 음식의 스코빌 지수를 K 이상으로 만들 수 없는 경우에는 -1을 return 합니다.
입출력 예
scoville	K	return
[1, 2, 3, 9, 10, 12]	7	2
입출력 예 설명
스코빌 지수가 1인 음식과 2인 음식을 섞으면 음식의 스코빌 지수가 아래와 같이 됩니다.
새로운 음식의 스코빌 지수 = 1 + (2 * 2) = 5
가진 음식의 스코빌 지수 = [5, 3, 9, 10, 12]

스코빌 지수가 3인 음식과 5인 음식을 섞으면 음식의 스코빌 지수가 아래와 같이 됩니다.
새로운 음식의 스코빌 지수 = 3 + (5 * 2) = 13
가진 음식의 스코빌 지수 = [13, 9, 10, 12]

모든 음식의 스코빌 지수가 7 이상이 되었고 이때 섞은 횟수는 2회입니다.
"""


def solution(S, K):
    answer = 0
    print(S, K)
    def scoville_gen(_S):
        # for _ in _S:
        #     yield _
        yield from _S

    mix = []
    clr = []
    for s in scoville_gen(S):
        print(s)
        if s < K:
            mix.append(s)
        else:
            clr.append(s)
        if len(mix) == 2:
            print(">>> CNT + 1 :", answer)
            answer += 1
            mix_s = mix.pop(0) + mix.pop()*2
            print(">>", mix_s)
            if mix_s > K:
                pass
            else:
                mix.append(mix_s)
    if len(mix) > 0:
        while len(clr) and len(mix):
            print(">>>> CNT + 1:", answer)
            answer += 1
            clr_s = mix.pop(0) + clr.pop(0)*2
            print(">>", clr_s)
            if clr_s > K:
                pass
            else:
                mix.append(clr_s)
        if len(mix) > 0:
            return -1
    return answer


scoville = [1,2,3,9,10,12]
k = 7
# scoville = [8242, 745, 9876, 115, 3225425, 1151, 211551]
# k = 1000000

print(solution(scoville, k))


def soultion2(S, K):
    answer = 0
    while len(S):
        left_s = S.pop(0)
        print(">", left_s)
        if left_s > K:
            continue
        compare_s = S.pop(0)

    return answer


print(soultion2(scoville, k))
