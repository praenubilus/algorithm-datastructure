class Solution:
    """
        O() time complexity, O() Space.
    """

    def sort(self, data: list):
        self.quick_sort(data, 0, len(data)-1)

    def quick_sort(self, data, start, end):
        if start >= end:
            return

        left, right = start, end
        # decide a pivot, here we use the middle element
        pivot = data[(start+end)//2]

        # left elem <= end elem, keep comparing
        while left <= right:
            # skipt the left side elems which are less than pivot
            while left <= right and data[left] < pivot:
                left += 1
            # skipt the right side elems which are greater than pivot
            while left <= right and data[right] > pivot:
                right -= 1

            if left <= right:
                data[left], data[right] = data[right], data[left]
                left += 1
                right -= 1

        self.quick_sort(data, start, right)
        self.quick_sort(data, left, end)
