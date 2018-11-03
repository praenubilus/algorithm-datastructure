import org.junit.jupiter.api.*;

/**
 * TestBubbleSort
 */
public class TestQuickSortSolution {

    Testable sol;

    @BeforeEach
    void setUp() {
        sol = new QuickSortSolution();
    }

    @Test
    void testSampleInput() {
        int[] data = new int[] {};
        int[] expected = new int[] {};
        actual = sol.method(data);
        Assertions.assertArrayEquals(expected, data);
    }

}