package lcrf.logic;

import junit.framework.TestCase;

public class SubstitutionsTest extends TestCase {
    public void testsubstitution1() throws Exception {
        Atom a1 = new Atom("the(dog,Y,good(X))");
        Atom a2 = new Atom("the(dog,'sunny',good(  42  ))");

        Atom b1 = new Atom("the(good(X))");
        Atom b2 = new Atom("the(good(42))");

        Substitution subst1 = new Substitution(new Variable("X"), new NumberConstant(42));
        Substitution subst2 = new Substitution(new Variable("Y"), new StringConstant("sunny"));
        Substitutions substs = new Substitutions();
        substs.add(subst1);
        substs.add(subst2);

        assertEquals(a2.getTermRepresentation(), substs.apply(a1.getTermRepresentation()));
        assertEquals(b2.getTermRepresentation(), substs.apply(b1.getTermRepresentation()));
    }

}
