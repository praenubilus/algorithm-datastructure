import org.junit.jupiter.api.*;

/**
 * TestBubbleSort
 */
public class BubbleSortTest {

    Testable sol;

    @BeforeEach
    void setUp() {
        sol = new SolutionOptimal();
    }

    @Test
    void testSimpleInput() {
        int[] data = new int[] { 4, 2, 1, 5, 3, 7, 0, -5 };
        int[] expected = new int[] { -5, 0, 1, 2, 3, 4, 5, 7 };
        sol.sort(data);
        Assertions.assertArrayEquals(expected, data);
    }

    @Test
    void testBestPossibleInput() {
        int[] data = new int[] { -5, 0, 1, 2, 3, 4, 5, 7 };
        int[] expected = new int[] { -5, 0, 1, 2, 3, 4, 5, 7 };
        sol.sort(data);
        Assertions.assertArrayEquals(expected, data);
    }
}