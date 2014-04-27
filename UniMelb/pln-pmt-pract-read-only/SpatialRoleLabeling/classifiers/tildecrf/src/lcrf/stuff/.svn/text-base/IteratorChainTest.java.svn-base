package lcrf.stuff;

import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Vector;

import junit.framework.TestCase;

public class IteratorChainTest extends TestCase {
    public void testWithNoIterators() {
        List<Iterator<Integer>> iterators = new Vector<Iterator<Integer>>();

        IteratorChain<Integer> chain = new IteratorChain<Integer>(iterators);
        assertFalse(chain.hasNext());
        try {
            chain.next();
            fail("No Exception was thrown");
        } catch (NoSuchElementException e) {
            // everything is fine
        }
    }

    public void testWithOneEmptyIterators() {
        List<Iterator<Integer>> iterators = new Vector<Iterator<Integer>>();
        iterators.add(new IntegerIterator(0, -1));

        IteratorChain<Integer> chain = new IteratorChain<Integer>(iterators);

        assertFalse(chain.hasNext());
        try {
            chain.next();
            fail("No Exception was thrown");
        } catch (NoSuchElementException e) {
            // everything is fine
        }
    }

    public void testWithOneFilledIterators() {
        List<Iterator<Integer>> iterators = new Vector<Iterator<Integer>>();
        iterators.add(new IntegerIterator(0, 1));

        IteratorChain<Integer> chain = new IteratorChain<Integer>(iterators);
        assertTrue(chain.hasNext());
        assertEquals(0, chain.next().intValue());
        assertFalse(chain.hasNext());
        assertFalse(chain.hasNext());
        try {
            chain.next();
            fail("No Exception was thrown");
        } catch (NoSuchElementException e) {
            // everything is fine
        }
    }

    public void testWithServeralIterators() {
        List<Iterator<Integer>> iterators = new Vector<Iterator<Integer>>();
        iterators.add(new IntegerIterator(0, 1));
        iterators.add(new IntegerIterator(1, 3));
        iterators.add(new IntegerIterator(3, 2));
        iterators.add(new IntegerIterator(5, 7));
        iterators.add(new IntegerIterator(7, 6));

        IteratorChain<Integer> chain = new IteratorChain<Integer>(iterators);
        assertTrue(chain.hasNext());
        assertEquals(0, chain.next().intValue());
        assertTrue(chain.hasNext());
        assertEquals(1, chain.next().intValue());
        assertTrue(chain.hasNext());
        assertEquals(2, chain.next().intValue());
        assertTrue(chain.hasNext());
        assertEquals(5, chain.next().intValue());
        assertTrue(chain.hasNext());
        assertEquals(6, chain.next().intValue());
        assertFalse(chain.hasNext());
        try {
            chain.next();
            fail("No Exception was thrown");
        } catch (NoSuchElementException e) {
            // everything is fine
        }

    }

}
