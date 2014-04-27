package lcrf;

import java.util.Vector;

import junit.framework.TestCase;
import lcrf.logic.Atom;
import lcrf.logic.parser.ParseException;

public class ClassificationExampleContainerTest extends TestCase {

    public void testConstructor() throws ParseException {
        ClassificationExampleContainer ex1 = new ClassificationExampleContainer();
        assertEquals(0, ex1.size());
        assertEquals(0, ex1.getClassAtoms().size());
    }

    public void testAddExample() throws ParseException {
        ClassificationExampleContainer ex1 = new ClassificationExampleContainer();
        ex1.addExample(new Vector<Atom>(), new Atom("1"),"Sequence1");
        ex1.addExample(new Vector<Atom>(), new Atom("2"),"Sequence2");
        assertEquals(2, ex1.size());
        assertEquals(new Vector<Atom>(), ex1.getInputSequence(0));
        assertEquals(new Atom("1"), ex1.getClassAtom(0));
        assertEquals("Sequence1", ex1.getSequenceId(0));
        assertEquals("Sequence2", ex1.getSequenceId(1));
    }

    public void testGenerateFolds() throws ParseException {
        ClassificationExampleContainer ex1 = new ClassificationExampleContainer();
        ex1.addExamples(XMLInput.readSequencesDOM("data/proteinfolds_kristian/fold1l.100.train.xml").o1,
                new Atom("0"));
        assertEquals(100, ex1.size());

        ClassificationExampleContainer fold1 = ex1.getSubfold(3, 0, 2511);
        ClassificationExampleContainer fold2 = ex1.getSubfold(3, 1, 2511);
        ClassificationExampleContainer fold3 = ex1.getSubfold(3, 2, 2511);

        assertEquals(33, fold1.size());
        assertEquals(33, fold2.size());
        assertEquals(34, fold3.size());

        fold3.addExamples(fold2);
        fold3.addExamples(fold1);

        assertEquals(100, fold3.size());
        assertTrue(ex1.haveSameExamples(fold3));
        assertTrue(fold3.haveSameExamples(ex1));
    }

    public void testGenerateFolds2() throws ParseException {
        ClassificationExampleContainer ex1 = new ClassificationExampleContainer();
        ex1.addExamples(XMLInput.readSequencesDOM("data/proteinfolds_kristian/fold1l.100.train.xml").o1,
                new Atom("0"));
        assertEquals(100, ex1.size());

        ClassificationExampleContainer fold1 = ex1.getSubfold(3, 0, 2511);
        ClassificationExampleContainer fold2 = ex1.getSubfold(3, 1, 2511);
        ClassificationExampleContainer fold3 = ex1.getSubfold(3, 2, 2511);
        ClassificationExampleContainer fold23 = ex1.getSubfoldInverse(3, 0, 2511);

        assertEquals(33, fold1.size());
        assertEquals(33, fold2.size());
        assertEquals(34, fold3.size());
        assertEquals(67, fold23.size());

        fold3.addExamples(fold2);

        assertTrue(fold23.haveSameExamples(fold3));
        assertTrue(fold3.haveSameExamples(fold23));

        fold3.addExamples(fold1);
        fold23.addExamples(fold1);

        assertTrue(ex1.haveSameExamples(fold3));
        assertTrue(fold3.haveSameExamples(ex1));
        assertTrue(ex1.haveSameExamples(fold23));
        assertTrue(fold23.haveSameExamples(ex1));

        assertEquals(100, fold3.size());
        assertEquals(100, fold23.size());
    }
}
