package lcrf.counting;

import java.util.List;
import java.util.Random;
import java.util.Vector;

import junit.framework.TestCase;
import lcrf.XMLInput;
import lcrf.logic.Atom;
import lcrf.logic.UnificationJob;
import lcrf.logic.parser.ParseException;
import lcrf.stuff.ArrayStuff;

import org.apache.log4j.BasicConfigurator;
import org.apache.log4j.Logger;

/**
 * @author Bernd Gutmann
 */
public class LogicalCountingTreeTest extends TestCase {
    Atom a1, a2, a3, a4, a5, a6;

    List<Atom> example1;

    List<Atom> example2;

    List<Atom> example3;

    List<Atom> example4;

    List<Atom> example5;

    public LogicalCountingTreeTest() {
        super();
        BasicConfigurator.resetConfiguration();
        BasicConfigurator.configure();
    }

    public void setUp() throws ParseException {
        // Logger.getLogger("SRT").setLevel(Level.WARN);
        a1 = new Atom("kandel");
        a2 = new Atom("platte");
        a3 = new Atom("hinterwaldkopf");
        a4 = new Atom("feldberg");
        a5 = new Atom("stuebenwasen");
        a6 = new Atom("schauinsland");

        example1 = new Vector<Atom>(3);
        example1.add(a1);
        example1.add(a2);
        example1.add(a3);

        example2 = new Vector<Atom>(3);
        example2.add(a6);
        example2.add(a5);
        example2.add(a4);

        example3 = new Vector<Atom>(3);
        example3.add(a1);
        example3.add(a5);
        example3.add(a4);

        example4 = new Vector<Atom>(3);
        example4.add(a1);
        example4.add(a1);
        example4.add(a1);

        example5 = new Vector<Atom>(3);
        example5.add(a6);
        example5.add(a5);
        example5.add(a4);
    }

    public void testTrainWithOneExample() throws ParseException {
        List<CountingExample> examples = new Vector<CountingExample>(1);
        examples.add(new CountingExample(example1, 1));

        LogicalCountingTree t = new LogicalCountingTreeTrainer(1, 1).trainFromExamples(examples, 2);

        int[] countArray = new int[] { 0, 1 };

        assertTrue(ArrayStuff.arrayEquals(countArray, t.getCountArrayFor(example1)));
        assertTrue(ArrayStuff.arrayEquals(countArray, t.getCountArrayFor(example2)));
        assertEquals(new LogicalCountingTree(countArray, null, null, null), t);
    }

    public void testTrainWithTwoExamples1() throws ParseException {
        List<CountingExample> examples = new Vector<CountingExample>(1);
        examples.add(new CountingExample(example1, 1));
        examples.add(new CountingExample(example2, 0));

        LogicalCountingTree t = new LogicalCountingTreeTrainer(2, 1).trainFromExamples(examples, 2);

        int[] countArray1 = new int[] { 1, 0 };
        int[] countArray2 = new int[] { 0, 1 };

        assertTrue(ArrayStuff.arrayEquals(countArray2, t.getCountArrayFor(example1)));
        assertTrue(ArrayStuff.arrayEquals(countArray1, t.getCountArrayFor(example2)));
        assertEquals(new LogicalCountingTree(null, new UnificationJob(2, new Atom("feldberg")
                .getTermRepresentation()), new LogicalCountingTree(countArray1, null, null, null),
                new LogicalCountingTree(countArray2, null, null, null)), t);

    }

    public void testTrainWithThreeExamples1() throws ParseException {
        List<CountingExample> examples = new Vector<CountingExample>(1);
        examples.add(new CountingExample(example1, 0));
        examples.add(new CountingExample(example1, 1));
        examples.add(new CountingExample(example2, 0));

        LogicalCountingTree t = new LogicalCountingTreeTrainer(2, 1).trainFromExamples(examples, 2);

        int[] countArray1 = new int[] { 1, 1 };
        int[] countArray2 = new int[] { 1, 0 };

        assertTrue(ArrayStuff.arrayEquals(countArray1, t.getCountArrayFor(example1)));
        assertTrue(ArrayStuff.arrayEquals(countArray2, t.getCountArrayFor(example2)));
        assertEquals(new LogicalCountingTree(null, new UnificationJob(2, new Atom("hinterwaldkopf")
                .getTermRepresentation()), new LogicalCountingTree(countArray1, null, null, null),
                new LogicalCountingTree(countArray2, null, null, null)), t);

    }

    public void testRandomValues() throws ParseException {

        int examplecount = 100;
        int windowsize = 5;
        int atomcount = 3;
        int countingClasses = 10;

        Random rand = new Random(25111);

        List<CountingExample> testexamples = new Vector<CountingExample>(examplecount);
        List<CountingExample> trainexamples = new Vector<CountingExample>(examplecount);
        for (int i = 0; i < examplecount; i++) {
            List<Atom> example = new Vector<Atom>(windowsize);
            for (int j = 0; j < windowsize; j++) {
                example.add(new Atom("a" + rand.nextInt(atomcount)));
            }

            int v = rand.nextInt(countingClasses);

            trainexamples.add(new CountingExample(example, v));
            testexamples.add(new CountingExample(example, v));
        }

        LogicalCountingTree t = new LogicalCountingTreeTrainer(6, 1).trainFromExamples(trainexamples,
                countingClasses);

        for (int i = 0; i < testexamples.size(); i++) {
            Logger.getLogger(this.getClass()).info(
                    testexamples.get(i).content + " " + testexamples.get(i).number + " : "
                            + ArrayStuff.argmax(t.getCountArrayFor(testexamples.get(i).content)));

        }
    }

    public void testRandomValuesWithSchemata() throws ParseException {

        int examplecount = 1000;
        int windowsize = 5;
        int atomcount = 3;
        int countingClasses = 10;

        Random rand = new Random(25111);

        List<CountingExample> testexamples = new Vector<CountingExample>(examplecount);
        List<CountingExample> trainexamples = new Vector<CountingExample>(examplecount);
        for (int i = 0; i < examplecount; i++) {
            List<Atom> example = new Vector<Atom>(windowsize);
            for (int j = 0; j < windowsize; j++) {
                if (rand.nextBoolean()) {
                    example.add(new Atom("a(" + rand.nextInt(atomcount) + ")"));
                } else {
                    example.add(new Atom("b(" + rand.nextInt(atomcount) + ")"));
                }
            }

            int v = rand.nextInt(countingClasses);

            trainexamples.add(new CountingExample(example, v));
            testexamples.add(new CountingExample(example, v));
        }

        LogicalCountingTree t = new LogicalCountingTreeTrainer(10, 6, XMLInput
                .readSchemata("stuff/schemata3.xml")).trainFromExamples(trainexamples, countingClasses);

        for (int i = 0; i < testexamples.size(); i++) {
            Logger.getLogger(this.getClass()).info(
                    testexamples.get(i).content + " " + testexamples.get(i).number + " : "
                            + ArrayStuff.argmax(t.getCountArrayFor(testexamples.get(i).content)));

        }
    }

}
