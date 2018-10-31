class Solution:
    """In place naive bubble sort
       With O(n^2) time complexity and O(1) Space.
    """

    def sort(self, data, reverse=False):
        if data is None or len(data) <= 1:
            return
        length = len(data)
        for pass_ in range(0, length):
            for idx in range(0, length-pass_-1):
                if data[idx] > data[idx+1]:
                    # incorrect order, swap
                    data[idx], data[idx+1] = data[idx+1], data[idx]

        
