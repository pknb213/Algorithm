from timeit import default_timer as timer
from datetime import timedelta
from collections import deque
st = timer()

def bfs(start, maps, visited):
    queue = deque()
    queue.append(start)
    while queue:
        y = queue.popleft()
        visited.add(y)
        for x in range(len(maps[y])):
            if maps[y][x] is True and x not in visited:
                visited.add(x)
                queue.append(x)
    return True


def get_minimum_connections(costs):
    answer = 0
    visited = set()
    for y in range(len(costs)):
        if y not in visited:
            visited.add(y)
            answer += bfs(y, costs, visited)
    print(">>", answer)

matrix = \
    [
        [False, True, False, False, True],
        [True, False, False, False, False],
        [False, False, False, True, False],
        [False, False, True, False, False],
        [True, False, False, False, False]
    ]
print(get_minimum_connections(matrix)) # should print 1

print(timedelta(seconds=timer() - st))