class Solution:
    """In place naive bubble sort
       With O(n^2) and Θ(n) time complexity and O(1) Space. 
       Optimal solution having a swap check flag, which will check whether
       the swap happened. If no swap happened after a certain pass, that 
       means the data is already in order. Then terminate the following passes.
       The Θ(n) time happened if the given data collection is already in order
    """

    def sort(self, data, reverse=False):
        if data is None or len(data) <= 1:
            return
        length = len(data)
        for pass_ in range(0, length):
            swapped = False
            for idx in range(0, length-pass_-1):
                if data[idx] > data[idx+1]:
                    # incorrect order, swap
                    data[idx], data[idx+1] = data[idx+1], data[idx]
                    swapped = True
            # end of pair-wise swapping
            # after first pass, if not swapped, that means the data is already in order
            if not swapped:
                break
