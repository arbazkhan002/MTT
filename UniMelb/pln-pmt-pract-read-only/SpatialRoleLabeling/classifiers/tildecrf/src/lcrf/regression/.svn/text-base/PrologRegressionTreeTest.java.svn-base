package lcrf.regression;

import java.io.StringReader;
import java.util.List;
import java.util.Vector;

import junit.framework.TestCase;
import lcrf.logic.Atom;
import lcrf.logic.Constant;

import org.apache.log4j.BasicConfigurator;

import xprolog.Engine;
import xprolog.ParseException;

public class PrologRegressionTreeTest extends TestCase {
    private static String bgknowledge = "test(same)." + "test(outis(Y)) :- member(Y,[class1,class2,class3])."
            + "test(outoldis(Y)) :- test(outis(Y))." + "succeds(test(same),[X,X|_])."
            + "succeds(test(outis(X)),[_,X|_])." + "succeds(test(outoldis(X)),[X,_|_])."
            + "succeds(not(Test),X):-not(succeds(Test,X)).";

    private Engine engine;

    public void setUp() throws ParseException {
        BasicConfigurator.resetConfiguration();
        BasicConfigurator.configure();
        engine = new Engine(new StringReader(PrologRegressionTreeTrainer.fixedBGPart.substring(0).concat(
                bgknowledge.substring(0).concat("outputPositions([])."))));
    }

    public void testTrain1() {
        Vector<RegressionExample<List<Atom>>> examples = new Vector<RegressionExample<List<Atom>>>();
        Vector<Atom> ex1content = new Vector<Atom>();
        ex1content.add(new Atom(new Constant("class2")));
        ex1content.add(new Atom(new Constant("class2")));
        examples.add(new RegressionExample<List<Atom>>(ex1content, 0));

        Vector<Atom> ex2content = new Vector<Atom>();
        ex2content.add(new Atom(new Constant("class1")));
        ex2content.add(new Atom(new Constant("class2")));
        examples.add(new RegressionExample<List<Atom>>(ex2content, 100));

        Vector<Atom> ex3content = new Vector<Atom>();
        ex3content.add(new Atom(new Constant("class3")));
        ex3content.add(new Atom(new Constant("class3")));
        examples.add(new RegressionExample<List<Atom>>(ex3content, 101));

        PrologRegressionTreeTrainer trainer = new PrologRegressionTreeTrainer(10, 2, bgknowledge, "[]");

        RegressionModel<List<Atom>> trainedTree = trainer.trainFromExamples(examples);

        PrologRegressionTree trueTree2 = new PrologRegressionTree(0.0, null, null, null, null);
        PrologRegressionTree falseTree2 = new PrologRegressionTree(100.0, null, null, null, null);
        PrologRegressionTree trueTree = new PrologRegressionTree(0, "test(same)", trueTree2, falseTree2,
                engine);
        PrologRegressionTree falseTree = new PrologRegressionTree(101.0, null, null, null, null);
        RegressionModel<List<Atom>> referenceTree = new PrologRegressionTree(0, "test(outis(class2))",
                trueTree, falseTree, engine);

        assertEquals(trainedTree, referenceTree);
        assertEquals(referenceTree, trainedTree);

        assertEquals(trainedTree.getValueFor(ex1content), 0.0, 0.0);
        assertEquals(trainedTree.getValueFor(ex2content), 100.0, 0.0);
        assertEquals(trainedTree.getValueFor(ex3content), 101.0, 0.0);

        assertEquals(referenceTree.getValueFor(ex1content), 0.0, 0.0);
        assertEquals(referenceTree.getValueFor(ex2content), 100.0, 0.0);
        assertEquals(referenceTree.getValueFor(ex3content), 101.0, 0.0);
    }
    
    public void testTrain2() {
        Vector<RegressionExample<List<Atom>>> examples = new Vector<RegressionExample<List<Atom>>>();
        Vector<Atom> ex1content = new Vector<Atom>();
        ex1content.add(new Atom(new Constant("class1")));
        ex1content.add(new Atom(new Constant("class1")));
        examples.add(new RegressionExample<List<Atom>>(ex1content, 1));

        Vector<Atom> ex2content = new Vector<Atom>();
        ex2content.add(new Atom(new Constant("class1")));
        ex2content.add(new Atom(new Constant("class2")));
        examples.add(new RegressionExample<List<Atom>>(ex2content, 10));

        Vector<Atom> ex3content = new Vector<Atom>();
        ex3content.add(new Atom(new Constant("class2")));
        ex3content.add(new Atom(new Constant("class1")));
        examples.add(new RegressionExample<List<Atom>>(ex3content, 100));
        
        Vector<Atom> ex4content = new Vector<Atom>();
        ex4content.add(new Atom(new Constant("class2")));
        ex4content.add(new Atom(new Constant("class2")));
        examples.add(new RegressionExample<List<Atom>>(ex4content, 1000));

        PrologRegressionTreeTrainer trainer = new PrologRegressionTreeTrainer(10, 1, bgknowledge, "[]");

        RegressionModel<List<Atom>> trainedTree = trainer.trainFromExamples(examples);

        PrologRegressionTree trueTreeT = new PrologRegressionTree(1.0, null, null, null, null);
        PrologRegressionTree falseTreeT = new PrologRegressionTree(10.0, null, null, null, null);
        PrologRegressionTree trueTree = new PrologRegressionTree(0, "test(same)", trueTreeT, falseTreeT,
                engine);
        
        PrologRegressionTree trueTreeF = new PrologRegressionTree(1000.0, null, null, null, null);
        PrologRegressionTree falseTreeF = new PrologRegressionTree(100.0, null, null, null, null);
        PrologRegressionTree falseTree = new PrologRegressionTree(0, "test(same)", trueTreeF, falseTreeF,
                engine);
        
        RegressionModel<List<Atom>> referenceTree = new PrologRegressionTree(0, "test(outoldis(class1))",
                trueTree, falseTree, engine);

        assertEquals(trainedTree, referenceTree);
        assertEquals(referenceTree, trainedTree);

        assertEquals(trainedTree.getValueFor(ex1content), 1.0, 0.0);
        assertEquals(trainedTree.getValueFor(ex2content), 10.0, 0.0);
        assertEquals(trainedTree.getValueFor(ex3content), 100.0, 0.0);
        assertEquals(trainedTree.getValueFor(ex4content), 1000.0, 0.0);

        assertEquals(referenceTree.getValueFor(ex1content), 1.0, 0.0);
        assertEquals(referenceTree.getValueFor(ex2content), 10.0, 0.0);
        assertEquals(referenceTree.getValueFor(ex3content), 100.0, 0.0);
        assertEquals(referenceTree.getValueFor(ex4content), 1000.0, 0.0);
    }


}
