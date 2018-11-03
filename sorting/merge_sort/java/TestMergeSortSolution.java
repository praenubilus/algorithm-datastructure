import org.junit.jupiter.api.*;

/**
 * TestBubbleSort
 */
public class TestMergeSortSolution {

    Testable sol;

    @BeforeEach
    void setUp() {
        sol = new MergeSortSolution();
    }

    @Test
    void testSampleInput() {
        int[] data = { 4, 2, 1, 5, 3, 7, 0, -5 };
        int[] expected = { -5, 0, 1, 2, 3, 4, 5, 7 };
        sol.sort(data);
        Assertions.assertArrayEquals(expected, data);
    }

    @Test
    void testBestPossibleInput() {
        int[] data = { -5, 0, 1, 2, 3, 4, 5, 7 };
        int[] expected = { -5, 0, 1, 2, 3, 4, 5, 7 };
        sol.sort(data);
        Assertions.assertArrayEquals(expected, data);
    }

}