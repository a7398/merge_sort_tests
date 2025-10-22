import unittest

# функция сортировки слиянием
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# тесты
class TestMergeSort(unittest.TestCase):

    def test_empty_list(self):
        self.assertEqual(merge_sort([]), [])

    def test_single_element(self):
        self.assertEqual(merge_sort([1]), [1])

    def test_unsorted_list(self):
        arr = [4, 2, 5, 1, 3]
        self.assertEqual(merge_sort(arr), sorted(arr))

    def test_duplicates(self):
        arr = [3, 1, 2, 3, 1]
        self.assertEqual(merge_sort(arr), sorted(arr))

if __name__ == '__main__':
    unittest.main()
