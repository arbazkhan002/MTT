package lcrf;

import java.util.Vector;

import junit.framework.TestCase;
import lcrf.logic.Atom;
import lcrf.logic.Interpretation;
import lcrf.regression.InterpretationRegressionTreeTrainerBestFirst;

import org.apache.log4j.BasicConfigurator;

public class CRFInterpretationTest extends TestCase {
    public void setUp() {
        BasicConfigurator.resetConfiguration();
        BasicConfigurator.configure();
    }

    public void testSimple() throws Exception {
        Vector<Atom> classAtoms = new Vector<Atom>();
        classAtoms.add(new Atom("x"));
        classAtoms.add(new Atom("y"));

        InterpretationExampleContainer examples = new InterpretationExampleContainer(classAtoms);

        Vector<Interpretation> input1 = new Vector<Interpretation>();
        Vector<Atom> output1 = new Vector<Atom>();

        Vector<Interpretation> input2 = new Vector<Interpretation>();
        Vector<Atom> output2 = new Vector<Atom>();

        {
            Interpretation i1 = new Interpretation();
            i1.add(new Atom("ab"));

            Interpretation i2 = new Interpretation();
            i2.add(new Atom("a"));

            Interpretation i3 = new Interpretation();
            i3.add(new Atom("a"));

            Interpretation i4 = new Interpretation();
            i4.add(new Atom("a"));

            Interpretation i5 = new Interpretation();
            i5.add(new Atom("a"));

            input1.add(i1);
            input1.add(i2);
            input1.add(i3);
            input1.add(i4);
            input1.add(i5);

            output1.add(new Atom("x"));
            output1.add(new Atom("x"));
            output1.add(new Atom("x"));
            output1.add(new Atom("x"));
            output1.add(new Atom("x"));

        }

        {
            Interpretation i1 = new Interpretation();
            i1.add(new Atom("a"));
            i1.add(new Atom("b"));

            Interpretation i2 = new Interpretation();
            i2.add(new Atom("a"));
            i2.add(new Atom("b"));

            Interpretation i3 = new Interpretation();
            i3.add(new Atom("a"));
            i3.add(new Atom("b"));

            Interpretation i4 = new Interpretation();
            i4.add(new Atom("a"));
            i4.add(new Atom("b"));

            Interpretation i5 = new Interpretation();
            i5.add(new Atom("a"));
            i5.add(new Atom("b"));

            input2.add(i1);
            input2.add(i2);
            input2.add(i3);
            input2.add(i4);
            input2.add(i5);

            output2.add(new Atom("y"));
            output2.add(new Atom("y"));
            output2.add(new Atom("y"));
            output2.add(new Atom("y"));
            output2.add(new Atom("y"));

        }

        examples.addExample(input1, output1);
        examples.addExample(input2, output2);

        CRFInterpretation crf0 = new CRFInterpretation(classAtoms,
                new InterpretationRegressionTreeTrainerBestFirst(14, 1), null);
        crf0.train(examples, 2);

        assertEquals(output1, crf0.classifyFB(input1));
        assertEquals(output2, crf0.classifyFB(input2));

    }
}
