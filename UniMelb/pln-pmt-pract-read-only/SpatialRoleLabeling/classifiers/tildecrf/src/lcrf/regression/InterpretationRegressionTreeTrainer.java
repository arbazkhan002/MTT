/**
 * 
 */
package lcrf.regression;

import java.io.Serializable;
import java.util.List;
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
 * 
 */
public class InterpretationRegressionTreeTrainer implements RegressionModelTrainer<Interpretation>, Serializable {
    private static final long serialVersionUID = 3257008743811134257L;

    private int maxTreeDepth;

    private int minLeafSize;

    private double defaultValue = 0.0;

    public List<TermSchema> schemata;

    private RegressionModelStuff<Interpretation> stuff;

    // temp variables for training
    private Substitutions[] bestsubsts;

    private Substitutions[] substs;

    public InterpretationRegressionTreeTrainer(int maxTreeDepth, int minLeafSize) {
        this(maxTreeDepth, minLeafSize, null);
    }

    public InterpretationRegressionTreeTrainer(int maxTreeDepth, int minLeafSize, List<TermSchema> schemata) {
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
//FIXME        
        
       return new InterpretationSchemaUnificationJobGenerator(schemata, boundedVars,actualDepth);
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

        InterpretationRegressionTree t = trainIntern(examples, new Vector<Variable>(30), 0, stuff
                .calcAverage(examples), new Vector<Atom>());

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



    private InterpretationRegressionTree trainIntern(List<RegressionExample<Interpretation>> examples,
            Vector<Variable> boundedVars, int depth, double average, Vector<Atom> usedJobs) {
        

        if (depth == maxTreeDepth || examples.size() < 2) {
            return new InterpretationRegressionTree(average, null, null, null);
        }
        
        //Logger.getLogger("Learner").debug("Depth "+depth+ "  Size " + examples.size());

        double bestsumsquarederror = Double.MAX_VALUE;
        Atom bestUnificationJob = null;

        int bestTrueExamplesCount = 0;
        int bestFalseExamplesCount = 0;
        double bestTrueExamplesSum = 0;
        double bestFalseExamplesSum = 0;

        for (Atom test : getJobIterator(examples, boundedVars, depth)) {
            
            if (usedJobs.contains(test))
                continue;

            int trueExamplesCount = 0;
            int falseExamplesCount = 0;
            double trueExamplesSum = 0;
            double falseExamplesSum = 0;

            // split examples into true/false-parts
            for (int i = 0; i < examples.size(); i++) {                
                substs[i] = examples.get(i).content.contains(test.getTermRepresentation(), ((Substitutions) examples.get(i).auxObject).clone());
                if (substs[i] != null) { // true branch
                    trueExamplesCount++;
                    trueExamplesSum += examples.get(i).value;
                } else {
                    falseExamplesCount++;
                    falseExamplesSum += examples.get(i).value;
                }
            }
            
//            Logger.getLogger("Learner").debug(test+" "+trueExamplesCount + " " + falseExamplesCount);
            
            

            if (trueExamplesCount < 1 || falseExamplesCount < 1) {
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
            //    double val = examples.get(i).value
            //            - ((substs[i] != null) ? trueExamplesAverage : falseExamplesAverage);
            //    sumsquarederror += val * val;
                        if (substs[i] != null) {
                            double tmp = examples.get(i).value - trueExamplesAverage;
                            truesumsquarederror += tmp*tmp;
                        } else {
                            double tmp = examples.get(i).value - falseExamplesAverage;
                            falsesumsquarederror += tmp*tmp;                            
                        }
            }
            
            sumsquarederror = (truesumsquarederror * trueExamplesCount + falsesumsquarederror * falseExamplesCount) /
                examples.size();

            if (sumsquarederror < bestsumsquarederror) {
                Substitutions[] tmp = substs;
                substs = bestsubsts;
                bestsubsts = tmp;

                bestsumsquarederror = sumsquarederror;
                bestUnificationJob = test;

                bestTrueExamplesCount = trueExamplesCount;
                bestFalseExamplesCount = falseExamplesCount;
                bestTrueExamplesSum = trueExamplesSum;
                bestFalseExamplesSum = falseExamplesSum;
            }
        }
        
        //Logger.getLogger("Learner").debug("Depth "+depth+ "  Trues "+bestTrueExamplesCount + "   False "+bestFalseExamplesCount +"   "+bestUnificationJob);

        if (bestTrueExamplesCount == 0 || bestFalseExamplesCount == 0) {
            return new InterpretationRegressionTree(average, null, null, null);
        }

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

        Vector<Variable> boundedVars2 = (Vector<Variable>) boundedVars.clone();
        for (Variable v : bestUnificationJob.getTermRepresentation().getContainedVariables()) {
            if (!boundedVars2.contains(v)) {
                boundedVars2.add(v);
            }
        }

        usedJobs.add(bestUnificationJob);

        InterpretationRegressionTree falseSubTree = trainIntern(falseExamples, boundedVars2, depth + 1,
                bestFalseExamplesSum / bestFalseExamplesCount, usedJobs);

        // free memory
        falseExamples.clear();
        falseExamples = null;

        InterpretationRegressionTree trueSubTree = trainIntern(trueExamples, boundedVars2, depth + 1,
                bestTrueExamplesSum / bestTrueExamplesCount, usedJobs);

        // free memory
        trueExamples.clear();
        trueExamples = null;

        usedJobs.remove(usedJobs.size() - 1);

        return new InterpretationRegressionTree(average, bestUnificationJob, trueSubTree, falseSubTree);
    }

    public String toString() {
        return "LogicalRegressionTreeTrainer(" + maxTreeDepth + "," + minLeafSize + ","+schemata+")";
    }

}
