/**
 * Solution. Since java does not have generic array supported out of box, here
 * we just use an example with a simple primitive int array as input.
 * 
 * This is the optimal Solution with O(n^2), Θ(n) time complexity and O(1)
 * Space.
 */
public class Solution {

    public void sort(int[] data) {
        if (data == null || data.length <= 1)
            return;

        int length = data.length;
        for (int pass = 0; pass < length; pass++) {
            boolean swapped = false;
            for (int idx = 0; idx < length - pass - 1; idx++) {
                if (data[idx] > data[idx + 1]) {
                    tmp = data[idx];
                    data[idx] = data[idx + 1];
                    data[idx + 1] = tmp;
                    swapped = true;
                }
            }
            if (swapped)
                break;
        }
    }
}