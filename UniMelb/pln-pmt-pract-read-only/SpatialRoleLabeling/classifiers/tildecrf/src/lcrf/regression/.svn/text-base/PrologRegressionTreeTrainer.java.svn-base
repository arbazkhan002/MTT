/**
 * 
 */
package lcrf.regression;

import java.io.Serializable;
import java.io.StringReader;
import java.util.List;
import java.util.Vector;

import lcrf.logic.Atom;
import lcrf.logic.Variable;
import lcrf.stuff.FileWriter;

import org.apache.log4j.Logger;

import xprolog.Engine;
import xprolog.ParseException;

/**
 * @author bgutmann
 */
public class PrologRegressionTreeTrainer implements RegressionModelTrainer<List<Atom>>, Serializable {
    private static final long serialVersionUID = 3257008743811134257L;

    protected static final String fixedBGPart = "listsucceds([],Test,E):-succeds(Test,E)."
            + "listsucceds([H|Tail],Test,E):-succeds(H,E),listsucceds(Tail,Test,E).";
            

    // this is the default value for a tree, that es returned when one
    // traines a tree from zero examples
    private static final double defaultValue = 0.0;

    // if the depth of the current node is below this constant
    // we try to split the examples further
    private int maxTreeDepth;

    // if we have at least this examples we try to split them
    // 2 is the lower bound for this constant
    private int minLeafSize;

    // temp variables for training
    private boolean[] bestmapping;

    private boolean[] mapping;

    private Engine prologEngine;

    private String backgroundKnowledge;

    /**
     * 
     * @param maxTreeDepth
     * @param minLeafSize
     * @param windowSize
     * @param backgroundKnowledge
     * @param outputPositions  e.g. <pre>[1,2,3,4,5,6]</pre>
     */
    public PrologRegressionTreeTrainer(int maxTreeDepth, int minLeafSize, String backgroundKnowledge,String outputPositions) {
        assert minLeafSize > 1;
        assert maxTreeDepth >= 0;
        assert backgroundKnowledge != null;

        this.maxTreeDepth = maxTreeDepth;
        this.minLeafSize = minLeafSize;

        this.backgroundKnowledge = PrologRegressionTreeTrainer.fixedBGPart.substring(0).concat(
                backgroundKnowledge.substring(0)).concat("outputPositions(").concat(outputPositions).concat(").");

        try {
            prologEngine = new Engine(new StringReader(this.backgroundKnowledge));
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    private Iterable<String> getTestIterator(List<RegressionExample<List<Atom>>> examples,
            List<Variable> boundedVars, int actualDepth) {

        return null;
    }

    public RegressionModel<List<Atom>> trainFromExamples(List<RegressionExample<List<Atom>>> examples) {
        if (examples == null || examples.size() == 0) {
            return new PrologRegressionTree(defaultValue, null, null, null, null);
        }


        double examplesSum = 0.0;
        for (int i = 0; i < examples.size(); i++) {
            examplesSum += examples.get(i).value;

            //tansform the content into prolog notation
            String term = "[";
            boolean notfirst = false;
            for (Atom atom : examples.get(i).content) {
                if (notfirst) {
                    term = term.concat(",");
                }
                notfirst = true;
                term = term.concat(atom.toString());
            }
            term = term.concat("]))");
            
            examples.get(i).auxObject = term;

        }

        double average = examplesSum / examples.size();

        // prapare global variables
        this.bestmapping = new boolean[examples.size()];
        this.mapping = new boolean[examples.size()];

        PrologRegressionTree t = trainIntern(examples, new Vector<Variable>(30), 0, average, "");

        // clear global variables
        this.bestmapping = null;
        this.mapping = null;

        FileWriter.writeToFile("models/prt", ".dot", t.toDotString());

        return t;
    }

    private PrologRegressionTree trainIntern(List<RegressionExample<List<Atom>>> examples,
            Vector<Variable> boundedVars, int depth, double average, String testsSoFar) {

        if (depth >= maxTreeDepth || examples.size() < minLeafSize) {
            return new PrologRegressionTree(average, null, null, null, null);
        }

        double bestsumsquarederror = Double.MAX_VALUE;
        String bestTest = null;

        int bestTrueExamplesCount = 0;
        int bestFalseExamplesCount = 0;
        double bestTrueExamplesSum = 0;
        double bestFalseExamplesSum = 0;

        
        Logger.getLogger(getClass()).debug("Start finding possible Tests");
        Vector<String> possibleTests = new Vector<String>();
        try {
            if (prologEngine.setQuery("test(X)")) {
                do {
                    possibleTests.add(prologEngine.answer().term.toString());
                } while (prologEngine.more());
            }
        } catch (ParseException e) {
            // this should never happen :)
            throw new RuntimeException(e);
        }
        Logger.getLogger(getClass()).debug(Integer.toString(possibleTests.size())+" tests found.");
        
        for (String test : possibleTests) {
            int trueExamplesCount = 0;
            int falseExamplesCount = 0;
            double trueExamplesSum = 0;
            double falseExamplesSum = 0;
            
            String queryPrefix = "";
            
            if (testsSoFar.equals("")) {
                queryPrefix = "succeds("+test+",";
            } else{
               queryPrefix = "listsucceds([" + testsSoFar + "]," + test + ",";
            }

            // split examples into true/false-parts
            Logger.getLogger(getClass()).debug("Test : "+test.toString());
            for (int i = 0; i < examples.size(); i++) {
                String query = queryPrefix + examples.get(i).auxObject.toString() + ")";

                try {
                    if (prologEngine.setQuery(query)) {
                        mapping[i] = true;
                        trueExamplesCount++;
                        trueExamplesSum += examples.get(i).value;
                    } else {
                        mapping[i] = false;
                        falseExamplesCount++;
                        falseExamplesSum += examples.get(i).value;
                    }
                } catch (ParseException e) {
                    // this should never happen :)
                    throw new RuntimeException(e);
                }            
            }

            if (trueExamplesCount == 0 || falseExamplesCount == 0) {
                // using this splitatom doesnt make sense
                continue;
            }

            double trueExamplesAverage = trueExamplesSum / trueExamplesCount;
            double falseExamplesAverage = falseExamplesSum / falseExamplesCount;
            double sumsquarederror = 0.0;

            for (int i = 0; i < examples.size(); i++) {
                double val = examples.get(i).value
                        - (mapping[i] ? trueExamplesAverage : falseExamplesAverage);
                sumsquarederror += val * val;
            }

            if (sumsquarederror < bestsumsquarederror) {
                boolean[] tmp = mapping;
                mapping = bestmapping;
                bestmapping = tmp;

                bestsumsquarederror = sumsquarederror;
                bestTest = test;

                bestTrueExamplesCount = trueExamplesCount;
                bestFalseExamplesCount = falseExamplesCount;
                bestTrueExamplesSum = trueExamplesSum;
                bestFalseExamplesSum = falseExamplesSum;
            }
        }

        if (bestTrueExamplesCount == 0 || bestFalseExamplesCount == 0) {
            return new PrologRegressionTree(average, null, null, null, null);
        }

        // split training data for both subtrees
        List<RegressionExample<List<Atom>>> trueExamples = new Vector<RegressionExample<List<Atom>>>(
                bestTrueExamplesCount);
        List<RegressionExample<List<Atom>>> falseExamples = new Vector<RegressionExample<List<Atom>>>(
                bestTrueExamplesCount);

        for (int i = 0; i < examples.size(); i++) {
            RegressionExample<List<Atom>> ex = examples.get(i);
            if (bestmapping[i] == true) {
                trueExamples.add(ex);
            } else {
                falseExamples.add(ex);
            }
        }

        // free memory
        examples.clear();
        examples = null;

        String testsSoFarFalseTree = (testsSoFar.equals("")) ? "not(" + bestTest + ")" : testsSoFar
                + ", not(" + bestTest + ")";
        String testsSoFarTrueTree = (testsSoFar.equals("")) ? bestTest : testsSoFar + ", " + bestTest;

        int sizeold = falseExamples.size();

        PrologRegressionTree falseSubTree = trainIntern(falseExamples, boundedVars, depth + 1,
                bestFalseExamplesSum / bestFalseExamplesCount, testsSoFarFalseTree);
        falseSubTree.dirty_ExampleSize = sizeold;

        // free memory
        falseExamples.clear();
        falseExamples = null;

        sizeold = trueExamples.size();
        PrologRegressionTree trueSubTree = trainIntern(trueExamples, boundedVars, depth + 1,
                bestTrueExamplesSum / bestTrueExamplesCount, testsSoFarTrueTree);
        trueSubTree.dirty_ExampleSize = sizeold;

        // free memory
        trueExamples.clear();
        trueExamples = null;

        return new PrologRegressionTree(average, bestTest, trueSubTree, falseSubTree, prologEngine);
    }

    public String toString() {
        return "LogicalRegressionTreeTrainer(" + maxTreeDepth + "," + minLeafSize + ")";
    }

}
