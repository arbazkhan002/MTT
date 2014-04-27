/**
 * 
 */
package lcrf.logic;

import java.io.Serializable;

/**
 * @author Bernd Gutmann
 * 
 */

public class UnificationJob implements Serializable {
    private static final long serialVersionUID = 3617569410097820217L;

    private int position;

    private Term term;

    public UnificationJob(int position, Term term) {
        if (term == null)
            throw new IllegalArgumentException();
        if (position < 0)
            throw new IllegalArgumentException(Integer.toString(position));

        this.position = position;
        this.term = term;
    }

    public int getPosition() {
        return position;
    }

    public Term getTerm() {
        return term;
    }

    public int hashCode() {
        return term.hashCode() * 16  + position;
    }

    public boolean equals(Object anObject) {
        if (anObject == this) {
            return true;
        }

        if (anObject instanceof UnificationJob) {
            UnificationJob job2 = (UnificationJob) anObject;
            return position == job2.getPosition() && term.equals(job2.getTerm());
        }

        return false;
    }

    public String toString() {
        return Integer.toString(position) + ":" + term;
    }
}
