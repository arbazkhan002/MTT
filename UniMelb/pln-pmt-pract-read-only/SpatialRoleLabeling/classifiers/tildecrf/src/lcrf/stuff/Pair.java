/**
 * 
 */
package lcrf.stuff;

import java.io.Serializable;

/**
 * @author Bernd Gutmann
 * 
 */
public class Pair<T1, T2> implements Serializable {
    private static final long serialVersionUID = 3257847684017699129L;

    public T1 o1;

    public T2 o2;

    public Pair(T1 o1, T2 o2) {
        this.o1 = o1;
        this.o2 = o2;
    }

    public int hashCode() {
        return o1.hashCode() * 8 ^ o2.hashCode();
    }

    public String toString() {
        return "(" + o1.toString() + "," + o2.toString() + ")";
    }

    public boolean equals(Object anObject) {
        if (this == anObject)
            return true;
        if (anObject instanceof Pair) {
            Pair p2 = (Pair) anObject;
            return o1.equals(p2.o1) && o2.equals(p2.o2);
        }
        return false;
    }
}
