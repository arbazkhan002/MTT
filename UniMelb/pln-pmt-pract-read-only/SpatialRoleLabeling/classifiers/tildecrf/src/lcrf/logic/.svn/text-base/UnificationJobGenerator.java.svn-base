/**
 * 
 */
package lcrf.logic;

import java.util.Iterator;
import java.util.List;

/**
 * @author Bernd Gutmann
 * 
 */
public class UnificationJobGenerator implements Iterator<UnificationJob>, Iterable<UnificationJob> {
    private List<Atom> differentAtoms;

    private int maxsequencelength;

    private int nextposition = 0;

    private int nextatom = 0;

    public UnificationJobGenerator(List<Atom> atoms, int maxLength) {
        differentAtoms = atoms;
        maxsequencelength = maxLength;
        nextatom = 0;
        nextposition = 0;
    }

    public boolean hasNext() {
        return nextatom < differentAtoms.size();
    }

    public UnificationJob next() {
        UnificationJob job = new UnificationJob(nextposition, differentAtoms.get(nextatom)
                .getTermRepresentation());
        nextposition++;
        if (nextposition >= maxsequencelength) {
            nextposition = 0;
            nextatom++;
        }

        return job;
    }

    public void remove() {
        throw new UnsupportedOperationException();
    }

    public Iterator<UnificationJob> iterator() {
        return this;
    }

}
