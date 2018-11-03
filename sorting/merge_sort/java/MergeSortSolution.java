/**
 * O() time complexity, O() Space.
 */
public class MergeSortSolution implements Testable {

    @Override
    public void sort(int[] data) {
        if (data == null || data.length <= 1)
            return;
        int length = data.length;
        int mid = length / 2;
        int[] left = new int[mid];
        int[] right = new int[length - mid];
        for (int i = 0; i < length; i++) {
            if (i < mid) {
                left[i] = data[i];
            } else {
                right[i - mid] = data[i];
            }
        }

        sort(left);
        sort(right);

        int iLeft = 0, iRight = 0, iData = 0;
        for (; iLeft < left.length && iRight < right.length; iData++) {
            if (left[iLeft] < right[iRight]) {
                data[iData] = left[iLeft];
                iLeft++;
            } else {
                data[iData] = right[iRight];
                iRight++;
            }
        }

        while (iLeft < left.length) {
            data[iData++] = left[iLeft++];
        }
        while (iRight < right.length) {
            data[iData++] = right[iRight++];
        }
    }

}