class Solution:
    """
        O(Nlog N) time complexity, O(N) Space.
        Recursion based divide and conquer
    """

    def sort(self, data: list):
        # check terminate condition
        if data is None or len(data) <= 1:
            return

        # divide to two parts
        length = len(data)
        mid = length//2
        left = data[:mid]
        right = data[mid:]

        self.sort(left)
        self.sort(right)

        i_left, i_right, i_data = 0, 0, 0
        # conquer, merge them together
        while i_left < len(left) and i_right < len(right):
            if left[i_left] < right[i_right]:
                data[i_data] = left[i_left]
                i_left += 1
            else:
                data[i_data] = right[i_right]
                i_right += 1
            i_data += 1

        # after comparison for two parts, the part with remaining values will
        # be the rest of the data set
        if i_left < len(left):
            data[i_data:] = left[i_left:]
        if i_right < len(right):
            data[i_data:] = right[i_right:]
