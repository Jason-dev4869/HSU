def knapsack(N, M, weights, values):
    # Tạo bảng lưu trữ kết quả tối ưu
    dp = [[0 for _ in range(M + 1)] for _ in range(N + 1)]

    # Xây dựng bảng dp
    for i in range(1, N + 1):
        for j in range(M + 1):
            if weights[i - 1] > j:
                dp[i][j] = dp[i - 1][j]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - weights[i - 1]] + values[i - 1])

    # Truy vết để xác định các đồ được chọn
    selected_items = []
    i, j = N, M
    while i > 0 and j > 0:
        if dp[i][j] != dp[i - 1][j]:
            selected_items.append(i)
            j -= weights[i - 1]
        i -= 1

    # Xuất kết quả
    selected_items.reverse()
    return selected_items

# Đọc input
N, M = map(int, input().split())
weights, values = [], []
for _ in range(N):
    w, v = map(int, input().split())
    weights.append(w)
    values.append(v)

# Gọi hàm và xuất kết quả
result = knapsack(N, M, weights, values)
print(*result)