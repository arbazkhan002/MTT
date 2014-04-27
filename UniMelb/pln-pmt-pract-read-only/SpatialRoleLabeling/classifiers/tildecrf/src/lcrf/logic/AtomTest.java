/*
 * Created on 08.03.2005
 *
 */
package lcrf.logic;

import junit.framework.TestCase;
import lcrf.logic.parser.ParseException;

/**
 * @author Bernd Gutmann
 * 
 */
public class AtomTest extends TestCase {
    public void testEqualsSimple() throws ParseException {
        Atom a1 = new Atom("gurke");
        Atom a2 = new Atom("tomate");
        Atom a3 = new Atom("gurke");

        assertTrue(a1.equals(a3));
        assertFalse(a1.equals(a2));
    }

    public void testParserFunction() throws ParseException {
        Atom a1 = new Atom("dog(chichilla)");
        Atom a2 = new Atom("dog(father(rex))");
        Atom a3 = new Atom("  dog (   father(rex   ))");

        assertFalse(a1.equals(a2));
        assertFalse(a1.equals(a3));
        assertTrue(a2.equals(a3));
        assertTrue(a3.equals(a2));
    }

    public void testIsMoreGeneralThan() throws ParseException {
        assertTrue(new Atom("X").isMoreGeneralThan(new Atom("X")));
        assertTrue(new Atom("X").isMoreGeneralThan(new Atom("Y")));
        assertTrue(new Atom("X").isMoreGeneralThan(new Atom("42")));
        assertTrue(new Atom("X").isMoreGeneralThan(new Atom("a")));
        assertTrue(new Atom("X").isMoreGeneralThan(new Atom("a(1)")));
        assertTrue(new Atom("a(X)").isMoreGeneralThan(new Atom("a(X)")));
        assertFalse(new Atom("a(X,X)").isMoreGeneralThan(new Atom("a(1,2)")));
        assertTrue(new Atom("a(X,Y)").isMoreGeneralThan(new Atom("a(1,2)")));
        assertFalse(new Atom("X").isMoreGeneralThan(new Atom("a(X)")));
        assertFalse(new Atom("1").isMoreGeneralThan(new Atom("X")));
    }

}
