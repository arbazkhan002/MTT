/**
 * 
 */
package lcrf.stuff;

import java.util.Iterator;
import java.util.NoSuchElementException;

/**
 * @author bgutmann
 * 
 */
public class IntegerIterator implements Iterator<Integer> {
    private int next;

    private int mininclusive;

    private int maxexclusive;

    public IntegerIterator(int maxexclusive) {
        this(0, maxexclusive);
    }

    public IntegerIterator(int mininclusive, int maxexclusive) {
        next = mininclusive;
        this.mininclusive = mininclusive;
        this.maxexclusive = maxexclusive;
    }

    public boolean hasNext() {
        return next < maxexclusive;
    }

    public Integer next() {
        if (next < maxexclusive) {
            Integer result = new Integer(next);
            next++;
            return result;
        }
        throw new NoSuchElementException();
    }

    public void pushBack() {
        if (next == mininclusive)
            throw new IllegalStateException("Next was never called before.");
        next--;
    }

    public void remove() {
        throw new UnsupportedOperationException();
    }

    public void reset() {
        next = mininclusive;
    }
}
