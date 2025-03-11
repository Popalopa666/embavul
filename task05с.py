def max_subarray_sum(nums, k):
    max_sum = float('-inf')

    for i in range(len(nums)):
        current_sum = 0

        for j in range(i, min(i + k, len(nums))):
            current_sum += nums[j]
            if current_sum > max_sum:
                max_sum = current_sum

    return max_sum

nums = [1, 3, -1, -3, 5, 4, 6, 8]
k = 1
print(max_subarray_sum(nums, k))
