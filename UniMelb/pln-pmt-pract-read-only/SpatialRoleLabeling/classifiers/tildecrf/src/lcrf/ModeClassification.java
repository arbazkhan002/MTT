/**
 * 
 */
package lcrf;

import java.util.List;

import lcrf.counting.LogicalCountingTreeTrainer;
import lcrf.logic.Atom;
import lcrf.regression.RegressionModelTrainer;

import org.apache.log4j.Logger;

/**
 * @author bgutmann
 * 
 */
public class ModeClassification {
    public ModeClassification(ClassificationExampleContainer trainFold,
            ClassificationExampleContainer testFold, 
            ClassificationExampleContainer validationSet,
            int improvements,
            long seed, RegressionModelTrainer<List<Atom>> trainer,
            WindowMaker wm, LogicalCountingTreeTrainer trainer2, int crftrainsteps) {

        CRF crf = new CRF(trainFold.getClassAtoms(), trainer, wm, trainer2, seed);

        for (int step = 1; step <= crftrainsteps; step++) {
            Logger.getLogger("main.step").info("Step " + step + " of " + crftrainsteps);
            crf.trainOneStep(trainFold);
            Logger.getLogger("main.step.classification").info("Classify the traindata");
            classifyAndLog(crf, trainFold, "traindata");
            Logger.getLogger("main.step.classification").info("Classify the testdata");
            classifyAndLog(crf, testFold, "testdata");
        }

        /*
         * ByteArrayOutputStream baos = new ByteArrayOutputStream();
         * ObjectOutputStream oas = new ObjectOutputStream(baos);
         * oas.writeObject(crf);
         * 
         * FileWriter.writeToFile("crf", ".ser", baos.toString());
         */
    }

    private static void classifyAndLog(CRF crf, ClassificationExampleContainer examples, String prefix) {
        assert crf != null;
        assert examples != null;

        int wrongClassCounterViterbi = 0;
        int wrongClassCounterFB = 0;
        List<Atom> classAtoms = examples.getClassAtoms();
        int[][] corellationCounterViterbi = new int[classAtoms.size()][];
        int[][] corellationCounterFB = new int[classAtoms.size()][];
        for (int i = 0; i < examples.getClassAtoms().size(); i++) {
            corellationCounterViterbi[i] = new int[classAtoms.size()];
            corellationCounterFB[i] = new int[classAtoms.size()];
        }
        
        
        double loglikelihood = 0.0d;

        for (int i = 0; i < examples.size(); i++) {
            List<Atom> input = examples.getInputSequence(i);
            int classifiedClassViterbi = classAtoms.indexOf(crf.classifyViterbiMaxClassAtom(examples
                    .getInputSequence(i)));
            int classifiedClassFB = classAtoms.indexOf(crf.classifyFBMaxClassAtom(examples
                    .getInputSequence(i)));
            int realClass = classAtoms.indexOf(examples.getClassAtom(i));

            corellationCounterViterbi[realClass][classifiedClassViterbi]++;
            corellationCounterFB[realClass][classifiedClassFB]++;
            if (realClass != classifiedClassFB) {
                wrongClassCounterFB++;
            }
            if (realClass != classifiedClassViterbi) {
                wrongClassCounterViterbi++;
            }
            
            loglikelihood = crf.getLogLikelihood(input,examples.getClassAtom(i));
        }
        Logger.getLogger("main.step.classification").info("Log-Likelihood        : "+loglikelihood);
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
        // NumberStorage.add(prefix + "ErrFB", (double) wrongClassCounterFB /
        // (double) examples.size());

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
        // NumberStorage.add(prefix + "ErrViterbi", (double) wrongClassCounterFB
        // / (double) examples.size());

    }

}
