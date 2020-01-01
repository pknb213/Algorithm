def min(a, b):
    return a if a <= b else b


# RGB를 빨,초,파
# 이웃은 같은색이 안됨 i의 이웃은 i-1, i+1
# 빨강 비용, 초록 비용, 파랑 비용이 주어질때 최소로 칠 할 수 있는 비용

# 집의 수
n = int(input())
matrix = [[0] * 3 for i in range(n)]

for i in range(n):
    # 각 색별 페인트 비용
    matrix[i][0], matrix[i][1], matrix[i][2] = map(int, input().split())

matrix2 = [[0] * 3 for i in range(n)]
print(matrix2)
for i in range(n):
    if i == 0:
        matrix2[i] = matrix[i]
    else:
        matrix2[i][0] = matrix[i][0] + min(matrix2[i - 1][1], matrix2[i - 1][2])
        matrix2[i][1] = matrix[i][1] + min(matrix2[i - 1][0], matrix2[i - 1][2])
        matrix2[i][2] = matrix[i][2] + min(matrix2[i - 1][0], matrix2[i - 1][1])

print(min(min(
    matrix2[n - 1][0], matrix2[n - 1][1]), matrix2[n - 1][2]))