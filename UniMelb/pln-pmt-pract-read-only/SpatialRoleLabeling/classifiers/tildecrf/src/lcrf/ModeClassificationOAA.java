/**
 * 
 */
package lcrf;

import java.util.HashMap;
import java.util.List;

import lcrf.counting.LogicalCountingTreeTrainer;
import lcrf.logic.Atom;
import lcrf.regression.RegressionModelTrainer;
import lcrf.stuff.ArrayStuff;
import lcrf.stuff.NumberStorage;

import org.apache.log4j.Logger;

/**
 * @author bgutmann
 * 
 */
public class ModeClassificationOAA {
    public ModeClassificationOAA(ClassificationExampleContainer trainFold,
            ClassificationExampleContainer testFold,
            ClassificationExampleContainer validationSet,
            int improvements,
            long seed, RegressionModelTrainer<List<Atom>> trainer,
            WindowMaker wm, LogicalCountingTreeTrainer trainer2, int crftrainsteps, Atom targetAtom,
            Atom othersAtom) {

        List<Atom> classAtoms = trainFold.getClassAtoms();
        HashMap<Atom, List<List<Atom>>> justTheExamplesTrain = new HashMap<Atom, List<List<Atom>>>();

        //split training examples for into folds for each class atom
        for (Atom a : classAtoms) {
            justTheExamplesTrain.put(a, trainFold.getExamplesForAtom(a));
        }

        HashMap<Atom, ClassificationExampleContainer> examples = new HashMap<Atom, ClassificationExampleContainer>(
                classAtoms.size());
        HashMap<Atom, CRF> crfs = new HashMap<Atom, CRF>(classAtoms.size());

        // prepare example container and the CRFs
        for (Atom a : classAtoms) {
            ClassificationExampleContainer c = new ClassificationExampleContainer();
            c.addExamples(justTheExamplesTrain.get(a), targetAtom);

            // add all the other folds
            for (Atom a2 : classAtoms) {
                if (!a.equals(a2))
                    c.addExamples(justTheExamplesTrain.get(a2), othersAtom);
            }

            examples.put(a, c);
            crfs.put(a, new CRF(c.getClassAtoms(), trainer, wm, trainer2, seed));
        }

        for (int step = 1; step <= crftrainsteps; step++) {
            Logger.getLogger("main.step").info("Step " + step + " of " + crftrainsteps);
            for (Atom a : classAtoms) {
                Logger.getLogger("main.step").info("train CRF for atom " + a + " against the rest");
                crfs.get(a).trainOneStep(examples.get(a));
            }

            Logger.getLogger("main.step.classification").info("Classify the traindata");
            classifyAndLogOneAgainstAll(crfs, trainFold, "traindata", targetAtom,othersAtom);
            Logger.getLogger("main.step.classification").info("Classify the testdata");
            classifyAndLogOneAgainstAll(crfs, testFold, "testdata", targetAtom, othersAtom);
        }

        /*
         * ByteArrayOutputStream baos = new ByteArrayOutputStream();
         * ObjectOutputStream oas = new ObjectOutputStream(baos);
         * oas.writeObject(crfs);
         * 
         * FileWriter.writeToFile("crfs", ".ser", baos.toString());
         */
    }

    private static void classifyAndLogOneAgainstAll(HashMap<Atom, CRF> crfs,
            ClassificationExampleContainer examples, String prefix, Atom targetAtom, Atom othersAtom) {

        int wrongClassCounterViterbi = 0;
        int wrongClassCounterFB = 0;
        List<Atom> classAtoms = examples.getClassAtoms();
        int[][] corellationCounterViterbi = new int[classAtoms.size()][];
        int[][] corellationCounterFB = new int[classAtoms.size()][];
        for (int i = 0; i < examples.getClassAtoms().size(); i++) {
            corellationCounterViterbi[i] = new int[classAtoms.size()];
            corellationCounterFB[i] = new int[classAtoms.size()];
        }
        
        HashMap<Atom,Double> loglikelihoods = new HashMap<Atom,Double>(classAtoms.size());
        for (Atom a:classAtoms) {
            loglikelihoods.put(a, new Double(0.0d));
        }
        


        for (int i = 0; i < examples.size(); i++) {
            List<Atom> input = examples.getInputSequence(i);                      

            int[] viterbiCounter = new int[classAtoms.size()];
            int[] fbCounter = new int[classAtoms.size()];
            for (Atom a : classAtoms) {
                CRF crf = crfs.get(a);
                Atom viClassifiedAtom = crf.classifyViterbiMaxClassAtom(examples.getInputSequence(i));
                Atom fbClassifiedAtom = crf.classifyFBMaxClassAtom(examples.getInputSequence(i));

                if (viClassifiedAtom.equals(targetAtom)) {                    
                    viterbiCounter[classAtoms.indexOf(a)]++;
                } else {
                    for (int k = 0; k < classAtoms.size(); k++) {
                        if (!(classAtoms.get(k).equals(a)))
                            viterbiCounter[k]++;
                    }

                }

                if (fbClassifiedAtom.equals(targetAtom)) {
                    fbCounter[classAtoms.indexOf(a)]++;
                } else {
                    for (int k = 0; k < classAtoms.size(); k++) {
                        if (!(classAtoms.get(k).equals(a)))
                            fbCounter[k]++;
                    }

                }
                
                Atom knownClassAtom = (a.equals(examples.getClassAtom(i))) ?
                        targetAtom : othersAtom;
                
                double loglikelihood = crf.getLogLikelihood(input,knownClassAtom);
                loglikelihoods.put(a,loglikelihoods.get(a)+loglikelihood);
            }

            int classifiedClassViterbi = ArrayStuff.argmax(viterbiCounter);
            int classifiedClassFB = ArrayStuff.argmax(fbCounter);
            int realClass = classAtoms.indexOf(examples.getClassAtom(i));

            corellationCounterViterbi[realClass][classifiedClassViterbi]++;
            corellationCounterFB[realClass][classifiedClassFB]++;
            if (realClass != classifiedClassFB) {
                wrongClassCounterFB++;
            }
            if (realClass != classifiedClassViterbi) {
                wrongClassCounterViterbi++;
            }
        }
        
        double loglikelihoodSum = 0.0d;
        for (Atom a:classAtoms) {
            loglikelihoodSum += loglikelihoods.get(a);
        }
        
        Logger.getLogger("main.step.classification").info("Log-Likelihood of every submodel: "+loglikelihoods.toString());
        Logger.getLogger("main.step.classification").info("Log-Likelihood summed           : "+loglikelihoodSum);
        
        
        Logger.getLogger("main.step.classification").info("Predicted classes (FB):");
        for (int i = 0; i < classAtoms.size(); i++) {
            String line = "  Class " + classAtoms.get(i) + " : ";
            for (int j = 0; j < classAtoms.size(); j++) {
                line += "(" + classAtoms.get(j) + " : " + corellationCounterFB[i][j] + " times) ";
            }
            Logger.getLogger("main.step.classification").info(line);
        }
        Logger.getLogger("main.step.classification").info(
                wrongClassCounterFB + " Errors at " + examples.size() + " Test examples (" + 100.0
                        * (double) wrongClassCounterFB / (double) examples.size() + " %)");
        NumberStorage.add(prefix + "ErrFB", (double) wrongClassCounterFB / (double) examples.size());

        Logger.getLogger("main.step.classification").info("Predicted classes (Viterbi):");
        for (int i = 0; i < classAtoms.size(); i++) {
            String line = "  Class " + classAtoms.get(i) + " : ";
            for (int j = 0; j < classAtoms.size(); j++) {
                line += "(" + classAtoms.get(j) + " : " + corellationCounterViterbi[i][j] + " times) ";
            }
            Logger.getLogger("main.step.classification").info(line);
        }
        Logger.getLogger("main.step.classification").info(
                wrongClassCounterViterbi + " Errors at " + examples.size() + " Test examples (" + 100.0
                        * (double) wrongClassCounterViterbi / (double) examples.size() + " %)");
        NumberStorage.add(prefix + "ErrViterbi", (double) wrongClassCounterFB / (double) examples.size());

    }

}
