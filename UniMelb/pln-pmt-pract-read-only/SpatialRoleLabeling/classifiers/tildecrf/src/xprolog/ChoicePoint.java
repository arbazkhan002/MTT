/**
 * 
 */
package xprolog;

/**
 * @author bgutmann
 * 
 */
/**
 * This is a simple record. A choicepoint contains the continuation (a goal
 * list) and the next clause to be tried.
 */

final class ChoicePoint {
    TermList goal;

    Clause clause;

    public ChoicePoint(TermList g, Clause c) {
        goal = g;
        clause = c;
    }

    public final String toString() {
        return ("  ||" + clause + "||   ");
    }
}
