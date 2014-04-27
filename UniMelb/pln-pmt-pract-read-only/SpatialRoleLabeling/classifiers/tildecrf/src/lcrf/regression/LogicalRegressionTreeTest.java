package lcrf.regression;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.List;
import java.util.Random;
import java.util.Vector;

import junit.framework.TestCase;
import lcrf.WindowMaker;
import lcrf.XMLInput;
import lcrf.logic.Atom;
import lcrf.logic.Constant;
import lcrf.logic.UnificationJob;
import lcrf.logic.parser.ParseException;

import org.apache.log4j.BasicConfigurator;
import org.apache.log4j.Logger;

/**
 * @author Bernd Gutmann
 */
public class LogicalRegressionTreeTest extends TestCase {
    Atom a1, a2, a3, a4, a5, a6;

    List<Atom> example1;

    List<Atom> example2;

    List<Atom> example3;

    List<Atom> example4;

    List<Atom> example5;

    public LogicalRegressionTreeTest() {
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
        List<RegressionExample<List<Atom>>> examples = new Vector<RegressionExample<List<Atom>>>(1);
        examples.add(new RegressionExample<List<Atom>>(example1, 42.0));

        RegressionModel<List<Atom>> t = new LogicalRegressionTreeTrainer(1, 1).trainFromExamples(examples);

        assertEquals(42.0, t.getValueFor(example1), 0.0);
        assertEquals(42.0, t.getValueFor(example2), 0.0);
        assertEquals(new LogicalRegressionTree(42.0, null, null, null), t);
    }

    public void testTrainWithTwoExamples1() throws ParseException {
        List<RegressionExample<List<Atom>>> examples = new Vector<RegressionExample<List<Atom>>>(2);
        examples.add(new RegressionExample<List<Atom>>(example1, 42.0));
        examples.add(new RegressionExample<List<Atom>>(example2, 23.0));

        RegressionModel<List<Atom>> t = new LogicalRegressionTreeTrainer(2, 1).trainFromExamples(examples);

        assertEquals(42.0, t.getValueFor(example1), 0.0);
        assertEquals(23.0, t.getValueFor(example2), 0.0);
        assertEquals(new LogicalRegressionTree(0.0, new UnificationJob(0, a1.getTermRepresentation()),
                new LogicalRegressionTree(42.0, null, null, null), new LogicalRegressionTree(23.0, null,
                        null, null)), t);
    }

    public void testRandomValues() throws ParseException {
        // Logger.getLogger(this.getClass()).info("test with random values");
        int examplecount = 1000;
        int windowsize = 10;
        int atomcount = 3;

        Random rand = new Random(25111);

        List<RegressionExample<List<Atom>>> testexamples = new Vector<RegressionExample<List<Atom>>>(
                examplecount);
        List<RegressionExample<List<Atom>>> trainexamples = new Vector<RegressionExample<List<Atom>>>(
                examplecount);
        for (int i = 0; i < examplecount; i++) {
            List<Atom> example = new Vector<Atom>(windowsize);
            for (int j = 0; j < windowsize; j++) {
                example.add(new Atom("a" + rand.nextInt(atomcount)));
            }

            double v = rand.nextInt(10);

            trainexamples.add(new RegressionExample<List<Atom>>(example, v));
            testexamples.add(new RegressionExample<List<Atom>>(example, v));
        }

        // Logger.getLogger(this.getClass()).info("Start Training");
        RegressionModel<List<Atom>> t = new LogicalRegressionTreeTrainer(50, 1)
                .trainFromExamples(trainexamples);

        // Logger.getLogger(this.getClass()).info("training finished");
        // Logger.getLogger(this.getClass()).info("result = " + t);

        double error = 0;
        for (int i = 0; i < testexamples.size(); i++) {
            /*
             * Logger.getLogger(this.getClass()).info(
             * testexamples.get(i).content + " " + testexamples.get(i).value + " : " +
             * t.getValueFor(testexamples.get(i).content));
             */
            error += Math.abs(testexamples.get(i).value - t.getValueFor(testexamples.get(i).content));
        }
        // Logger.getLogger(this.getClass()).info("Average Error : " + error /
        // testexamples.size());
    }

    public void testWithSchema() throws ParseException {
        Logger.getLogger(this.getClass()).info("test with random values");
        int examplecount = 100;
        int windowsize = 5;
        int atomcount = 3;

        Random rand = new Random(25111);

        List<RegressionExample<List<Atom>>> testexamples = new Vector<RegressionExample<List<Atom>>>(
                examplecount);
        List<RegressionExample<List<Atom>>> trainexamples = new Vector<RegressionExample<List<Atom>>>(
                examplecount);
        for (int i = 0; i < examplecount; i++) {
            List<Atom> example = new Vector<Atom>(windowsize);
            for (int j = 0; j < windowsize; j++) {
                example.add(new Atom("a" + rand.nextInt(atomcount)));
            }

            double v = rand.nextInt(10);

            trainexamples.add(new RegressionExample<List<Atom>>(example, v));
            testexamples.add(new RegressionExample<List<Atom>>(example, v));
        }
        
        int[] fieldTypes = new int[windowsize];
        for (int i=0; i<windowsize; i++) {
            fieldTypes[i] = WindowMaker.FIELDINPUT;            
        }

        // Logger.getLogger(this.getClass()).info("Start Training");
        RegressionModel<List<Atom>> t = new LogicalRegressionTreeTrainer(6, 5, XMLInput
                .readSchemata("stuff/schemata3.xml"),fieldTypes).trainFromExamples(trainexamples);

        // Logger.getLogger(this.getClass()).info("training finished");
        // Logger.getLogger(this.getClass()).info("result = " + t);

        double error = 0;
        for (int i = 0; i < testexamples.size(); i++) {
            /*
             * Logger.getLogger(this.getClass()).info(
             * testexamples.get(i).content + " " + testexamples.get(i).value + " : " +
             * t.getValueFor(testexamples.get(i).content));
             */
            error += Math.abs(testexamples.get(i).value - t.getValueFor(testexamples.get(i).content));
        }
        // Logger.getLogger(this.getClass()).info("Average Error : " + error /
        // testexamples.size());
    }

    public void testSerialization() throws Exception {
        LogicalRegressionTree tree1 = new LogicalRegressionTree(42.0, null, null, null);
        LogicalRegressionTree tree2 = new LogicalRegressionTree(0.0, new UnificationJob(0, new Atom(
                "this(IS,a,'test')").getTermRepresentation()),
                new LogicalRegressionTree(45, null, null, null), new LogicalRegressionTree(67, null, null,
                        null));

        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oas = new ObjectOutputStream(baos);
        oas.writeObject(tree1);
        oas.writeObject(tree2);
        ByteArrayInputStream bais = new ByteArrayInputStream(baos.toByteArray());
        ObjectInputStream ois = new ObjectInputStream(bais);
        Object o1 = ois.readObject();
        Object o2 = ois.readObject();

        assertEquals(tree1, o1);
        assertEquals(tree2, o2);
    }
    
    public void testPrunning1() throws Exception {
        LogicalRegressionTree tree1 = new LogicalRegressionTree(0.0, new UnificationJob(0,new Constant("a")), new LogicalRegressionTree(25.0,null,null,null), new LogicalRegressionTree(25.0,null,null,null));
        LogicalRegressionTree tree2 = new LogicalRegressionTree(0.0, new UnificationJob(0,new Constant("a")), new LogicalRegressionTree(25.0,null,null,null), new LogicalRegressionTree(25.0,null,null,null));
        LogicalRegressionTree tree3 = new LogicalRegressionTree(0.0, new UnificationJob(1,new Constant("b")), tree1,tree2);
        LogicalRegressionTree tree4 = new LogicalRegressionTree(25.0,null,null,null);
        
        assertEquals(tree4,tree3.doPrunning(Double.MIN_VALUE));        
    }

}
