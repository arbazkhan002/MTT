/**
 * 
 */
package lcrf.regression;

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
public class LogicalRegressionTreeTrainer implements RegressionModelTrainer<List<Atom>>, Serializable {
    private static final long serialVersionUID = 3257008743811134257L;

    private int maxTreeDepth;

    private int minLeafSize;

    private double defaultValue = 0.0;

    public List<TermSchema> schemata;

    private RegressionModelStuff<List<Atom>> stuff;

    // temp variables for training
    private Substitutions[] bestsubsts;

    private Substitutions[] substs;

    private int[] windowFieldTypes;

    public LogicalRegressionTreeTrainer(int maxTreeDepth, int minLeafSize) {
        this(maxTreeDepth, minLeafSize, null, null);
    }

    public LogicalRegressionTreeTrainer(int maxTreeDepth, int minLeafSize, List<TermSchema> schemata,
            int[] windowFieldTypes) {
        if (minLeafSize < 1) {
            throw new IllegalArgumentException(Integer.toString(minLeafSize));
        }

        if (maxTreeDepth < 0) {
            throw new IllegalArgumentException(Integer.toString(maxTreeDepth));
        }
        this.maxTreeDepth = maxTreeDepth;
        this.minLeafSize = minLeafSize;
        this.schemata = schemata;
        stuff = new RegressionModelStuff<List<Atom>>();
        this.windowFieldTypes = windowFieldTypes;

    }

    private Iterable<UnificationJob> getJobIterator(List<RegressionExample<List<Atom>>> examples,
            List<Variable> boundedVars, int actualDepth) {
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

        return new SchemaUnificationJobGenerator(examples.get(0).content.size(), schemata, boundedVars,
                actualDepth);
    }

    public RegressionModel<List<Atom>> trainFromExamples(List<RegressionExample<List<Atom>>> examples) {
        if (examples == null || examples.size() == 0) {
            return new LogicalRegressionTree(defaultValue, null, null, null);
        }

        // prapare global variables
        this.bestsubsts = new Substitutions[examples.size()];
        this.substs = new Substitutions[examples.size()];

        for (RegressionExample ex : examples) {
            ex.auxObject = new Substitutions();
        }

        LogicalRegressionTree t = trainIntern(examples, new Vector<Variable>(30), 0, stuff
                .calcAverage(examples), new Vector<UnificationJob>());

        // logger.info("Unificator Cache-Hit/Cache-Miss : " +
        // Unificator.hitcounter + "/" + Unificator.misscounter);
        // logger.info("Substitutions Hit/Miss : " + Substitutions.hitcounter +
        // "/" + Substitutions.misscounter);
        // logger.info("Substitutions Clone/Modify : " +
        // Substitutions.clonecounter + "/" + Substitutions.modifycounter);

        // FIXME define constant via commandline
        t = t.doPrunning(0.0001);

        FileWriter.writeToFile("models/lrt", ".dot", t.toDotString());

        // clear global variables
        this.bestsubsts = null;
        this.substs = null;

        return t;
    }

    private boolean jobMakesSense(UnificationJob job) {
        // Logger.getLogger(getClass()).info("jobType is
        // "+job.getTerm().getType());
        // Logger.getLogger(getClass()).info("windowFieldType is
        // "+windowFieldTypes[job.getPosition()]);
        if (job.getTerm().getType() == 0)
            return true;
        return (job.getTerm().getType() & windowFieldTypes[job.getPosition()]) > 0;
    }

    private LogicalRegressionTree trainIntern(List<RegressionExample<List<Atom>>> examples,
            Vector<Variable> boundedVars, int depth, double average, Vector<UnificationJob> usedJobs) {
        // Logger.getLogger(getClass()).info("depth is "+depth+" examlesize is
        // "+examples.size());

        if (depth == maxTreeDepth || examples.size() < minLeafSize) {
            return new LogicalRegressionTree(average, null, null, null);
        }

        double bestsumsquarederror = Double.MAX_VALUE;
        UnificationJob bestUnificationJob = null;

        int bestTrueExamplesCount = 0;
        int bestFalseExamplesCount = 0;
        double bestTrueExamplesSum = 0;
        double bestFalseExamplesSum = 0;

        for (UnificationJob job : getJobIterator(examples, boundedVars, depth)) {
            if ((!jobMakesSense(job)) || usedJobs.contains(job))
                continue;

            int trueExamplesCount = 0;
            int falseExamplesCount = 0;
            double trueExamplesSum = 0;
            double falseExamplesSum = 0;
            
            double trueExamplesWeightSum = 0;
            double falseExamplesWeightSum = 0;

            // split examples into true/false-parts
            for (int i = 0; i < examples.size(); i++) {
                substs[i] = Unificator.findMGU(examples.get(i).content, job,
                        ((Substitutions) examples.get(i).auxObject).clone());
                if (substs[i] != null) { // true branch
                    trueExamplesCount++;
                    trueExamplesSum += examples.get(i).value;
                    
                    trueExamplesWeightSum += examples.get(i).weight;
                } else {
                    falseExamplesCount++;
                    falseExamplesSum += examples.get(i).value;
                    
                    falseExamplesWeightSum += examples.get(i).weight;
                }
            }

            if (trueExamplesCount < minLeafSize || falseExamplesCount < minLeafSize) {
                // if (trueExamplesCount == 0 || falseExamplesCount == 0) {
                // using this splitatom doesnt make sense
                continue;
            }

            double trueExamplesAverage = trueExamplesSum / trueExamplesCount;
            double falseExamplesAverage = falseExamplesSum / falseExamplesCount;
            double sumsquarederror = 0.0;
            
            double truesumsquarederror = 0.0d;
            double falsesumsquarederror = 0.0d;

            for (int i = 0; i < examples.size(); i++) {
                double val = examples.get(i).value
                        - ((substs[i] != null) ? trueExamplesAverage : falseExamplesAverage);
                sumsquarederror += val * val;
            
            
                //if you want to use the weighted version of the regression tree learner,
                //then comment the above lines and uncomment the following
                /*            if (substs[i] != null) {
                            double tmp = examples.get(i).value - trueExamplesAverage;
                            truesumsquarederror += tmp*tmp * examples.get(i).weight;
                        } else {
                            double tmp = examples.get(i).value - falseExamplesAverage;
                            falsesumsquarederror += tmp*tmp * examples.get(i).weight;                            
                        }*/
            }
            
            //if you want to use the weighted version of the regression tree learner,
            //then uncomment the following        
            //sumsquarederror = (truesumsquarederror * trueExamplesCount/trueExamplesWeightSum + falsesumsquarederror * falseExamplesCount/falseExamplesWeightSum) /
                examples.size();

            if (sumsquarederror < bestsumsquarederror) {
                Substitutions[] tmp = substs;
                substs = bestsubsts;
                bestsubsts = tmp;

                bestsumsquarederror = sumsquarederror;
                bestUnificationJob = job;

                bestTrueExamplesCount = trueExamplesCount;
                bestFalseExamplesCount = falseExamplesCount;
                bestTrueExamplesSum = trueExamplesSum;
                bestFalseExamplesSum = falseExamplesSum;
            }
        }

        if (bestTrueExamplesCount == 0 || bestFalseExamplesCount == 0) {
            return new LogicalRegressionTree(average, null, null, null);
        }

        // split training data for both subtrees
        List<RegressionExample<List<Atom>>> trueExamples = new Vector<RegressionExample<List<Atom>>>(
                bestTrueExamplesCount);
        List<RegressionExample<List<Atom>>> falseExamples = new Vector<RegressionExample<List<Atom>>>(
                bestTrueExamplesCount);

        for (int i = 0; i < examples.size(); i++) {
            RegressionExample<List<Atom>> ex = examples.get(i);
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

        usedJobs.add(bestUnificationJob);

        LogicalRegressionTree falseSubTree = trainIntern(falseExamples, boundedVars2, depth + 1,
                bestFalseExamplesSum / bestFalseExamplesCount, usedJobs);

        // free memory
        falseExamples.clear();
        falseExamples = null;

        LogicalRegressionTree trueSubTree = trainIntern(trueExamples, boundedVars2, depth + 1,
                bestTrueExamplesSum / bestTrueExamplesCount, usedJobs);

        // free memory
        trueExamples.clear();
        trueExamples = null;

        usedJobs.remove(usedJobs.size() - 1);

        return new LogicalRegressionTree(average, bestUnificationJob, trueSubTree, falseSubTree);
    }

    public String toString() {
        return "LogicalRegressionTreeTrainer(" + maxTreeDepth + "," + minLeafSize + ","+schemata+","+windowFieldTypes+")";
    }

}
