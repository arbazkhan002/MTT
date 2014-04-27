/**
 * 
 */
package lcrf;

import java.util.List;

import lcrf.counting.LogicalCountingTreeTrainer;
import lcrf.logic.Atom;
import lcrf.regression.RegressionModelTrainer;
import lcrf.stuff.NumberStorage;

import org.apache.log4j.Logger;

/**
 * @author Bernd Gutmann
 * 
 */
public class ModeTagging {
    public ModeTagging(SimpleExampleContainer trainFold, SimpleExampleContainer testFold, long seed,
            RegressionModelTrainer<List<Atom>> trainer, WindowMaker wm, LogicalCountingTreeTrainer trainer2,
            int crftrainsteps) {

        double averageLength = trainFold.averageSequenceLength();

        CRF crf = new CRF(trainFold.getClassAtoms(), trainer, wm, trainer2, seed);

        for (int step = 1; step <= crftrainsteps; step++) {
            Logger.getLogger("main.step").info("Step " + step + " of " + crftrainsteps);
            crf.trainOneStep(trainFold);
            Logger.getLogger("main.step.classification").info("Classify the traindata");
            tagAndLog(crf, trainFold);
            Logger.getLogger("main.step.classification").info("Classify the testdata");
            tagAndLog(crf, testFold);
        }
    }

    private void tagAndLog(CRF crf, SimpleExampleContainer examples) {
        int[] fb_diff = new int[(int)examples.averageSequenceLength() + 2];
        int[] fb_switch = new int[(int)examples.averageSequenceLength()+ 2];
        int[] vi_diff = new int[(int)examples.averageSequenceLength() + 2];
        int[] vi_switch = new int[(int)examples.averageSequenceLength() + 2];
        int itemsOverall = 0; // the count of all items in every sequence
        int itemsCorrect_fb = 0;
        int itemsCorrect_vi = 0;

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
            List<Atom> output = examples.getOutputSequence(i);
            List<Atom> outFB = crf.classifyFB(input);
            List<Atom> outVi = crf.classifyViterbi(input);
            
            loglikelihood += crf.getLogLikelihood(input,output);

            // enter values into the corellation counter
            for (int t = 0; t < examples.getOutputSequence(i).size(); t++) {
                int real = classAtoms.indexOf(examples.getOutputSequence(i).get(t));
                int indexFB = classAtoms.indexOf(outFB.get(t));
                int indexVi = classAtoms.indexOf(outVi.get(t));
                corellationCounterFB[real][indexFB]++;
                corellationCounterViterbi[real][indexVi]++;
                if (real != indexFB)
                    wrongClassCounterFB++;
                if (real != indexVi)
                    wrongClassCounterViterbi++;
            }

            int d_fb = getDifferentPositions(outFB, output);
            int d_vi = getDifferentPositions(outVi, output);

            itemsOverall += output.size();
            itemsCorrect_fb += output.size() - d_fb;
            itemsCorrect_vi += output.size() - d_vi;

            enterCount(d_fb, fb_diff);
            enterCount(d_vi, vi_diff);
        }
        
        Logger.getLogger("main.step.classification").info("Log-Likelihood        : "+loglikelihood);
        logCountTable(fb_diff, "Forward-Backward, wrong labels :");
        Logger.getLogger("main.step.classification").info(
                "Percent correct items : " + itemsCorrect_fb + "/" + itemsOverall + " = "
                        + (double) itemsCorrect_fb / (double) itemsOverall);
        logCountTable(vi_diff, "Viterbi, wrong labels :");
        Logger.getLogger("main.step.classification").info(
                "Percent correct items : " + itemsCorrect_vi + "/" + itemsOverall + " = "
                        + (double) itemsCorrect_vi / (double) itemsOverall);

        Logger.getLogger("main.step.classification").info("Predicted Items (FB):");
        for (int i = 0; i < classAtoms.size(); i++) {
            String line = "  Class " + classAtoms.get(i) + " : ";
            for (int j = 0; j < classAtoms.size(); j++) {
                line += "(" + classAtoms.get(j) + " : " + corellationCounterFB[i][j] + " times) ";
            }
            Logger.getLogger("main.step.classification").info(line);
        }
        Logger.getLogger("main.step.classification").info(
                wrongClassCounterFB + " Errors at " + examples.size() + " Test examples (" + 100.0
                        * (double) wrongClassCounterFB / (double) itemsOverall + " %)");

        Logger.getLogger("main.step.classification").info("Predicted Items (Viterbi):");
        for (int i = 0; i < classAtoms.size(); i++) {
            String line = "  Class " + classAtoms.get(i) + " : ";
            for (int j = 0; j < classAtoms.size(); j++) {
                line += "(" + classAtoms.get(j) + " : " + corellationCounterViterbi[i][j] + " times) ";                               
                
            }
            Logger.getLogger("main.step.classification").info(line);
        }
        Logger.getLogger("main.step.classification").info(
                wrongClassCounterViterbi + " Errors at " + examples.size() + " Test examples (" + 100.0
                        * (double) wrongClassCounterViterbi / (double) itemsOverall + " %)");        

    }

    private static void logCountTable(int[] table, String name) {
        int max = table.length - 2;
        int akku = 0;
        int counter = 0;

        Logger logger = Logger.getLogger("main.step.classification");
        logger.info("    *   *   *   *   *   *   *");
        logger.info(name);

        for (int i = 0; i < max; i++) {
            akku += table[i];
            counter += i * table[i];
            logger.info(" " + i + " errors   :  " + table[i] + " times   (akkumulated " + akku + ")");
        }

        akku += table[max];

        double average = ((double) counter + table[table.length - 1]) / ((double) akku);
        logger.info(" >" + max + " errors  :  " + table[max] + " time   (akkumulated " + akku + ")");
        logger.info(" Average : " + average);
        logger.info("    *   *   *   *   *   *   *");

        NumberStorage.add(name, average);
    }

    private static void enterCount(int count, int[] table) {
        if (count >= table.length - 2) {
            table[table.length - 2]++;
            table[table.length - 1] += count;
            return;
        }
        table[count]++;
    }

    private static int getDifferentPositions(List l1, List l2) {
        assert l1 != null;
        assert l2 != null;
        assert l1.size() == l2.size();

        int counter = 0;
        for (int i = 0; i < l1.size(); i++) {
            counter += (l1.get(i).equals(l2.get(i))) ? 0 : 1;
        }

        return counter;
    }

}
