/**
 * 
 */
package xprolog;

/**
 * @author bgutmann
 * 
 */
final class Number extends Term {
    public Number(String s) {
        super(s, 0);
        try {
            varid = Integer.parseInt(s);
        } catch (Exception e) {
            varid = 0;
        }
    }

    public Number(int n) {
        super(Integer.toString(n).intern(), 0);
        varid = n;
    }

    public int value() {
        return varid;
    }

    public Term dup() // to copy correctly CUT & Number terms
    {
        return new Number(varid);
    }
}
