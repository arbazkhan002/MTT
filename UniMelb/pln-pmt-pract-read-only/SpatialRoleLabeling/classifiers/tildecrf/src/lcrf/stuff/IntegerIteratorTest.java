package lcrf.stuff;

import junit.framework.TestCase;

public class IntegerIteratorTest extends TestCase {
    public void test1() {
        IntegerIterator it1 = new IntegerIterator(5);
        assertTrue(it1.hasNext());
        assertEquals(0, it1.next().intValue());
        assertTrue(it1.hasNext());
        assertEquals(1, it1.next().intValue());
        assertTrue(it1.hasNext());
        assertEquals(2, it1.next().intValue());
        assertTrue(it1.hasNext());
        assertEquals(3, it1.next().intValue());
        assertTrue(it1.hasNext());
        assertEquals(4, it1.next().intValue());
        assertFalse(it1.hasNext());
        it1.reset();
        assertTrue(it1.hasNext());
        assertEquals(0, it1.next().intValue());
        assertTrue(it1.hasNext());
        assertEquals(1, it1.next().intValue());
        assertTrue(it1.hasNext());
        assertEquals(2, it1.next().intValue());
        assertTrue(it1.hasNext());
        assertEquals(3, it1.next().intValue());
        assertTrue(it1.hasNext());
        assertEquals(4, it1.next().intValue());
        assertFalse(it1.hasNext());
    }

    public void test2() {
        IntegerIterator it1 = new IntegerIterator(-1, 1);
        assertTrue(it1.hasNext());
        assertEquals(-1, it1.next().intValue());
        assertTrue(it1.hasNext());
        assertEquals(0, it1.next().intValue());
        assertFalse(it1.hasNext());
        it1.reset();
        assertTrue(it1.hasNext());
        assertEquals(-1, it1.next().intValue());
        assertTrue(it1.hasNext());
        assertEquals(0, it1.next().intValue());
        assertFalse(it1.hasNext());
    }

    public void test3() {
        IntegerIterator it1 = new IntegerIterator(-1);
        assertFalse(it1.hasNext());
        it1.reset();
        assertFalse(it1.hasNext());
    }

}
