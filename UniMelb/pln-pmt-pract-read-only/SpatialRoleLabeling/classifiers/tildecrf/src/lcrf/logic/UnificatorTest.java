package lcrf.logic;

import java.util.Vector;

import junit.framework.TestCase;
import lcrf.logic.parser.ParseException;

import org.apache.log4j.BasicConfigurator;

public class UnificatorTest extends TestCase {
    public void setUp() {
        BasicConfigurator.resetConfiguration();
        BasicConfigurator.configure();
    }

    public void test1() throws Exception {
        Term t1 = new Atom("X").getTermRepresentation();
        Term t2 = new Atom("f(X)").getTermRepresentation();

        assertNull(Unificator.findMGU(t1, t2));
        assertEquals(new Substitutions(), Unificator.findMGU(t1, t1));
        assertEquals(new Substitutions(), Unificator.findMGU(t2, t2));
    }

    public void test2() throws Exception {
        Term t1 = new Atom("f(X,Y)").getTermRepresentation();
        Term t2 = new Atom("f(Y,Y)").getTermRepresentation();

        Substitutions substs = new Substitutions();
        substs.add(new Substitution(new Variable("Y"), new Variable("X")));

        assertEquals(substs, Unificator.findMGU(t1, t2));
        assertEquals(new Substitutions(), Unificator.findMGU(t1, t1));
        assertEquals(new Substitutions(), Unificator.findMGU(t2, t2));

    }

    public void test3() throws Exception {
        Term t1 = new Atom("f(42,X)").getTermRepresentation();
        Term t2 = new Atom("f(Y,'sunny')").getTermRepresentation();

        Substitutions substs = new Substitutions();
        substs.add(new Substitution(new Variable("X"), new StringConstant("sunny")));
        substs.add(new Substitution(new Variable("Y"), new NumberConstant(42)));

        assertEquals(substs, Unificator.findMGU(t1, t2));
        assertEquals(new Substitutions(), Unificator.findMGU(t1, t1));
        assertEquals(new Substitutions(), Unificator.findMGU(t2, t2));
    }

    public void test4() throws Exception {
        Term t1 = new Atom("f(42,Y)").getTermRepresentation();
        Term t2 = new Atom("f(Y,'sunny')").getTermRepresentation();

        assertNull(Unificator.findMGU(t1, t2));
        assertEquals(new Substitutions(), Unificator.findMGU(t1, t1));
        assertEquals(new Substitutions(), Unificator.findMGU(t2, t2));
    }

    public void testJobUnification() throws Exception {
        Vector<Atom> sequence = new Vector<Atom>();
        Vector<UnificationJob> jobs = new Vector<UnificationJob>();

        assertEquals(new Substitutions(), Unificator.findMGU(sequence, jobs));
    }

    public void testJobUnification2() throws Exception {
        Vector<Atom> sequence = new Vector<Atom>();
        sequence.add(new Atom("dog(X)"));
        sequence.add(new Atom("cat(X)"));

        Vector<UnificationJob> jobs = new Vector<UnificationJob>();
        jobs.add(new UnificationJob(0, new Atom("dog(rex)").getTermRepresentation()));
        jobs.add(new UnificationJob(1, new Atom("_AnVar").getTermRepresentation()));

        Substitutions substs = new Substitutions();
        substs.add(new Substitution(new Variable("X"), new Constant("rex")));
        substs.add(new Substitution(new Variable("_AnVar"), new Atom("cat(rex)").getTermRepresentation()));

        assertEquals(substs, Unificator.findMGU(sequence, jobs));
    }

    public void testJobUnification3() throws Exception {
        Vector<Atom> sequence = new Vector<Atom>();
        sequence.add(new Atom("dog(X)"));
        sequence.add(new Atom("cat(X)"));
        sequence.add(new Atom("g(g(Y))"));

        Vector<UnificationJob> jobs = new Vector<UnificationJob>();
        jobs.add(new UnificationJob(0, new Atom("dog(rex)").getTermRepresentation()));
        jobs.add(new UnificationJob(1, new Atom("_AnVar").getTermRepresentation()));
        jobs.add(new UnificationJob(2, new Atom("g(g(X))").getTermRepresentation()));

        Substitutions substs = new Substitutions();
        substs.add(new Substitution(new Variable("X"), new Constant("rex")));
        substs.add(new Substitution(new Variable("_AnVar"), new Atom("cat(rex)").getTermRepresentation()));
        substs.add(new Substitution(new Variable("Y"), new Constant("rex")));

        assertEquals(substs, Unificator.findMGU(sequence, jobs));
    }

    public void testWithDoubledVariable() throws ParseException {
        Term t = new Atom("a(1)").getTermRepresentation();
        Term t2 = new Atom("a(X)").getTermRepresentation();

        Substitutions substs = new Substitutions();
        substs.add(new Substitution(new Variable("X"), new NumberConstant(1)));

        assertNull(Unificator.findSpecialisation(t, t2, new Substitutions()));
        assertEquals(substs, Unificator.findSpecialisation(t2, t, new Substitutions()));
    }

}
