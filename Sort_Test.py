# 인접한 두 원소를 비교하며 정렬, Time Complexity : O(n ** 2)
# Time Complexity : O(n**2)
def bubble_sort(input_list):
    length = len(input_list)
    for i in range(length-1):
        for j in range(length-i-1):
            # print(i, j)
            if input_list[j] > input_list[j+1]:
                input_list[j], input_list[j+1] = input_list[j+1], input_list[j]
    return input_list


# privot보다 작은 값은 앞으로, 큰 값은 뒤로 정렬
# Time Complexity : O(nlogn) / O(n**2)
def quick_sort(input_list):
    if len(input_list) <= 1:
        return input_list
    pivot = input_list[len(input_list) // 2]
    lesser_list, equal_list, greater_list = [], [], []
    for num in input_list:
        if num < pivot:
            lesser_list.append(num)
        elif num > pivot:
            greater_list.append(num)
        else:
            equal_list.append(num)
    return quick_sort(lesser_list) + equal_list + quick_sort(greater_list)


# 데이터를 계속 나눈 후, 더이상 분할이 안될 때 합병하면서 정렬
# Time Complexity : O(nlogn)
def merge_sort(input_list):
    def merge(left, right):
        result = []
        while len(left) > 0 or len(right) > 0:
            if len(left) > 0 and len(right) > 0:
                if left[0] <= right[0]:
                    result.append(left[0])
                    left = left[1:]
                else:
                    result.append(right[0])
                    right = right[1]
            elif len(left) > 0:
                result.append(left[0])
                left = left[1:]
            elif len(right) > 0:
                result.append(right[0])
                right = right[1:]
        return result

    if len(input_list) <= 1:
        return input_list
    mid = len(input_list) // 2
    left_list = input_list[:mid]
    right_list = input_list[mid:]
    left_list = merge_sort(left_list)
    right_list = merge_sort(right_list)
    return merge(left_list, right_list)


d1, d2, d3, d4, d5, d6, d7 = map(int, input("정수 : ").split())
data = [d1, d2, d3, d4, d5, d6, d7]

print(bubble_sort(data))
print(quick_sort(data))
print(merge_sort(data))



