/*
 * Created on 09.03.2005
 */
package lcrf;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.List;
import java.util.Random;
import java.util.Vector;

import junit.framework.TestCase;
import lcrf.counting.LogicalCountingTreeTrainer;
import lcrf.logic.Atom;
import lcrf.logic.Constant;
import lcrf.logic.NumberConstant;
import lcrf.logic.parser.ParseException;
import lcrf.regression.LogicalRegressionTreeTrainer;
import lcrf.regression.PrologRegressionTreeTrainer;
import lcrf.regression.RegressionModelTrainer;
import lcrf.regression.TrainerWrapper;
import lcrf.stuff.NumberStorage;

import org.apache.log4j.BasicConfigurator;
import org.apache.log4j.Logger;

/**
 * @author Bernd Gutmann
 */
public class CRFTest extends TestCase {
    Atom a1, a2, a3, a4, a5, a6, b1, b2;

    Vector<Atom> classAtom1 = new Vector<Atom>(2);

    List<Atom> input1;

    List<Atom> output1;

    Vector<Atom> input2;

    Vector<Atom> output2;

    protected void setUp() throws Exception {
        super.setUp();

        BasicConfigurator.resetConfiguration();
        BasicConfigurator.configure();

        a1 = new Atom("kandel");
        a2 = new Atom("platte");
        a3 = new Atom("hinterwaldkopf");
        a4 = new Atom("feldberg");
        a5 = new Atom("stuebenwasen");
        a6 = new Atom("schauinsland");

        b1 = new Atom("gut");
        b2 = new Atom("schlecht");

        input1 = new Vector<Atom>(6);
        output1 = new Vector<Atom>(6);
        input2 = new Vector<Atom>(10);
        output2 = new Vector<Atom>(10);

        input1.add(a1);
        input1.add(a2);
        input1.add(a3);
        input1.add(a4);
        input1.add(a5);
        input1.add(a6);
        input1.add(a6);

        output1.add(b2);
        output1.add(b1);
        output1.add(b2);
        output1.add(b1);
        output1.add(b2);
        output1.add(b2);
        output1.add(b2);

        input2.add(a1);
        input2.add(a1);
        input2.add(a1);
        input2.add(a1);
        input2.add(a1);
        input2.add(a1);
        input2.add(a1);
        input2.add(a1);
        input2.add(a1);
        input2.add(a1);
        output2.add(b1);
        output2.add(b2);
        output2.add(b1);
        output2.add(b2);
        output2.add(b1);
        output2.add(b2);
        output2.add(b1);
        output2.add(b2);
        output2.add(b1);
        output2.add(b2);

        classAtom1.add(b1);
        classAtom1.add(b2);
    }

    public void testConstructor() {
        CRF crf0 = new CRF(classAtom1, new LogicalRegressionTreeTrainer(8, 1), 1,
                new LogicalCountingTreeTrainer(5, 1));
    }

    public void testOneSimpleExampleOnly() throws Exception {
        Vector<Atom> classAtoms = new Vector<Atom>();
        classAtoms.add(new Atom("x"));
        classAtoms.add(new Atom("y"));
        SimpleExampleContainer examples = new SimpleExampleContainer(classAtoms);

        Vector<Atom> input = new Vector<Atom>();
        input.add(new Atom("a"));
        input.add(new Atom("a"));
        Vector<Atom> output = new Vector<Atom>();
        output.add(new Atom("x"));
        output.add(new Atom("x"));
        examples.addExample(input, output);

        CRF crf0 = new CRF(classAtoms, new LogicalRegressionTreeTrainer(14, 1), 7,
                new LogicalCountingTreeTrainer(5, 1));
        crf0.trainOneStep(examples);
    }
    
    public void testOneSimpleExampleOnly2() throws Exception {
        Vector<Atom> classAtoms = new Vector<Atom>();
        classAtoms.add(new Atom("c1"));
        classAtoms.add(new Atom("c2"));
        ClassificationExampleContainer examples = new ClassificationExampleContainer();

        Vector<Atom> input = new Vector<Atom>();
        input.add(new Atom("a"));
        input.add(new Atom("a"));
        input.add(new Atom("a"));
        input.add(new Atom("a"));
        input.add(new Atom("a"));
        input.add(new Atom("a"));
        input.add(new Atom("a"));
        examples.addExample(input,new Atom("c1"));
        
        Vector<Atom> input2 = new Vector<Atom>();
        input2.add(new Atom("b"));
        input2.add(new Atom("b"));
        input2.add(new Atom("b"));
        input2.add(new Atom("b"));
        input2.add(new Atom("b"));
        input2.add(new Atom("b"));
        input2.add(new Atom("b"));
        examples.addExample(input,new Atom("c2"));
        

        CRF crf0 = new CRF(classAtoms, new LogicalRegressionTreeTrainer(14, 1), 7,
                new LogicalCountingTreeTrainer(5, 1));
        crf0.trainOneStep(examples);        
        Logger.getLogger(getClass()).info(crf0.classifyFB(input1));
        Logger.getLogger(getClass()).info(crf0.classifyViterbi(input1));
        Logger.getLogger(getClass()).info(crf0.classifyFB(input2));
        Logger.getLogger(getClass()).info(crf0.classifyViterbi(input2));
    }


    public void testTrain_prolog() throws ParseException {
        String bgknowledge = "test(same)."
                + "test(outis(Y)) :- member(Y,[city(1),city(2)])."
                + "test(outputis(Pos,Elem)) :- outputPositions(Positions),member(Pos,Positions),member(Elem,[a,b,c,d])."
                + "test(outoldis(Y)) :- test(outYis(Y))." + "succeds(test(same),[X,X|_])."
                + "succeds(test(outis(X)),[_,X|_])." + "succeds(test(outoldis(X)),[X,_|_])."
                + "succeds(test(outputis(Pos,Elem)),Window):-nth0(Pos,Window,Elem)."
                + "succeds(not(Test),Window):-not(succeds(Test,Window)).";

        Vector<Atom> classAtoms = new Vector<Atom>();
        classAtoms.add(new Atom("city(1)"));
        classAtoms.add(new Atom("city(2)"));
        SimpleExampleContainer examples = new SimpleExampleContainer(classAtoms);

        Vector<Atom> input = new Vector<Atom>();
        input.add(new Atom("a"));
        input.add(new Atom("b"));
        input.add(new Atom("b"));
        input.add(new Atom("a"));

        Vector<Atom> output = new Vector<Atom>();
        output.add(new Atom("city(1)"));
        output.add(new Atom("city(1)"));
        output.add(new Atom("city(2)"));
        output.add(new Atom("city(2)"));

        examples.addExample(input, output);
        
        Vector<Atom> input2 = new Vector<Atom>();
        input2.add(new Atom("a"));
        input2.add(new Atom("a"));
        input2.add(new Atom("a"));
        input2.add(new Atom("a"));

        Vector<Atom> output2 = new Vector<Atom>();
        output2.add(new Atom("city(2)"));
        output2.add(new Atom("city(2)"));
        output2.add(new Atom("city(2)"));
        output2.add(new Atom("city(2)"));

        examples.addExample(input2, output2);
        
        Vector<Atom> input3 = new Vector<Atom>();
        input3.add(new Atom("b"));
        input3.add(new Atom("b"));
        input3.add(new Atom("b"));
        input3.add(new Atom("b"));

        Vector<Atom> output3 = new Vector<Atom>();
        output3.add(new Atom("city(1)"));
        output3.add(new Atom("city(1)"));
        output3.add(new Atom("city(1)"));
        output3.add(new Atom("city(1)"));

        examples.addExample(input3, output3);



        WindowMaker wm = new WindowMaker(3, null, null);
        PrologRegressionTreeTrainer trainer = new PrologRegressionTreeTrainer(14, 2, bgknowledge, wm
                .getOutputFields());

        CRF crf0 = new CRF(examples.getClassAtoms(), trainer, wm, new LogicalCountingTreeTrainer(5, 1), 0);

        crf0.train(examples, 1);

        assertEquals(output, crf0.classifyViterbi(input));
        assertEquals(output, crf0.classifyFB(input));
        assertEquals(output2, crf0.classifyViterbi(input2));
        assertEquals(output2, crf0.classifyFB(input2));
        assertEquals(output3, crf0.classifyViterbi(input3));
        assertEquals(output3, crf0.classifyFB(input3));
    }

    public void testTrain_11() {
        SimpleExampleContainer examples = new SimpleExampleContainer(classAtom1);
        examples.addExample(input1, output1);
        CRF crf0 = new CRF(examples.getClassAtoms(), new LogicalRegressionTreeTrainer(14, 1), 7,
                new LogicalCountingTreeTrainer(5, 1));

        crf0.train(examples, 1);
        assertEquals(output1, crf0.classifyFB(input1));
        assertEquals(output1, crf0.classifyViterbi(input1));
    }

    public void testTaggingWithPartialKnownOutputs() throws ParseException {
        Vector<Atom> input1 = new Vector<Atom>(6);
        Vector<Atom> output1 = new Vector<Atom>(6);

        input1.add(new Atom("aa"));
        input1.add(new Atom("ba"));
        input1.add(new Atom("bb"));
        input1.add(new Atom("aa"));
        input1.add(new Atom("ba"));
        input1.add(new Atom("ab"));

        output1.add(new Atom("aa"));
        output1.add(new Atom("ab"));
        output1.add(new Atom("bb"));
        output1.add(new Atom("aa"));
        output1.add(new Atom("ab"));
        output1.add(new Atom("ab"));

        Vector<Atom> classAtoms = new Vector<Atom>();
        classAtoms.add(new Atom("aa"));
        classAtoms.add(new Atom("ab"));
        classAtoms.add(new Atom("bb"));

        Vector<Atom> knownPositions = new Vector<Atom>(6);
        knownPositions.add(new Atom("aa"));
        knownPositions.add(null);
        knownPositions.add(new Atom("bb"));
        knownPositions.add(new Atom("aa"));
        knownPositions.add(null);
        knownPositions.add(null);

        SimpleExampleContainer examples = new SimpleExampleContainer(classAtoms);
        examples.addExample(input1, output1);

        CRF crf0 = new CRF(examples.getClassAtoms(), new LogicalRegressionTreeTrainer(1, 7), 3,
                new LogicalCountingTreeTrainer(5, 1));

        crf0.train(examples, 1);
        Logger.getLogger(getClass()).info(crf0.classifyFB(input1));
        Logger.getLogger(getClass()).info(crf0.classifyFB(input1, knownPositions));

        Logger.getLogger(getClass()).info(crf0.classifyViterbi(input1));
        Logger.getLogger(getClass()).info(crf0.classifyViterbi(input1, knownPositions));

    }

    public void testTaggingWithPartialKnownOutputs2() throws ParseException {
        Vector<Atom> input1 = new Vector<Atom>(6);
        Vector<Atom> output1 = new Vector<Atom>(6);
        Vector<Atom> input2 = new Vector<Atom>(6);
        Vector<Atom> output2 = new Vector<Atom>(6);

        input1.add(new Atom("aa"));
        input1.add(new Atom("ba"));
        input1.add(new Atom("bb"));
        input1.add(new Atom("aa"));
        input1.add(new Atom("ba"));
        input1.add(new Atom("ab"));

        output1.add(new Atom("c(1)"));
        output1.add(new Atom("c(1)"));
        output1.add(new Atom("c(1)"));
        output1.add(new Atom("c(1)"));
        output1.add(new Atom("c(1)"));
        output1.add(new Atom("c(1)"));

        input2.add(new Atom("aa"));
        input2.add(new Atom("ba"));
        input2.add(new Atom("bb"));
        input2.add(new Atom("aa"));
        input2.add(new Atom("ba"));
        input2.add(new Atom("ab"));

        /*
         * input2.add(new Atom("ba")); input2.add(new Atom("aa"));
         * input2.add(new Atom("aa")); input2.add(new Atom("ba"));
         * input2.add(new Atom("ab")); input2.add(new Atom("bb"));
         */

        output2.add(new Atom("c(2)"));
        output2.add(new Atom("c(2)"));
        output2.add(new Atom("c(2)"));
        output2.add(new Atom("c(2)"));
        output2.add(new Atom("c(2)"));
        output2.add(new Atom("c(2)"));

        Vector<Atom> classAtoms = new Vector<Atom>();
        classAtoms.add(new Atom("c(1)"));
        classAtoms.add(new Atom("c(2)"));

        Vector<Atom> knownPositions1 = new Vector<Atom>(6);
        knownPositions1.add(new Atom("c(1)"));
        knownPositions1.add(null);
        knownPositions1.add(null);
        knownPositions1.add(null);
        knownPositions1.add(null);
        knownPositions1.add(null);

        Vector<Atom> knownPositions2 = new Vector<Atom>(6);
        knownPositions2.add(null);
        knownPositions2.add(null);
        knownPositions2.add(null);
        knownPositions2.add(null);
        knownPositions2.add(null);
        knownPositions2.add(null);

        SimpleExampleContainer examples = new SimpleExampleContainer(classAtoms);
        examples.addExample(input1, output1);
        examples.addExample(input2, output2);

        CRF crf0 = new CRF(examples.getClassAtoms(), new LogicalRegressionTreeTrainer(1, 1), 3,
                new LogicalCountingTreeTrainer(5, 1));

        crf0.train(examples, 3);
        Logger.getLogger(getClass()).info("Forward-Backward 1");
        Logger.getLogger(getClass()).info(crf0.classifyFB(input1));
        Logger.getLogger(getClass()).info(crf0.classifyFB(input1, knownPositions1));
        Logger.getLogger(getClass()).info("Viterbi 1");
        Logger.getLogger(getClass()).info(crf0.classifyViterbi(input1));
        Logger.getLogger(getClass()).info(crf0.classifyViterbi(input1, knownPositions1));
        Logger.getLogger(getClass()).info("Forward-Backward 2");
        Logger.getLogger(getClass()).info(crf0.classifyFB(input2));
        Logger.getLogger(getClass()).info(crf0.classifyFB(input2, knownPositions2));
        Logger.getLogger(getClass()).info("Viterbi 2");
        Logger.getLogger(getClass()).info(crf0.classifyViterbi(input2));
        Logger.getLogger(getClass()).info(crf0.classifyViterbi(input2, knownPositions2));

    }

    public void testRandomSequences_withoutSchema() throws ParseException {
        int examplecount = 15;
        int sequencelength = 10;
        int inatoms = 4;
        int outatoms = 4;

        Random rand = new Random(546488);

        Vector<Atom> classAtom = new Vector<Atom>(outatoms);
        for (int i = 0; i < outatoms; i++) {
            classAtom.add(new Atom(new Constant("b" + i)));
        }

        SimpleExampleContainer examples = new SimpleExampleContainer(classAtom);

        int cl = 0;
        for (int i = 0; i < examplecount; i++) {
            List<Atom> input = new Vector<Atom>(sequencelength);
            List<Atom> output = new Vector<Atom>(sequencelength);
            for (int j = 0; j < sequencelength; j++) {
                int r1 = rand.nextInt(inatoms);
                int r2 = rand.nextInt(r1 + 1);
                input.add(new Atom("a" + Integer.toString(r1)));
                // output.add(new Atom("b" + rand.nextInt(outatoms)));
                output.add(new Atom("b" + Integer.toString(r2)));
            }

            examples.addExample(input, output);
        }

        CRF c = new CRF(examples.getClassAtoms(), new LogicalRegressionTreeTrainer(8, 5), 1,
                new LogicalCountingTreeTrainer(5, 1));
        c.train(examples, 10);
        for (int i = 0; i < examplecount; i++) {
            Logger.getLogger(this.getClass()).info("in     : " + examples.getInputSequence(i));
            Logger.getLogger(this.getClass()).info("out    : " + examples.getOutputSequence(i));
            Logger.getLogger(this.getClass()).info("out_fb : " + c.classifyFB(examples.getInputSequence(i)));
            Logger.getLogger(this.getClass()).info(
                    "out_vi : " + c.classifyViterbi(examples.getInputSequence(i)));
        }
    }

    public void testRandomSequences2_withSchema() throws ParseException {
        int examplecount = 15;
        int sequencelength = 10;
        int classes = 4;

        Random rand = new Random(8856465);

        Vector<Atom> classAtom = new Vector<Atom>(classes);
        for (int i = 0; i < classes; i++) {
            classAtom.add(new Atom("b(" + i + ")"));
        }

        SimpleExampleContainer examples = new SimpleExampleContainer(classAtom);

        int cl = 0;
        for (int i = 0; i < examplecount; i++) {
            List<Atom> input = new Vector<Atom>(sequencelength);
            List<Atom> output = new Vector<Atom>(sequencelength);
            for (int j = 0; j < sequencelength; j++) {
                int r_class = rand.nextInt(classes);
                int r_other = rand.nextInt(100);
                input.add(new Atom("a(" + Integer.toString(r_class) + "," + Integer.toString(r_other) + ")"));
                output.add(new Atom("b(" + Integer.toString(r_class) + ")"));
            }

            examples.addExample(input, output);
        }

        WindowMaker wm = new WindowMaker(1);

        CRF c = new CRF(examples.getClassAtoms(), new LogicalRegressionTreeTrainer(8, 5, XMLInput
                .readSchemata("stuff/schemata2.xml"), wm.getFieldTypes()), wm,
                new LogicalCountingTreeTrainer(5, 1), 123456);
        c.train(examples, 4);
        for (int i = 0; i < examplecount; i++) {            
            Logger.getLogger(this.getClass()).info("in     : " + examples.getInputSequence(i));
            Logger.getLogger(this.getClass()).info("out    : " + examples.getOutputSequence(i));
            Logger.getLogger(this.getClass()).info("out_fb : " + c.classifyFB(examples.getInputSequence(i)));
            Logger.getLogger(this.getClass()).info(
                    "out_vi : " + c.classifyViterbi(examples.getInputSequence(i)));
        }
     /*   for (int y=0;y<10;y++) {
            c.trainOneStep(examples);
        double loglikelihood = 0.0;
        for (int j=0; j<examples.size(); j++) {
            loglikelihood += c.getLogLikelihood(examples.getInputSequence(j),examples.getOutputSequence(j));
        }
        Logger.getLogger(this.getClass()).info("log-Likelihood : " + loglikelihood);
        }*/
    }

    public void testDummySequences() throws ParseException {
        Vector<Atom> classAtoms = new Vector<Atom>();
        classAtoms.add(new Atom("a"));
        classAtoms.add(new Atom("b"));
        classAtoms.add(new Atom("c"));

        SimpleExampleContainer e = new SimpleExampleContainer(classAtoms);
        Vector<Atom> input = new Vector<Atom>(10);
        Vector<Atom> input2 = new Vector<Atom>(10);
        Vector<Atom> input3 = new Vector<Atom>(10);
        Vector<Atom> output = new Vector<Atom>(10);
        Vector<Atom> output2 = new Vector<Atom>(10);
        Vector<Atom> output3 = new Vector<Atom>(10);

        input.add(new Atom("x"));
        input.add(new Atom("x"));
        input.add(new Atom("x"));
        input.add(new Atom("x"));
        input.add(new Atom("x"));
        input.add(new Atom("x"));
        input.add(new Atom("x"));
        input.add(new Atom("x"));
        input.add(new Atom("x"));
        input.add(new Atom("x"));

        input2.add(new Atom("y"));
        input2.add(new Atom("y"));
        input2.add(new Atom("y"));
        input2.add(new Atom("y"));
        input2.add(new Atom("y"));
        input2.add(new Atom("y"));
        input2.add(new Atom("y"));
        input2.add(new Atom("y"));
        input2.add(new Atom("y"));
        input2.add(new Atom("y"));

        input3.add(new Atom("y"));
        input3.add(new Atom("z"));
        input3.add(new Atom("y"));
        input3.add(new Atom("z"));
        input3.add(new Atom("y"));
        input3.add(new Atom("z"));
        input3.add(new Atom("y"));
        input3.add(new Atom("z"));
        input3.add(new Atom("y"));
        input3.add(new Atom("z"));

        output.add(new Atom("a"));
        output.add(new Atom("a"));
        output.add(new Atom("a"));
        output.add(new Atom("a"));
        output.add(new Atom("a"));
        output.add(new Atom("a"));
        output.add(new Atom("a"));
        output.add(new Atom("a"));
        output.add(new Atom("a"));
        output.add(new Atom("a"));

        output2.add(new Atom("b"));
        output2.add(new Atom("b"));
        output2.add(new Atom("b"));
        output2.add(new Atom("b"));
        output2.add(new Atom("b"));
        output2.add(new Atom("b"));
        output2.add(new Atom("b"));
        output2.add(new Atom("b"));
        output2.add(new Atom("b"));
        output2.add(new Atom("b"));

        output3.add(new Atom("c"));
        output3.add(new Atom("c"));
        output3.add(new Atom("c"));
        output3.add(new Atom("a"));
        output3.add(new Atom("a"));
        output3.add(new Atom("a"));
        output3.add(new Atom("a"));
        output3.add(new Atom("c"));
        output3.add(new Atom("c"));
        output3.add(new Atom("c"));

        e.addExample(input, output);
        e.addExample(input2, output2);
        e.addExample(input3, output3);

        LogicalRegressionTreeTrainer t = new LogicalRegressionTreeTrainer(5, 1);
        CRF crf = new CRF(classAtoms, t, 5, new LogicalCountingTreeTrainer(5, 1));

        crf.train(e, 6);
        
        crf.trainOneStep(e);

        assertEquals(output, crf.classifyFB(input));
        assertEquals(output, crf.classifyViterbi(input));

        assertEquals(output2, crf.classifyFB(input2));
        assertEquals(output2, crf.classifyViterbi(input2));

        assertEquals(output3, crf.classifyFB(input3));
        assertEquals(output3, crf.classifyViterbi(input3));
    }

    // FIXME remove the dontuse
    public void dontusetestWithVariables1() throws ParseException {
        Vector<Atom> classAtoms = new Vector<Atom>(2);
        classAtoms.add(new Atom("e(X)"));
        classAtoms.add(new Atom("c(X,Y)"));

        int n = 700;
        int length = 10;
        int groundSymbols = 4;
        int maxruns = 10;

        SimpleExampleContainer ex = makeExample(n, length, new Random(787837), classAtoms, groundSymbols);
        SimpleExampleContainer ex2 = makeExample(10, length, new Random(234234), classAtoms, groundSymbols);

        RegressionModelTrainer<List<Atom>> trainer = new TrainerWrapper<List<Atom>>(
                new LogicalRegressionTreeTrainer(5, 2000));

        CRF crf = new CRF(classAtoms, trainer, 5, new LogicalCountingTreeTrainer(5, 1));

        for (int run = 0; run < maxruns; run++) {
            Logger.getLogger(getClass()).info("Run step " + (run + 1) + " of " + maxruns);
            crf.trainOneStep(ex);
            int count = 0;
            for (int i = 0; i < ex.size(); i++) {
                // Logger.getLogger(this.getClass()).info(ex.getInputSequence(i));
                // Logger.getLogger(this.getClass()).info(ex.getOutputSequence(i));
                // Logger.getLogger(this.getClass()).info(crf.classifyFB(ex.getInputSequence(i)));
                // Logger.getLogger(this.getClass()).info("------");
                count += getDifferentElements(ex.getOutputSequence(i), crf.classifyFB(ex.getInputSequence(i)));
            }
            Logger.getLogger(this.getClass()).info("Error on trainingset " + (double) count / ex.size());
            NumberStorage.add("errortrain", (double) count / ex.size());

            count = 0;
            for (int i = 0; i < ex2.size(); i++) {
                // Logger.getLogger(this.getClass()).info(ex.getInputSequence(i));
                // Logger.getLogger(this.getClass()).info(ex.getOutputSequence(i));
                // Logger.getLogger(this.getClass()).info(crf.classifyFB(ex.getInputSequence(i)));
                // Logger.getLogger(this.getClass()).info("------");
                count += getDifferentElements(ex2.getOutputSequence(i), crf.classifyFB(ex2
                        .getInputSequence(i)));
            }
            Logger.getLogger(this.getClass()).info("Error on testset " + (double) count / ex2.size());
            NumberStorage.add("errortest", (double) count / ex2.size());
        }

        Logger.getLogger(getClass()).info("Error on trainset\n" + NumberStorage.getValuesFor("errortrain"));
        Logger.getLogger(getClass()).info("Error on testset\n" + NumberStorage.getValuesFor("errortest"));

    }

    public SimpleExampleContainer makeExample(int n, int length, Random rand, Vector<Atom> classAtoms,
            int groundSymbols) throws ParseException {

        SimpleExampleContainer ex = new SimpleExampleContainer(classAtoms);

        for (int i = 0; i < n; i++) {
            Vector<Atom> input = new Vector<Atom>(length);
            Vector<Atom> output = new Vector<Atom>(length);
            for (int j = 0; j < length; j++) {
                input.add(new Atom(new NumberConstant(rand.nextInt(groundSymbols))));
            }
            output.add(new Atom("e(" + input.get(0) + ")"));
            for (int j = 1; j < length; j++) {
                if (input.get(j).equals(input.get(j - 1))) {
                    output.add(new Atom("e(" + input.get(j) + ")"));
                } else {
                    output.add(new Atom("c(" + input.get(j - 1) + "," + input.get(j) + ")"));
                }
            }
            ex.addExample(input, output);
        }

        return ex;

    }

    private int getDifferentElements(List a, List b) {
        int count = 0;
        for (int i = 0; i < a.size(); i++) {
            if (!a.get(i).equals(b.get(i))) {
                count++;
            }
        }
        return count;
    }

    public void testSerialization() throws Exception {
        Vector<Atom> classAtoms = new Vector<Atom>();
        classAtoms.add(new Atom("a"));
        classAtoms.add(new Atom("b"));
        classAtoms.add(new Atom("c"));

        SimpleExampleContainer e = new SimpleExampleContainer(classAtoms);
        Vector<Atom> input = new Vector<Atom>(10);

        Vector<Atom> output = new Vector<Atom>(10);

        input.add(new Atom("x"));
        input.add(new Atom("x"));

        output.add(new Atom("a"));
        output.add(new Atom("a"));

        e.addExample(input, output);

        LogicalRegressionTreeTrainer t = new LogicalRegressionTreeTrainer(5, 1);
        CRF crf = new CRF(classAtoms, t, 5, new LogicalCountingTreeTrainer(5, 1));

        crf.train(e, 6);

        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oas = new ObjectOutputStream(baos);
        oas.writeObject(crf);

        ByteArrayInputStream bais = new ByteArrayInputStream(baos.toByteArray());
        ObjectInputStream ois = new ObjectInputStream(bais);
        Object o1 = ois.readObject();

        assertTrue(o1 instanceof CRF);

        CRF crf2 = (CRF) o1;

        assertEquals(crf.classifyFB(input), crf2.classifyFB(input));
        assertEquals(crf.classifyViterbi(input), crf2.classifyViterbi(input));
    }

}
