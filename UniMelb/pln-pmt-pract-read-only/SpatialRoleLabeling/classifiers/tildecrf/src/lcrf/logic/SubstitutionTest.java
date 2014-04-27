package lcrf.logic;

import junit.framework.TestCase;

public class SubstitutionTest extends TestCase {
    public void testsubstitution1() throws Exception {
        Atom a1 = new Atom("the(dog,is,good(X))");
        Atom a2 = new Atom("the(dog,is,good(  42  ))");

        Atom b1 = new Atom("the(X,X,good(X))");
        Atom b2 = new Atom("the(42,42,good(42))");

        Substitution subst = new Substitution(new Variable("X"), new NumberConstant(42));

        assertEquals(a2.getTermRepresentation(), subst.apply(a1.getTermRepresentation()));
        assertEquals(b2.getTermRepresentation(), subst.apply(b1.getTermRepresentation()));
    }

}
