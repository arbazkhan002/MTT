/**
 * 
 */
package lcrf.counting;

import java.io.Serializable;
import java.util.List;
import java.util.Vector;

import lcrf.logic.Atom;
import lcrf.logic.SchemaUnificationJobGenerator;
import lcrf.logic.Substitutions;
import lcrf.logic.TermSchema;
import lcrf.logic.UnificationJob;
import lcrf.logic.UnificationJobGenerator;
import lcrf.logic.Unificator;
import lcrf.logic.Variable;
import lcrf.stuff.FileWriter;

/**
 * @author bgutmann
 * 
 */
public class LogicalCountingTreeTrainer implements Serializable {
    private static final long serialVersionUID = 3258416114399852856L;

    private int maxTreeDepth;

    private int minLeafSize;

    private List<TermSchema> schemata;

    // temp variables for training
    private Substitutions[] bestsubsts;

    private Substitutions[] substs;

    public LogicalCountingTreeTrainer(int maxTreeDepth, int minLeafSize) {
        this(maxTreeDepth, minLeafSize, null);
    }

    public LogicalCountingTreeTrainer(int maxTreeDepth, int minLeafSize, List<TermSchema> schemata) {
        if (minLeafSize < 1) {
            throw new IllegalArgumentException(Integer.toString(minLeafSize));
        }

        if (maxTreeDepth < 0) {
            throw new IllegalArgumentException(Integer.toString(maxTreeDepth));
        }
        this.maxTreeDepth = maxTreeDepth;
        this.minLeafSize = minLeafSize;
        this.schemata = schemata;
    }

    private Iterable<UnificationJob> getJobIterator(List<CountingExample> examples, List<Variable> boundedVars,int actualDepth) {
        assert examples != null;
        assert examples.size() > 0;

        if (schemata == null) {
            Vector<Atom> differentAtoms = new Vector<Atom>(100);
            for (int i = 0; i < examples.size(); i++) {
                List<Atom> example = examples.get(i).content;
                for (int j = 0; j < example.size(); j++) {
                    if (!differentAtoms.contains(example.get(j))) {
                        differentAtoms.add(example.get(j));
                    }
                }
            }
            return new UnificationJobGenerator(differentAtoms, examples.get(0).content.size());
        }

        return new SchemaUnificationJobGenerator(examples.get(0).content.size(), schemata, boundedVars,actualDepth);
    }

    public LogicalCountingTree trainFromExamples(List<CountingExample> examples, int countingClasses) {
        if (examples == null || examples.size() == 0) {
            int[] countArray = new int[countingClasses];
            for (int i = 0; i < countingClasses; i++) {
                countArray[i] = 1;
            }
            return new LogicalCountingTree(countArray, null, null, null);
        }

        // prapare global variables
        bestsubsts = new Substitutions[examples.size()];
        substs = new Substitutions[examples.size()];

        for (CountingExample ex : examples) {
            if (ex.number < 0 || ex.number >= countingClasses) {
                throw new IllegalArgumentException(ex.toString());
            }
            ex.auxObject = new Substitutions();
        }

        LogicalCountingTree t = trainIntern(examples, new Vector<Variable>(30), 0, countingClasses);

        // logger.info("Unificator Cache-Hit/Cache-Miss : " +
        // Unificator.hitcounter + "/" + Unificator.misscounter);
        // logger.info("Substitutions Hit/Miss : " + Substitutions.hitcounter +
        // "/" + Substitutions.misscounter);
        // logger.info("Substitutions Clone/Modify : " +
        // Substitutions.clonecounter + "/" + Substitutions.modifycounter);

        FileWriter.writeToFile("models/lct", ".dot", t.toDotString());

        return t;
    }

    private int[] countClasses(List<CountingExample> examples, int countingClasses) {
        int[] result = new int[countingClasses];
        for (int i = 0; i < examples.size(); i++) {
            result[examples.get(i).number]++;
        }

        return result;
    }

    private double calcEntropy(List<CountingExample> examples, int countingClasses) {
        int[] counts = countClasses(examples, countingClasses);
        double result = 0.0;
        for (int i = 0; i < countingClasses; i++) {

            if (counts[i] > 0) {
                result -= (double) counts[i] / (double) examples.size()
                        * Math.log(((double) counts[i]) / ((double) examples.size()) / Math.log(2.0));
            }
        }
        return result;
    }

    private LogicalCountingTree trainIntern(List<CountingExample> examples, Vector<Variable> boundedVars,
            int depth, int countingClasses) {
        assert examples != null;

        if (depth == maxTreeDepth || examples.size() < minLeafSize) {
            return new LogicalCountingTree(countClasses(examples, countingClasses), null, null, null);
        }

        double oldEntropy = calcEntropy(examples, countingClasses);

        if (oldEntropy < 0.00001) {
            return new LogicalCountingTree(countClasses(examples, countingClasses), null, null, null);
        }

        double bestGain = Double.NEGATIVE_INFINITY;
        UnificationJob bestUnificationJob = null;

        int bestTrueExamplesCount = 0;
        int bestFalseExamplesCount = 0;

        for (UnificationJob job : getJobIterator(examples, boundedVars,depth)) {
            Vector<CountingExample> trueExamples = new Vector<CountingExample>(examples.size());
            Vector<CountingExample> falseExamples = new Vector<CountingExample>(examples.size());

            // split examples into true/false-parts
            for (int i = 0; i < examples.size(); i++) {
                substs[i] = Unificator.findMGU(examples.get(i).content, job,
                        ((Substitutions) examples.get(i).auxObject).clone());
                if (substs[i] != null) { // true branch
                    trueExamples.add(examples.get(i));
                } else {
                    falseExamples.add(examples.get(i));
                }
            }

            if (trueExamples.size() == 0 || falseExamples.size() == 0) {
                // using this splitatom doesnt make sense
                continue;
            }

            double gain = oldEntropy;
            if (trueExamples.size() > 0) {
                gain -= ((double) trueExamples.size()) / ((double) examples.size())
                        * calcEntropy(trueExamples, countingClasses);
            }
            if (falseExamples.size() > 0) {
                gain -= ((double) falseExamples.size()) / ((double) examples.size())
                        * calcEntropy(falseExamples, countingClasses);
            }

            if (gain >= bestGain) {

                Substitutions[] tmp = substs;
                substs = bestsubsts;
                bestsubsts = tmp;

                bestGain = gain;
                bestUnificationJob = job;

                bestTrueExamplesCount = trueExamples.size();
                bestFalseExamplesCount = falseExamples.size();
            }
        }

        if (bestGain == Double.NEGATIVE_INFINITY) {
            return new LogicalCountingTree(countClasses(examples, countingClasses), null, null, null);
        }

        // split training data for both subtrees
        List<CountingExample> trueExamples = new Vector<CountingExample>(bestTrueExamplesCount);
        List<CountingExample> falseExamples = new Vector<CountingExample>(bestTrueExamplesCount);

        for (int i = 0; i < examples.size(); i++) {
            CountingExample ex = examples.get(i);
            if (bestsubsts[i] != null) {
                ex.auxObject = bestsubsts[i];
                trueExamples.add(ex);
            } else {
                falseExamples.add(ex);
            }
        }

        // free memory
        examples.clear();
        examples = null;

        Vector<Variable> boundedVars2 = (Vector<Variable>) boundedVars.clone();
        for (Variable v : bestUnificationJob.getTerm().getContainedVariables()) {
            if (!boundedVars2.contains(v)) {
                boundedVars2.add(v);
            }
        }
        LogicalCountingTree falseSubTree = trainIntern(falseExamples, boundedVars, depth + 1, countingClasses);

        LogicalCountingTree trueSubTree = trainIntern(trueExamples, boundedVars, depth + 1, countingClasses);

        return new LogicalCountingTree(null, bestUnificationJob, trueSubTree, falseSubTree);
    }

    public String toString() {
        return "LogicalRegressionTreeTrainer(" + maxTreeDepth + "," + minLeafSize + ")";
    }

}
