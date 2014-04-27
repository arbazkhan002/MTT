/**
 * 
 */
package lcrf;

import java.util.HashMap;
import java.util.List;
import java.util.Vector;

import lcrf.counting.LogicalCountingTreeTrainer;
import lcrf.logic.Atom;
import lcrf.regression.RegressionModelTrainer;
import lcrf.stuff.ArrayStuff;
import lcrf.stuff.FileWriter;
import lcrf.stuff.Pair;

import org.apache.log4j.Logger;

/**
 * @author Bernd Gutmann
 */
public class ModeClassificationRR {
    private static final String fbclassFile = "classificationfb.txt";

    private static final String viclassFile = "classificationvi.txt";

    private double lastAccuracy = 0.0d;

    public ModeClassificationRR(ClassificationExampleContainer trainFold,
            ClassificationExampleContainer testFold, ClassificationExampleContainer validationSet,
            int improvements, long seed, RegressionModelTrainer<List<Atom>> trainer, WindowMaker wm,
            LogicalCountingTreeTrainer trainer2, int crftrainsteps, Atom targetAtom, Atom othersAtom) {

        double bestvalidationlikelihoodSoFar = Double.NEGATIVE_INFINITY;
        int bestStep = -1;
        int remainingImprovements = improvements;

        List<Atom> classAtoms = trainFold.getClassAtoms();
        List<Pair<Atom, Atom>> allPairs = generateAllPairs(classAtoms);
        HashMap<Atom, List<List<Atom>>> justTheExamplesTrain = new HashMap<Atom, List<List<Atom>>>();

        // split training examples into folds for each class atom
        for (Atom a : classAtoms) {
            justTheExamplesTrain.put(a, trainFold.getExamplesForAtom(a));
        }

        HashMap<Pair<Atom, Atom>, ClassificationExampleContainer> examples = new HashMap<Pair<Atom, Atom>, ClassificationExampleContainer>(
                classAtoms.size());
        HashMap<Pair<Atom, Atom>, CRF> crfs = new HashMap<Pair<Atom, Atom>, CRF>(classAtoms.size());

        // prepare example container and the CRFs
        for (Pair<Atom, Atom> p : allPairs) {
            ClassificationExampleContainer c = new ClassificationExampleContainer();
            c.addExamples(justTheExamplesTrain.get(p.o1), targetAtom);
            c.addExamples(justTheExamplesTrain.get(p.o2), othersAtom);

            examples.put(p, c);
            crfs.put(p, new CRF(c.getClassAtoms(), trainer, wm, trainer2, seed));
        }

        FileWriter.writeToFile(ModeClassificationRR.fbclassFile, "");
        FileWriter.writeToFile(ModeClassificationRR.viclassFile, "");

        for (int step = 1; step <= crftrainsteps && remainingImprovements > 0; step++) {
            remainingImprovements--;
            String outputHead = "START Step " + step + "\n";
            String outputBodyFB = "";
            String outputBodyVI = "";
            String outputFoot = "STOP Step " + step + "\n";

            Logger.getLogger("main.step").info("Step " + step + " of " + crftrainsteps);

            for (Pair<Atom, Atom> p : allPairs) {
                Logger.getLogger("main.step").info("train CRF for atom " + p.o1 + " against " + p.o2);
                crfs.get(p).trainOneStep(examples.get(p));
            }

            { // for training set
                Logger.getLogger("main.step.classification").info("Classify the traindata");
                String result = "Result:\n";
                double loglikelihood = calcLogLikelihood(trainFold, crfs, targetAtom, othersAtom);
                outputHead += "loglikelihood training set   : " + loglikelihood + "\n";

                List<Integer> fbClassification = classifyAllExamplesFB(crfs, trainFold, targetAtom,
                        othersAtom);
                List<Integer> viClassification = classifyAllExamplesVI(crfs, trainFold, targetAtom,
                        othersAtom);
                result += "Log-Likelihood : " + loglikelihood + "\n";
                result += "Forward-Backward:\n";
                result += makeConfusionMatrix(fbClassification, trainFold) + "\n";
                outputBodyFB += "accuracy training set        : " + lastAccuracy + "\n";
                result += "Viterbi:\n";
                result += makeConfusionMatrix(viClassification, trainFold) + "\n";
                outputBodyVI += "accuracy training set        : " + lastAccuracy + "\n";
                Logger.getLogger("main.step.classification").info(result);
            }

            if (validationSet != null) { // for validation set
                Logger.getLogger("main.step.classification").info("Classify the validation data");
                String result = "Result:\n";
                double loglikelihood = calcLogLikelihood(validationSet, crfs, targetAtom, othersAtom);
                if (loglikelihood >= bestvalidationlikelihoodSoFar) {
                    bestvalidationlikelihoodSoFar = loglikelihood;
                    bestStep = step;
                    remainingImprovements = improvements;
                }
                outputHead += "loglikelihood validation set : " + loglikelihood + "\n";
                outputHead += "best was                     : " + bestvalidationlikelihoodSoFar + "\n";
                outputHead += "best step was                : " + bestStep + "\n";
                outputHead += "remaining steps              : " + remainingImprovements + "\n";
                List<Integer> fbClassification = classifyAllExamplesFB(crfs, validationSet, targetAtom,
                        othersAtom);
                List<Integer> viClassification = classifyAllExamplesVI(crfs, validationSet, targetAtom,
                        othersAtom);
                result += "Log-Likelihood : " + loglikelihood + "\n";
                result += "Forward-Backward:\n";
                result += makeConfusionMatrix(fbClassification, validationSet) + "\n";
                outputBodyFB += "accuracy validation set      : " + lastAccuracy + "\n";
                result += "Viterbi:\n";
                result += makeConfusionMatrix(viClassification, validationSet) + "\n";
                outputBodyVI += "accuracy validation set      : " + lastAccuracy + "\n";
                Logger.getLogger("main.step.classification").info(result);
            }

            if (testFold != null) { // for test set
                Logger.getLogger("main.step.classification").info("Classify the testdata");
                String result = "Result:\n";
                double loglikelihood = calcLogLikelihood(testFold, crfs, targetAtom, othersAtom);
                outputHead += "loglikelihood test set       : " + loglikelihood + "\n";
                List<Integer> fbClassification = classifyAllExamplesFB(crfs, testFold, targetAtom, othersAtom);
                List<Integer> viClassification = classifyAllExamplesVI(crfs, testFold, targetAtom, othersAtom);
                result += "Log-Likelihood : " + loglikelihood + "\n";
                result += "Forward-Backward:\n";
                result += makeConfusionMatrix(fbClassification, testFold) + "\n";
                outputBodyFB += "accuracy test set            : " + lastAccuracy + "\n";
                result += "Viterbi:\n";
                result += makeConfusionMatrix(viClassification, testFold) + "\n";
                outputBodyVI += "accuracy test set            : " + lastAccuracy + "\n";
                Logger.getLogger("main.step.classification").info(result);
                outputBodyFB += this.evaluateClassifcationList(fbClassification, testFold);
                outputBodyVI += this.evaluateClassifcationList(viClassification, testFold);
            }

            FileWriter.writeToFile(ModeClassificationRR.fbclassFile, outputHead + outputBodyFB + outputFoot,
                    true);
            FileWriter.writeToFile(ModeClassificationRR.viclassFile, outputHead + outputBodyVI + outputFoot,
                    true);
        }

        /*
         * ByteArrayOutputStream baos = new ByteArrayOutputStream();
         * ObjectOutputStream oas = new ObjectOutputStream(baos);
         * oas.writeObject(crfs); FileWriter.writeToFile("crfs", ".ser",
         * baos.toString());
         */
    }

    /**
     * Generate all unique ordered pairs
     * 
     * @param classAtoms
     * @return
     */
    private Vector<Pair<Atom, Atom>> generateAllPairs(List<Atom> classAtoms) {
        Vector<Pair<Atom, Atom>> allPairs = new Vector<Pair<Atom, Atom>>();

        for (int i = 0; i < classAtoms.size(); i++) {
            for (int j = i + 1; j < classAtoms.size(); j++) {
                allPairs.add(new Pair<Atom, Atom>(classAtoms.get(i), classAtoms.get(j)));
            }
        }

        return allPairs;
    }

    /**
     * @param inputSequence
     * @param crfs
     * @param classAtoms
     * @param targetAtom
     * @param othersAtom
     * @return
     */
    private static int classifyFB(List<Atom> inputSequence, HashMap<Pair<Atom, Atom>, CRF> crfs,
            List<Atom> classAtoms, Atom targetAtom, Atom othersAtom) {
        int[] counter = new int[classAtoms.size()];

        for (Pair<Atom, Atom> p : crfs.keySet()) {
            Atom viClassification = crfs.get(p).classifyFBMaxClassAtom(inputSequence);
            if (viClassification.equals(targetAtom)) {
                counter[classAtoms.indexOf(p.o1)]++;
            } else {
                counter[classAtoms.indexOf(p.o2)]++;
            }

        }

        return ArrayStuff.argmax(counter);
    }

    /**
     * @param inputSequence
     * @param crfs
     * @param classAtoms
     * @param targetAtom
     * @param othersAtom
     * @return
     */
    private static int classifyViterbi(List<Atom> inputSequence, HashMap<Pair<Atom, Atom>, CRF> crfs,
            List<Atom> classAtoms, Atom targetAtom, Atom othersAtom) {
        int[] counter = new int[classAtoms.size()];

        for (Pair<Atom, Atom> p : crfs.keySet()) {
            Atom viClassification = crfs.get(p).classifyViterbiMaxClassAtom(inputSequence);
            if (viClassification.equals(targetAtom)) {
                counter[classAtoms.indexOf(p.o1)]++;
            } else {
                counter[classAtoms.indexOf(p.o2)]++;
            }

        }

        return ArrayStuff.argmax(counter);
    }

    /**
     * @param inputSequence
     * @param knownClass
     * @param crfs
     * @param loglikelihoods
     * @param targetAtom
     * @param othersAtom
     */
    private static double calcLogLikelihood(ClassificationExampleContainer examples,
            HashMap<Pair<Atom, Atom>, CRF> crfs, Atom targetAtom, Atom othersAtom) {

        HashMap<Pair<Atom, Atom>, Double> loglikelihoods = new HashMap<Pair<Atom, Atom>, Double>(crfs
                .keySet().size());
        for (Pair<Atom, Atom> pair : crfs.keySet()) {
            loglikelihoods.put(pair, new Double(0.0d));

        }

        for (int i = 0; i < examples.size(); i++) {
            List<Atom> input = examples.getInputSequence(i);
            Atom output = examples.getClassAtom(i);

            for (Pair<Atom, Atom> p : crfs.keySet()) {
                Atom knownClassAtom = (p.o1.equals(output)) ? targetAtom : othersAtom;

                double loglikelihood = crfs.get(p).getLogLikelihood(input, knownClassAtom);
                loglikelihoods.put(p, loglikelihoods.get(p) + loglikelihood);

            }
        }

        double loglikelihoodSum = 0.0d;

        for (Double llh : loglikelihoods.values()) {
            loglikelihoodSum += llh;
        }

        return loglikelihoodSum;
    }

    private String evaluateClassifcationList(List<Integer> classification, ClassificationExampleContainer ex) {
        String result = "(no;id;predicted;real)\n";
        List<Atom> classAtoms = ex.getClassAtoms();
        
        for (int i = 0; i < ex.size(); i++) {
            result += i + ";" + ex.getSequenceId(i) + ";" + ex.getClassAtom(i) + ";"
                    + classAtoms.get(classification.get(i)) + "\n";
        }

        return result;
    }

    private String makeConfusionMatrix(List<Integer> classification, ClassificationExampleContainer ex) {
        List<Atom> classAtoms = ex.getClassAtoms();
        int[][] confusionMatrix = new int[classAtoms.size()][];

        for (int i = 0; i < ex.getClassAtoms().size(); i++) {
            confusionMatrix[i] = new int[classAtoms.size()];
        }

        for (int i = 0; i < ex.size(); i++) {
            int realClass = classAtoms.indexOf(ex.getClassAtom(i));

            confusionMatrix[realClass][classification.get(i)]++;
        }

        return ArrayStuff.toConfusionMatrix(classAtoms, confusionMatrix);
    }

    /**
     * @param crfs
     * @param examples
     * @param targetAtom
     * @param othersAtom
     * @return
     */
    private static List<Integer> classifyAllExamplesFB(HashMap<Pair<Atom, Atom>, CRF> crfs,
            ClassificationExampleContainer examples, Atom targetAtom, Atom othersAtom) {

        Vector<Integer> classifications = new Vector<Integer>(examples.size());

        List<Atom> classAtoms = examples.getClassAtoms();

        for (int i = 0; i < examples.size(); i++) {
            List<Atom> input = examples.getInputSequence(i);
            classifications.add(classifyFB(input, crfs, classAtoms, targetAtom, othersAtom));
        }

        return classifications;

    }

    /**
     * @param crfs
     * @param examples
     * @param targetAtom
     * @param othersAtom
     * @return
     */
    private static List<Integer> classifyAllExamplesVI(HashMap<Pair<Atom, Atom>, CRF> crfs,
            ClassificationExampleContainer examples, Atom targetAtom, Atom othersAtom) {

        Vector<Integer> classifications = new Vector<Integer>(examples.size());

        List<Atom> classAtoms = examples.getClassAtoms();

        for (int i = 0; i < examples.size(); i++) {
            List<Atom> input = examples.getInputSequence(i);
            classifications.add(classifyViterbi(input, crfs, classAtoms, targetAtom, othersAtom));
        }

        return classifications;
    }

}
