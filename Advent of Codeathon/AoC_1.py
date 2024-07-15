def find_increasing_subsequences(nums):
    result = []
    current_subsequence = []

    for i in range(len(nums)):
        if i == 0 or nums[i] > nums[i - 1]:
            current_subsequence.append(nums[i])
        else:
            if len(current_subsequence) > 1:
                result.append(current_subsequence.copy())
            current_subsequence = [nums[i]]

    if len(current_subsequence) > 1:
        result.append(current_subsequence.copy())

    return result

def main():
    # Nhập dữ liệu từ người dùng
    n = int(input())
    sequence = list(map(int, input().split()))

    # Tìm các chuỗi con tăng
    increasing_subsequences = find_increasing_subsequences(sequence)

    # In kết quả
    for subsequence in increasing_subsequences:
        print(" ".join(map(str, subsequence)))

if __name__ == "__main__":
    main()