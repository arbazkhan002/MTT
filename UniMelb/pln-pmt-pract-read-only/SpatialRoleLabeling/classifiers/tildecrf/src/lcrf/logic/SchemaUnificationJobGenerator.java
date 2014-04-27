/**
 * 
 */
package lcrf.logic;

import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Vector;

import lcrf.stuff.IntegerIterator;
import lcrf.stuff.IteratorChain;

/**
 * @author bgutmann
 * 
 */
public class SchemaUnificationJobGenerator implements Iterable<UnificationJob>, Iterator<UnificationJob> {
    private int maxsequencelength;

    private IntegerIterator integerIterator;

    private Iterator<Term> termIterator;

    private Term actualTerm;

    public SchemaUnificationJobGenerator(int maxsequencelength, List<TermSchema> schemata,
            List<Variable> boundedVars, int actualDepth) {
        assert schemata != null;
        assert boundedVars != null;

        this.maxsequencelength = maxsequencelength;

        List<Iterator<Term>> iterators = new Vector<Iterator<Term>>(schemata.size());
        for (TermSchema schema : schemata) {
            iterators.add(schema.iterator(boundedVars,actualDepth));
        }

        integerIterator = new IntegerIterator(maxsequencelength);
        termIterator = new IteratorChain<Term>(iterators);
        actualTerm = (termIterator.hasNext() && integerIterator.hasNext()) ? termIterator.next() : null;
    }

    public Iterator<UnificationJob> iterator() {
        return this;
    }

    public boolean hasNext() {
        return actualTerm != null;
    }

    public UnificationJob next() {
        if (actualTerm == null) {
            throw new NoSuchElementException();
        }
        UnificationJob job = new UnificationJob(integerIterator.next().intValue(), actualTerm);
        if (!integerIterator.hasNext()) {
            integerIterator.reset();
            actualTerm = (termIterator.hasNext()) ? termIterator.next() : null;
        }
        return job;
    }

    public void remove() {
        throw new UnsupportedOperationException();
    }

}
