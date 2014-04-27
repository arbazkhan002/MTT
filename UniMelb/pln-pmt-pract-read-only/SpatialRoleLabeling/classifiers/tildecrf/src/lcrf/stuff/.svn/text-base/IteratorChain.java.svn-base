/**
 * 
 */
package lcrf.stuff;

import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;

/**
 * @author bgutmann
 * 
 */
public class IteratorChain<T> implements Iterator<T> {
    private int actualiterator;

    private List<Iterator<T>> iterators;

    public IteratorChain(List<Iterator<T>> iterators) {
        assert iterators != null;

        this.iterators = iterators;
        actualiterator = 0;
        while (actualiterator < iterators.size() && !iterators.get(actualiterator).hasNext()) {
            actualiterator++;
        }
    }

    public boolean hasNext() {
        return actualiterator < iterators.size();
    }

    public T next() {
        if (actualiterator >= iterators.size()) {
            throw new NoSuchElementException();
        }
        T result = iterators.get(actualiterator).next();
        while (actualiterator < iterators.size() && !iterators.get(actualiterator).hasNext()) {
            actualiterator++;
        }
        return result;
    }

    public void remove() {
        throw new UnsupportedOperationException();
    }

}
