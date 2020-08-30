from collections import deque
from queue import Queue

def solution2(n, computers):
    answer = 0
    visited = [0 for i in range(n)]
    def dfs(computers, visited, start):
        stack = [start]
        while stack:
            j = stack.pop()
            if visited[j] == 0:
                visited[j] = 1
            # for i in range(len(computers)-1, -1, -1):
            for i in range(0, len(computers)):
                if computers[j][i] ==1 and visited[i] == 0:
                    stack.append(i)
    i=0
    while 0 in visited:
        if visited[i] ==0:
            dfs(computers, visited, i)
            answer +=1
        i+=1
    return answer


def solution3(n, computers):
    answer = 0
    bfs = [] # 탐색 큐
    visited = [0] * n # 방문한 노드 체크할 리스트
    print("노드 수  -  간선 노드  -  빈 방문 리스트")
    print(n, " - ", computers, " - ", visited)

    while 0 in visited:
        bfs.append(visited.index(0))  # 0이 있는 위치 값 반환
        print(">>  시작노드, 방문 리스트, 0이 있는 위치")
        print(">>", bfs, visited, visited.index(0))
        while bfs:
            node = bfs.pop(0)
            visited[node] = 1  # 시작 노드 방문 표시
            print("시작 노드 방문 :", visited)
            for i in range(n):  # 그리고 나서 모든 노드의 인접 확인
                print(">>>> i번째 순환, 방문 확인, 인접 노드 확인")
                print(">>>>", i, visited[i], computers[node][i])
                if visited[i] == 0 and computers[node][i] == 1:  # 방문한적 없는 노드이고, 이웃 노드일때
                    bfs.append(i)
        print("탐색 끝, 네트워크 1개 추가 ")
        answer += 1
    return answer


def solution(n, computers):
    answer = 0
    visited = [0 for i in range(n)]
    print(visited)
    def dfs(node, visited, start):
        print(node, " | ", visited, " | ", start)
        stack = [start]
        while stack:
            print(">>>>>", stack)
            j = stack.pop()
            if visited[j] == 0:
                visited[j] = 1
            for i in range(len(node)):
                if node[j][i] == 1 and visited[i] == 0:
                    stack.append(i)

    i = 0
    while 0 in visited:
        print(">>", visited)
        if visited[i] == 0:
            dfs(computers, visited, i)
            answer += 1
        i += 1

    return answer


data = [[1, 0, 0, 1, 0, 0], [0, 1, 0, 1, 0, 1], [1, 0, 0, 1, 0, 1], [1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 1, 0]]
data2 = [[1, 1, 0], [1, 1, 1], [0, 1, 1]]

print(solution3(6, data))
# print(solution(3, data2))