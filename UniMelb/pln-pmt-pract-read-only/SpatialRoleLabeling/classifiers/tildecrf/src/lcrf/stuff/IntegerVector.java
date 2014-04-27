/**
 * 
 */
package lcrf.stuff;

import java.util.List;
import java.util.Vector;

/**
 * @author Bernd Gutmann
 * 
 */
public class IntegerVector {
    public static int sumAll(Vector<Integer> v) {
        if (v == null) {
            return 0;
        }

        int sum = 0;
        for (int i = 0; i < v.size(); i++) {
            sum += v.get(i).intValue();
        }

        return sum;
    }

    public static Vector<Integer> subInt(Vector<Integer> v, int s) {
        if (v == null) {
            return null;
        }

        Vector<Integer> v2 = new Vector<Integer>(v.size());

        for (int i = 0; i < v.size(); i++) {
            v2.add(i, v.get(i) - s);
        }

        return v2;
    }

    public static Vector<Integer> sub(Vector<Integer> v1, Vector<Integer> v2) {
        assert v1 != null;
        assert v2 != null;
        assert v1.size() == v2.size();

        Vector<Integer> v3 = new Vector<Integer>(v1.size());

        for (int i = 0; i < v1.size(); i++) {
            v3.add(i, v1.get(i) - v2.get(i));
        }

        return v3;

    }

    public static int argmax(List<Integer> v) {
        if (v == null) {
            throw new IllegalArgumentException("Input must not be null.");
        }

        int argmax = 0;

        for (int i = 1; i < v.size(); i++) {
            if (v.get(i) > v.get(argmax)) {
                argmax = i;
            }
        }

        return argmax;
    }

}
