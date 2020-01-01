from queue import Queue
from time import sleep

graph = {'A': set(['B', 'C']),
         'B': set(['A', 'D', 'E']),
         'C': set(['A', 'F']),
         'D': set(['B']),
         'E': set(['B', 'F']),
         'F': set(['C', 'E'])}


def bfs(tree, start, goal):
    # 출발하는 곳과 현재 경로
    queue = [(start, [start])]
    result = []
    print("Start Q : ", start, [start])

    print("현재 노드 | 이동 가능한 노드 | 미완성 경로 | 이동가능-경로")
    while queue:  # Q가 비어있지 않는 이상 반복
        # print(queue)
        n, path = queue.pop(0)
        print(n, tree[n], set(path), tree[n] - set(path))  # 현재 노드, 이동 가능한 노드, 미완성 경로
        if n == goal:   # 현재 노드가 골 노드와 같다면 아래 실행
            result.append(path)   # 결과에 완성된 경로 추가
        else:
            for m in tree[n] - set(path):   # 현재 노드의 다음 경로들과 미완성경로의 차집합
                queue.append((m, path + [m]))  # 큐에다가 남은 노드와 경로와 남은 노드의 다음 노드들을 경로로 추가
    return result


def line_bfs(cony, brown):
    tree = {brown: set([brown - 1, brown + 1, brown * 2])}
    t = 0
    queue = [(brown, [brown], t, cony)]
    res = []
    while queue:
        # print(tree)
        n, path, t, cony = queue.pop(0)
        print(t, cony, n, tree[n], set(path))
        if cony == n:
            res = path
            break
        elif cony < n:
            pass
        elif cony > 10000:
            res.append(-1)
            break
        else:
            for m in tree[n] - set(path):
                if m > 0:
                    tree[m] = set([m-1, m+1, 2*m])
                    queue.append((m, path + [m], t+1, cony+t+1))
        # sleep(0.1)
    return len(res) - 1


while 1:
    a, b = map(int, input("코니와 브라운의 거리를 입력하세요(공백 이용) : ").split())
    # print(bfs(graph, a, b))
    print("브라운이 코니를", line_bfs(a, b), "초 만에 잡는다")
    sleep(5)
