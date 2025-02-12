def solution(n, computers):
    answer = 0
    visited = [0 for i in range(n)]

    def dfs(computers, visited, start):
        stack = [start]
        while stack:
            j = stack.pop()
            if visited[j] == 0:
                visited[j] = 1

                for i in range(0, len(computers)):
                    if computers[j][i] == 1 and visited[i] == 0:
                        stack.append(i)
    i = 0
    while 0 in visited:
        if visited[i] == 0:
            dfs(computers, visited, i)
            answer += 1
        i += 1
    return answer

print(solution(3, [[1, 1, 0], [1, 1, 0], [0, 0, 1]]))