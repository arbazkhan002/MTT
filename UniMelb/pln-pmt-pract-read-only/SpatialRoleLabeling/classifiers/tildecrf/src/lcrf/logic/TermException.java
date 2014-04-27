/**
 * 
 */
package lcrf.logic;

/**
 * @author bgutmann
 * 
 */
public class TermException extends Exception {
    /**
     * random generated UID
     */
    private static final long serialVersionUID = 3546360634758411828L;

    int type;

    public static final int NOSUBTERMSALLOWED = 0;

    public TermException(int type) {
        super();
        this.type = type;
    }

}
