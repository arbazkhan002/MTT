package lcrf.regression;

import junit.framework.TestCase;
import lcrf.logic.Atom;
import lcrf.logic.Interpretation;

import org.apache.log4j.BasicConfigurator;
import org.apache.log4j.Logger;

public class InterpretationRegressionTreeTest extends TestCase {
    public void setUp() {
        BasicConfigurator.resetConfiguration();
        BasicConfigurator.configure();
    }

    public void testSimpel() throws Exception {
        InterpretationRegressionTree tree0 = new InterpretationRegressionTree(42.0d, null, null, null);

        Interpretation i0 = new Interpretation();
        Interpretation i1 = new Interpretation();
        i1.add(new Atom("a1"));

        assertEquals(42.0d, tree0.getValueFor(i0));
        assertEquals(42.0d, tree0.getValueFor(i1));
    }

    public void testSimpe2() throws Exception {
        InterpretationRegressionTree tree0 = new InterpretationRegressionTree(42.0d, null, null, null);
        InterpretationRegressionTree tree1 = new InterpretationRegressionTree(23.0d, null, null, null);
        InterpretationRegressionTree tree2 = new InterpretationRegressionTree(23.0d, new Atom("a1"), tree0,
                tree1);

        Interpretation i0 = new Interpretation();
        Interpretation i1 = new Interpretation();
        i1.add(new Atom("a1"));

        assertEquals(23.0d, tree2.getValueFor(i0));
        assertEquals(42.0d, tree2.getValueFor(i1));
    }

    public void testSimpel3() throws Exception {
        InterpretationRegressionTree tree0 = new InterpretationRegressionTree(42.0d, null, null, null);
        InterpretationRegressionTree tree1 = new InterpretationRegressionTree(23.0d, null, null, null);
        InterpretationRegressionTree tree2 = new InterpretationRegressionTree(23.0d, new Atom("a1"), tree0,
                tree1);
        InterpretationRegressionTree tree3 = new InterpretationRegressionTree(17.0d, null, null, null);
        InterpretationRegressionTree tree4 = new InterpretationRegressionTree(23.0d, new Atom("b1"), tree3,
                tree2);

        Logger.getLogger("wsd").info(tree2);

        Interpretation i0 = new Interpretation();
        Interpretation i1 = new Interpretation();
        i1.add(new Atom("a1"));

        Interpretation i2 = new Interpretation();
        i2.add(new Atom("a1"));
        i2.add(new Atom("b1"));

        assertEquals(23.0d, tree4.getValueFor(i0));
        assertEquals(42.0d, tree4.getValueFor(i1));
        assertEquals(17.0d, tree4.getValueFor(i2));
    }

    public void testSimpel4() throws Exception {
        InterpretationRegressionTree tree0 = new InterpretationRegressionTree(42.0d, null, null, null);
        InterpretationRegressionTree tree1 = new InterpretationRegressionTree(23.0d, null, null, null);
        InterpretationRegressionTree tree2 = new InterpretationRegressionTree(23.0d, new Atom("a(X)"), tree0,
                tree1);
        InterpretationRegressionTree tree3 = new InterpretationRegressionTree(17.0d, null, null, null);
        InterpretationRegressionTree tree4 = new InterpretationRegressionTree(23.0d, new Atom("b(X)"), tree2,
                tree3);

        Interpretation i1 = new Interpretation();
        Interpretation i2 = new Interpretation();
        Interpretation i3 = new Interpretation();

        i1.add(new Atom("a(1)"));

        i2.add(new Atom("a(1)"));
        i2.add(new Atom("b(1)"));

        i3.add(new Atom("a(1)"));
        i3.add(new Atom("b(2)"));

        assertEquals(17.0d, tree4.getValueFor(i1));
        assertEquals(42.0d, tree4.getValueFor(i2));
        assertEquals(23.0d, tree4.getValueFor(i3));
    }

}
