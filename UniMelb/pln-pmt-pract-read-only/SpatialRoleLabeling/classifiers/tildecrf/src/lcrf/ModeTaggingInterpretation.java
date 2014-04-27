/**
 * 
 */
package lcrf;

import java.util.List;

import lcrf.counting.LogicalCountingTreeTrainer;
import lcrf.logic.Atom;
import lcrf.logic.Interpretation;
import lcrf.regression.RegressionModelTrainer;
import lcrf.stuff.ArrayStuff;
import lcrf.stuff.NumberStorage;

import org.apache.log4j.Logger;

/**
 * @author Bernd Gutmann
 * 
 */
public class ModeTaggingInterpretation {
    public ModeTaggingInterpretation(InterpretationExampleContainer trainFold, InterpretationExampleContainer testFold, long seed,
            RegressionModelTrainer<Interpretation> trainer, WindowMaker wm, LogicalCountingTreeTrainer trainer2,
            int crftrainsteps) {

        double averageLength = trainFold.averageSequenceLength();

        CRFInterpretation crf = new CRFInterpretation(trainFold.getClassAtoms(), trainer, trainer2, seed);
        
        for (int step = 1; step <= crftrainsteps; step++) {
            Logger.getLogger("main.step").info("Step " + step + " of " + crftrainsteps);
            crf.trainOneStep(trainFold);
            Logger.getLogger("main.step.classification").info("Classify the traindata");
            tagAndLog(crf, trainFold);
            Logger.getLogger("main.step.classification").info("Classify the testdata");
            tagAndLog(crf, testFold);
        }
    }

    private void tagAndLog(CRFInterpretation crf, InterpretationExampleContainer examples) {
        int[] fb_diff = new int[(int)examples.averageSequenceLength() + 2];
        int[] vi_diff = new int[(int)examples.averageSequenceLength() + 2];
        
        List<Atom> classAtoms = examples.getClassAtoms();
        int[][] corellationCounterViterbi = new int[classAtoms.size()][];
        int[][] corellationCounterFB = new int[classAtoms.size()][];
        for (int i = 0; i < examples.getClassAtoms().size(); i++) {
            corellationCounterViterbi[i] = new int[classAtoms.size()];
            corellationCounterFB[i] = new int[classAtoms.size()];
        }
        
        double loglikelihood = 0.0d;
        double loglikelihoodlocal = 0.0d;

        for (int i = 0; i < examples.size(); i++) {
            List<Interpretation> input = examples.getInputInterpretations(i);
            List<Atom> output = examples.getOutputSequence(i);
            //Logger.getLogger("hurz").debug(input);
            //Logger.getLogger("hurz").debug(output);
            List<Atom> outFB = crf.classifyFB(input);
            List<Atom> outVi = crf.classifyViterbi(input);
            
            Logger.getLogger("h").info(input);
            Logger.getLogger("hin").info(output);
            Logger.getLogger("hir").info(outFB);
            Logger.getLogger("hin").info("**************");

            
            loglikelihood += crf.getLogLikelihood(input,output);
            loglikelihoodlocal += crf.getLogLikelihoodLocal(input,output);

            // enter values into the corellation counter
            for (int t = 0; t < examples.getOutputSequence(i).size(); t++) {
                int real = classAtoms.indexOf(examples.getOutputSequence(i).get(t));
                int indexFB = classAtoms.indexOf(outFB.get(t));
                int indexVi = classAtoms.indexOf(outVi.get(t));
                corellationCounterFB[real][indexFB]++;
                corellationCounterViterbi[real][indexVi]++;
            }
            
        }
        
        Logger.getLogger("main.step.classification").info("Log-Likelihood        : "+loglikelihood);
        Logger.getLogger("main.step.classification").info("Log-Likelihood-Local  : "+loglikelihoodlocal);
        Logger.getLogger("main.step.classification").info("Forward-Backward\n"+
                ArrayStuff.toConfusionMatrix(classAtoms,corellationCounterFB));
        Logger.getLogger("main.step.classification").info("Viterbi\n"+
                ArrayStuff.toConfusionMatrix(classAtoms,corellationCounterViterbi));

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
