import org.junit.jupiter.api.*;

/**
 * TestBubbleSort
 */
public class TestSolutionTemplate {

    Testable sol;

    @BeforeEach
    void setUp() {
        sol = new SolutionTemplate();
    }

    @Test
    void testSampleInput() {
        int[] data = new int[] {};
        int[] expected = new int[] {};
        actual = sol.method(data);
        Assertions.assertArrayEquals(expected, data);
    }

}