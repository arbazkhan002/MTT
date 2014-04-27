/*
 * Created on 10.03.2005
 *
 */
package lcrf;

import java.util.NoSuchElementException;

/**
 * @author Bernd Gutmann
 * 
 */
public class UsedFieldMarker {
    private boolean[] field;

    private int index;

    public UsedFieldMarker(int n) {
        field = new boolean[n];
        index = 0;
    }

    public boolean hasNext() {
        return index < field.length;
    }

    public int nextElement() {
        if (index >= field.length) {
            throw new NoSuchElementException();
        }
        int result = index;
        do {
            index++;
        } while (index < field.length && field[index] == true);

        return result;
    }

    public void markUsed(int n) {
        if (n < 0 || n >= field.length) {
            throw new IndexOutOfBoundsException(Integer.toString(n));
        }

        field[n] = true;
        index = 0;
        while (index < field.length && field[index] == true) {
            index++;
        }
    }

    public void markUnused(int n) {
        if (n < 0 || n >= field.length) {
            throw new IndexOutOfBoundsException(Integer.toString(n));
        }
        
        field[n] = false;
        index = 0;
        while (index < field.length && field[index] == true) {
            index++;
        }
    }

}
