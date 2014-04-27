/**
 * 
 */
package lcrf.logic;

import java.util.Iterator;
import java.util.List;
import java.util.Vector;

import lcrf.stuff.IteratorChain;

/**
 * @author bgutmann
 * 
 */
public class InterpretationSchemaUnificationJobGenerator implements Iterable<Atom>, Iterator<Atom> {       

    private Iterator<Term> termIterator;

    private Atom actualTerm;

    public InterpretationSchemaUnificationJobGenerator(List<TermSchema> schemata,
            List<Variable> boundedVars, int actualDepth) {
        assert schemata != null;
        assert boundedVars != null;
        

        List<Iterator<Term>> iterators = new Vector<Iterator<Term>>(schemata.size());
        for (TermSchema schema : schemata) {
            iterators.add(schema.iterator(boundedVars,actualDepth));
        }
        
        termIterator = new IteratorChain<Term>(iterators);
        actualTerm = (termIterator.hasNext()) ? new Atom(termIterator.next()) : null;
    }

    public Iterator<Atom> iterator() {
        return this;
    }

    public boolean hasNext() {
        return termIterator.hasNext();
    }

    public Atom next() {
        return new Atom(termIterator.next());
    }

    public void remove() {
        throw new UnsupportedOperationException();
    }

}
