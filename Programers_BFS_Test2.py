def solution2(ticks):
    answer = []
    print(ticks, len(ticks))
    temPath = []
    for i in range(len(ticks)):
        if "ICN" in ticks[i][0]:
            # print(ticks[i])
            temPath.append(ticks[i][1])
    tree = {'ICN': set(temPath)}
    print("Tree : ", tree)
    queue = [("ICN", ['ICN'])]
    while queue:
        n, path = queue.pop(0)
        print("POP : ", n, path, tree[n], tree[n] - set(path))
        for m in tree[n]:
            print(">>", m)
            temPath.clear()
            for i in range(len(ticks)):
                if m in ticks[i][0]:
                    temPath.append(ticks[i][1])
                else:
                    pass
            if len(temPath):
                tree[m] = set(temPath)
            if len(path) > len(ticks):
                break
            elif len(path) == len(ticks):
                return answer.append(path)

            queue.append((m, path + [m]))

    return answer


def solution(tickets):
    routes = {}

    for t in tickets:
        routes[t[0]] = routes.get(t[0], []) + [t[1]]
    print(routes)
    for r in routes:
        routes[r].sort(reverse=True)
    print("Sorted: ", routes)
    stack = ['ICN']
    path = []
    while stack:
        top = stack[-1]
        print(top, stack, path)
        if top not in routes or len(routes[top]) == 0:
            path.append(stack.pop())
        else:
            stack.append(routes[top][-1])
            routes[top] = routes[top][:-1]

    return path[::-1]


print(solution([["ICN", "SFO"], ["ICN", "ATL"], ["SFO", "ATL"], ["ATL", "ICN"], ["ATL", "SFO"]]))