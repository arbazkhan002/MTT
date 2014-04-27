/**
 * 
 */
package lcrf.regression;

import java.io.Serializable;
import java.util.Comparator;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Vector;

import lcrf.logic.Atom;
import lcrf.logic.Interpretation;
import lcrf.logic.InterpretationSchemaUnificationJobGenerator;
import lcrf.logic.Substitutions;
import lcrf.logic.TermSchema;
import lcrf.logic.Variable;
import lcrf.stuff.FileWriter;

import org.apache.log4j.Logger;

/**
 * @author bgutmann
 */
public class InterpretationRegressionTreeTrainerBestFirst implements RegressionModelTrainer<Interpretation>,
        Serializable {
    private static final long serialVersionUID = 3257008743811134257L;

    // FIXME hard-coded!
    // the maximum number of leaf-nodes that the trees may have
    private int maxLeafSize = 100;

    private int maxTreeDepth;

    private int minLeafSize;

    private double defaultValue = 0.0;

    public List<TermSchema> schemata;

    private RegressionModelStuff<Interpretation> stuff;

    // temp variables for training
    private Substitutions[] bestsubsts;

    private Substitutions[] substs;

    private PriorityQueue<ExploreJob<Interpretation>> queue;

    public InterpretationRegressionTreeTrainerBestFirst(int maxTreeDepth, int minLeafSize) {
        this(maxTreeDepth, minLeafSize, null);
    }

    public InterpretationRegressionTreeTrainerBestFirst(int maxTreeDepth, int minLeafSize,
            List<TermSchema> schemata) {
        if (minLeafSize < 1) {
            throw new IllegalArgumentException(Integer.toString(minLeafSize));
        }

        if (maxTreeDepth < 0) {
            throw new IllegalArgumentException(Integer.toString(maxTreeDepth));
        }
        this.maxTreeDepth = maxTreeDepth;
        this.minLeafSize = minLeafSize;
        this.schemata = schemata;
        stuff = new RegressionModelStuff<Interpretation>();

        queue = new PriorityQueue<ExploreJob<Interpretation>>(maxLeafSize * 2 + 10,
                new Comparator<ExploreJob<Interpretation>>() {
                    public int compare(ExploreJob<Interpretation> j1, ExploreJob<Interpretation> j2) {
                        int s1 = j1.getExamples().size();
                        int s2 = j2.getExamples().size();

                        if (s1 < s2)
                            return 1;
                        if (s1 > s2)
                            return -1;

                        return 0;
                    }
                });
    }

    private Iterable<Atom> getJobIterator(List<RegressionExample<Interpretation>> examples,
            List<Variable> boundedVars, int actualDepth) {
        if (schemata == null) {
            Vector<Atom> differentAtoms = new Vector<Atom>(100);
            for (int i = 0; i < examples.size(); i++) {
                Interpretation example = examples.get(i).content;
                for (int j = 0; j < example.size(); j++) {
                    if (!differentAtoms.contains(example.get(j))) {
                        differentAtoms.add(example.get(j));
                    }
                }
            }
            return differentAtoms;
        }
        // FIXME

        return new InterpretationSchemaUnificationJobGenerator(schemata, boundedVars, actualDepth);
    }

    public RegressionModel<Interpretation> trainFromExamples(List<RegressionExample<Interpretation>> examples) {
        if (examples == null || examples.size() == 0) {
            return new InterpretationRegressionTree(defaultValue, null, null, null);
        }

        // prapare global variables
        this.bestsubsts = new Substitutions[examples.size()];
        this.substs = new Substitutions[examples.size()];

        for (RegressionExample ex : examples) {
            ex.auxObject = new Substitutions();
        }

        queue.offer(new ExploreJob<Interpretation>(examples, stuff.calcAverage(examples), null, false, 0,
                new Vector<Variable>(20), new Vector<Atom>()));

        InterpretationRegressionTree t = trainIntern();

        queue.clear();

        FileWriter.writeToFile("models/lrt", ".dot", t.toDotString());

        // clear global variables
        this.bestsubsts = null;
        this.substs = null;

        return t;
    }

    private InterpretationRegressionTree trainIntern() {
        // one because we have the root node
        int leafsInTree = 1;
        InterpretationRegressionTree rootNode = null;

        while (queue.isEmpty() == false) {
            ExploreJob<Interpretation> currentJob = queue.poll();
            List<RegressionExample<Interpretation>> examples = currentJob.getExamples();

            //Logger.getLogger("Learner").debug(currentJob);

            double bestsumsquarederror = Double.MAX_VALUE;
            Atom bestUnificationJob = null;

            int bestTrueExamplesCount = 0;
            int bestFalseExamplesCount = 0;
            double bestTrueExamplesSum = 0;
            double bestFalseExamplesSum = 0;
            
            double bestAverageDifference = 0.0;

            if (leafsInTree < maxLeafSize) {

                for (Atom test : getJobIterator(examples, currentJob.getBoundedVars(), currentJob.getDepth())) {
                    //Logger.getLogger("test").debug(test);

                    if (currentJob.getTestsSoFar().contains(test))
                        continue;

                    int trueExamplesCount = 0;
                    int falseExamplesCount = 0;
                    double trueExamplesSum = 0;
                    double falseExamplesSum = 0;

                    // split examples into true/false-parts
                        for (int i = 0; i < examples.size(); i++) {
                            substs[i] = examples.get(i).content.contains(test.getTermRepresentation(), ((Substitutions) examples
                                    .get(i).auxObject).clone());
                            if (substs[i] != null) { // true branch
                                trueExamplesCount++;
                                trueExamplesSum += examples.get(i).value;
                            } else {
                                falseExamplesCount++;
                                falseExamplesSum += examples.get(i).value;
                            }
                    }

                    // Logger.getLogger("Learner").debug(test+"
                    // "+trueExamplesCount
                    // + " " + falseExamplesCount);
                        //Logger.getLogger("test").debug(test + " check1   "+trueExamplesCount +"   "+falseExamplesCount);
                    if (trueExamplesCount < 1 || falseExamplesCount < 1) {
                        // if (trueExamplesCount == 0 || falseExamplesCount ==
                        // 0) {
                        // using this splitatom doesnt make sense
                        continue;
                    }
                    //Logger.getLogger("test").debug(test + " check2   "+trueExamplesCount +"   "+falseExamplesCount);

                    double trueExamplesAverage = trueExamplesSum / trueExamplesCount;
                    double falseExamplesAverage = falseExamplesSum / falseExamplesCount;
                    double sumsquarederror = 0.0;

                    double truesumsquarederror = 0.0d;
                    double falsesumsquarederror = 0.0d;

                    for (int i = 0; i < examples.size(); i++) {
                        // double val = examples.get(i).value
                        // - ((substs[i] != null) ? trueExamplesAverage :
                        // falseExamplesAverage);
                        // sumsquarederror += val * val;
                        if (substs[i] != null) {
                            double tmp = examples.get(i).value - trueExamplesAverage;
                            truesumsquarederror += tmp * tmp;
                        } else {
                            double tmp = examples.get(i).value - falseExamplesAverage;
                            falsesumsquarederror += tmp * tmp;
                        }
                    }

                    sumsquarederror = (truesumsquarederror * trueExamplesCount + falsesumsquarederror
                            * falseExamplesCount)
                            / examples.size();

                    if (sumsquarederror < bestsumsquarederror) {
                        //Logger.getLogger("test").debug(test + " check3   "+sumsquarederror + " "+bestsumsquarederror);
                        Substitutions[] tmp = substs;
                        substs = bestsubsts;
                        bestsubsts = tmp;

                        bestsumsquarederror = sumsquarederror;
                        bestUnificationJob = test;

                        bestTrueExamplesCount = trueExamplesCount;
                        bestFalseExamplesCount = falseExamplesCount;
                        bestTrueExamplesSum = trueExamplesSum;
                        bestFalseExamplesSum = falseExamplesSum;
                        
                        bestAverageDifference = Math.abs(bestTrueExamplesSum/bestTrueExamplesCount - bestFalseExamplesSum/bestFalseExamplesCount);
                    }
                }
            }

            InterpretationRegressionTree currentNode = null;

            if (bestTrueExamplesCount == 0 || bestFalseExamplesCount == 0||bestAverageDifference<0.0000001) {
                // no split, we create a leaf node
                currentNode = new InterpretationRegressionTree(currentJob.getAverage(), null, null, null);
            } else {
                currentNode = new InterpretationRegressionTree(bestUnificationJob);
                // split training data for both subtrees
                List<RegressionExample<Interpretation>> trueExamples = new Vector<RegressionExample<Interpretation>>(
                        bestTrueExamplesCount);
                List<RegressionExample<Interpretation>> falseExamples = new Vector<RegressionExample<Interpretation>>(
                        bestTrueExamplesCount);

                for (int i = 0; i < examples.size(); i++) {
                    RegressionExample<Interpretation> ex = examples.get(i);
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

                Vector<Variable> trueBoundedVars = (Vector<Variable>) currentJob.getBoundedVars().clone();
                Vector<Variable> falseBoundedVars = currentJob.getBoundedVars();

                for (Variable v : bestUnificationJob.getTermRepresentation().getContainedVariables()) {
                    if (!trueBoundedVars.contains(v)) {
                        trueBoundedVars.add(v);
                    }
                }

                Vector<Atom> trueTestsSoFar = (Vector<Atom>) currentJob.getTestsSoFar().clone();
                Vector<Atom> falseTestsSoFar = (Vector<Atom>) currentJob.getTestsSoFar();

                trueTestsSoFar.add(bestUnificationJob);

                queue.offer(new ExploreJob<Interpretation>(trueExamples, bestTrueExamplesSum
                        / bestTrueExamplesCount, currentNode, true, currentJob.getDepth() + 1,
                        trueBoundedVars, trueTestsSoFar));
                queue.offer(new ExploreJob<Interpretation>(falseExamples, bestFalseExamplesSum
                        / bestFalseExamplesCount, currentNode, false, currentJob.getDepth() + 1,
                        falseBoundedVars, falseTestsSoFar));
            }

            // insert the node in the tree
            if (currentJob.getFather() == null) {
                rootNode = currentNode;
            } else {
                if (currentJob.isTrueChild()) {
                    currentJob.getFather().setTrueSubTree(currentNode);
                } else {
                    currentJob.getFather().setFalseSubTree(currentNode);
                }
            }

            currentJob.clear();
            leafsInTree++;
            //Logger.getLogger("Learner").debug(rootNode);
        }

        rootNode.verifyTree();

        return rootNode;
    }

    public String toString() {
        return "LogicalRegressionTreeTrainer(" + maxTreeDepth + "," + minLeafSize + "," + schemata + ")";
    }

}
