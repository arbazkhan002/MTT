/*
 * Created on 08.03.2005
 */
package lcrf;

import java.io.Serializable;
import java.math.MathContext;
import java.util.List;
import java.util.Random;
import java.util.Vector;

import lcrf.counting.LogicalCountingTree;
import lcrf.counting.LogicalCountingTreeTrainer;
import lcrf.logic.Atom;
import lcrf.logic.Constant;
import lcrf.logic.Interpretation;
import lcrf.logic.parser.ParseException;
import lcrf.regression.RegressionExample;
import lcrf.regression.RegressionModel;
import lcrf.regression.RegressionModelSummer;
import lcrf.regression.RegressionModelTrainer;
import lcrf.stuff.ArrayStuff;
import lcrf.stuff.Timer;

import org.apache.log4j.Logger;

/**
 * @author Bernd Gutmann
 */
public class CRFInterpretation implements Serializable {
    private static final long serialVersionUID = 3690191044994151731L;

    // specifies how long the pseudo likelihood should be used
    // for generating the regession examples
    public static final int PSEUDOLIKELIHOODTRAINSTEPS = 0;

    // FIXME we generate n times the same potential with pseudo likelihood

    private MathContext mathContext;

    private Atom[] classAtom;

    // set by alphaScaled
    private double[] fbScalingConstant;

    private Vector<RegressionModelSummer<Interpretation>> classPotentials;
    private Vector<RegressionModel<Interpretation>> classPotentialsFirstPos;

    // filled by generateExamples
    private List<RegressionExample<Interpretation>> generatedExamples;

    private RegressionModelTrainer<Interpretation> regressionModelTrainer;

    private LogicalCountingTreeTrainer countingTreeTrainer;

    private Atom firstClassAtom = new Atom(new Constant("startOfSequence"));

    private Vector<Vector<Atom>> observedClassAtoms;

    private Vector<LogicalCountingTree> classCountingTree;

    private int traincounter;

    private Random rand;

    /**
     * @param classAtom
     * @param regressionModelTrainer
     * @param windowSize
     * @param countingTreeTrainer
     */
    public CRFInterpretation(List<Atom> classAtom,
            RegressionModelTrainer<Interpretation> regressionModelTrainer,
            LogicalCountingTreeTrainer countingTreeTrainer) {
        this(classAtom, regressionModelTrainer, countingTreeTrainer, 123456);
    }

    /**
     * @param classAtom
     * @param regressionModelTrainer
     * @param windowMaker
     * @param countingTreeTrainer
     * @param seed
     */
    public CRFInterpretation(List<Atom> classAtom,
            RegressionModelTrainer<Interpretation> regressionModelTrainer,
            LogicalCountingTreeTrainer countingTreeTrainer, long seed) {
        if (classAtom == null || classAtom.size() == 0)
            throw new IllegalArgumentException();

        this.classAtom = classAtom.toArray(new Atom[0]);
        this.regressionModelTrainer = regressionModelTrainer;

        this.countingTreeTrainer = countingTreeTrainer;

        this.classPotentials = new Vector<RegressionModelSummer<Interpretation>>(this.classAtom.length);
        for (int c = 0; c < this.classAtom.length; c++) {
            this.classPotentials.add(c, new RegressionModelSummer<Interpretation>());
        }

        this.traincounter = 0;
        this.rand = new Random(seed);

        this.mathContext = new MathContext(10);
    }
    
    



    /**
     * Goes through all class atoms and returns the index of the first class
     * atom which is more general than a.
     * 
     * @param a
     *            an atom
     * @return
     */
    private int getClassAtomIndex(Atom a) {
        for (int i = 0; i < classAtom.length; i++) {
            if (classAtom[i].isMoreGeneralThan(a)) {
                return i;
            }
        }
        throw new IllegalStateException(a.toString());
    }

    /**
     * Calls trainOneStep
     * 
     * <pre>
     * steps
     * </pre>
     * 
     * times.
     * 
     * @param examples
     * @param steps
     */
    public void train(InterpretationExampleContainer examples, int steps) {
        assert examples != null;
        assert steps >= 0;

        for (int step = 0; step < steps; step++) {
            trainOneStep(examples);
        }
    }

    /**
     * Runs the gradient tree boosting algorithm.
     * 
     * @param ex
     */
    public void trainOneStep(InterpretationExampleContainer ex) {
        if (ex == null)
            throw new IllegalArgumentException();

        
        Logger logger = Logger.getLogger(this.getClass());
        
        if (generatedExamples == null) {
            generatedExamples = new Vector<RegressionExample<Interpretation>>(ex.size() * classAtom.length
                    * (int) ex.averageSequenceLength(), 50);
        } else {
            generatedExamples.clear();
            System.gc();
            System.gc();
            System.gc();
        }

        
        if (classPotentialsFirstPos == null) {
            logger.info("Learn potentials for first positions");
            classPotentialsFirstPos = new Vector<RegressionModel<Interpretation>>(classAtom.length);
            for (int i_class=0; i_class<classAtom.length; i_class++) {
                generateExamplesFirstPos(i_class, ex);
                classPotentialsFirstPos.add(i_class, this.regressionModelTrainer.trainFromExamples(generatedExamples));
            }            
        }
        

        /*
         * if (observedClassAtoms == null) generateCountingTrees(ex);
         */

        Vector<RegressionModel<Interpretation>> gradientPotentials = new Vector<RegressionModel<Interpretation>>(
                classAtom.length);


        // train gradient-potential for each class
        Timer.startTimer("crf.trainstep");
        for (int c = 0; c < classAtom.length; c++) {
            Timer.startTimer("crf.genExamples");

            if (traincounter < CRFInterpretation.PSEUDOLIKELIHOODTRAINSTEPS) {
                logger.info("generate examples for classAtom[" + c + "]=" + this.classAtom[c]
                        + ", use pseudo-likelihood");
                throw new IllegalStateException();

                // generateExamplesPseudo(c, ex);
            } else {
                logger.info("generate examples for classAtom[" + c + "]=" + this.classAtom[c]
                        + ", use likelihood");
                generateExamples(c, ex);
            }

            logger.info(generatedExamples.size() + " examples have been generated, Time "
                    + Timer.getDurationFormatted("crf.genExamples"));

            gradientPotentials.add(c, this.regressionModelTrainer.trainFromExamples(generatedExamples));

        }

        // append the gradient-potentials to the potentials
        for (int c = 0; c < classAtom.length; c++) {
            this.classPotentials.get(c).addSubModel(gradientPotentials.get(c));
        }
        logger.info("trainstep finished, time " + Timer.getDurationFormatted("crf.trainstep"));
        logger.info("crf has now " + getParameterCount() + " parameters");

        traincounter++;
    }

    /**
     * Returns the number of the parameters that this crf has.
     * 
     * @return i>0
     */
    public int getParameterCount() {
        int counter = 0;
        for (RegressionModel potential : classPotentials) {
            counter += potential.getParameterCount();
        }

        return counter;
    }

    private Interpretation interMaker(int pos, List<Interpretation> input, Atom previousAtom, Atom currentAtom) {
//        Interpretation tmp = new Interpretation(input.get(pos));
        Interpretation tmp = input.get(pos).clone();
        try {
            tmp.add(new Atom("outPrev(" + previousAtom + ")"));
            // tmp.add(new Atom("outCurrent("+currentAtom+")"));
        } catch (ParseException e) {
            throw new RuntimeException(e);
        }

        return tmp;

    }
    
    
    
    private double[][] calcAlpha(List<Interpretation> input) {
        assert input != null;
        assert input.size() > 0;
        
        double[][] alpha = new double[this.classAtom.length][];

        // calc values a(k,0) forall k
        for (int k = 0; k < classAtom.length; k++) {
            alpha[k] = new double[input.size()];

            Interpretation inter = interMaker(0, input, firstClassAtom, this.classAtom[k]);
            alpha[k][0] = Math.exp(classPotentialsFirstPos.get(k).getValueFor(inter));
        }
        

        // calc values a(k,t) forall k and t>
        for (int t = 1; t < input.size(); t++) { // everey position
            for (int k = 0; k < this.classAtom.length; k++) { // every class
                for (int k2 = 0; k2 < this.classAtom.length; k2++) { // every
                    // class
                    Interpretation inter = interMaker(t, input, this.classAtom[k2], this.classAtom[k]);
                    alpha[k][t] += Math.exp(classPotentials.get(k).getValueFor(inter)) * alpha[k2][t - 1];
                }
            }
        }

        return alpha;
    }

    private double[][] calcBeta(List<Interpretation> input) {
        assert input != null;
        assert input.size()>0;
        

        if (input == null) {
            throw new IllegalArgumentException();
        }

        double[][] beta = new double[classAtom.length][];

        // set beta(k,T) forall k
        for (int k = 0; k < classAtom.length; k++) {
            beta[k] = new double[input.size()]; 
            beta[k][input.size() - 1] = 1.0d;
        }

        // set beta(k,t) forall k and t<T
        for (int t = input.size() - 2; t >= 0; t--) { // everey position
            for (int k = 0; k < classAtom.length; k++) { // every class
                for (int k2 = 0; k2 < classAtom.length; k2++) { // every class

                    Interpretation inter = interMaker(t, input, this.classAtom[k], this.classAtom[k2]);
                    if (t>0) {
                        beta[k][t] += Math.exp(classPotentials.get(k2).getValueFor(inter)) * beta[k2][t + 1];
                    } else {
                        beta[k][t] += Math.exp(classPotentialsFirstPos.get(k2).getValueFor(inter)) * beta[k2][t + 1];
                    }
                }
            }
        }
        return beta;
    }

    
    
    

    private double[][] calcAlphaScaled(List<Interpretation> input) {
        assert input != null;
        assert input.size() > 0;
        
        double[][] alpha = new double[this.classAtom.length][];
        fbScalingConstant = new double[input.size()];

        // calc values a(k,0) forall k
        for (int k = 0; k < classAtom.length; k++) {
            alpha[k] = new double[input.size()];

            Interpretation inter = interMaker(0, input, firstClassAtom, this.classAtom[k]);
            alpha[k][0] = Math.exp(classPotentialsFirstPos.get(k).getValueFor(inter));
            fbScalingConstant[0] += alpha[k][0];
        }
        
        fbScalingConstant[0] = 1.0d / fbScalingConstant[0];

        // normalize alpha[_][0]
        for (int k = 0; k < classAtom.length; k++) {
            alpha[k][0] = alpha[k][0] * fbScalingConstant[0];
        }

        // calc values a(k,t) forall k and t>
        for (int t = 1; t < input.size(); t++) { // everey position
            for (int k = 0; k < this.classAtom.length; k++) { // every class
                for (int k2 = 0; k2 < this.classAtom.length; k2++) { // every
                    // class
                    Interpretation inter = interMaker(t, input, this.classAtom[k2], this.classAtom[k]);
                    alpha[k][t] += Math.exp(classPotentials.get(k).getValueFor(inter)) * alpha[k2][t - 1];
                }
                fbScalingConstant[t] += alpha[k][t];
            }
            fbScalingConstant[t] = 1.0d / fbScalingConstant[t];
            // normalize alpha[_][t]
            for (int k = 0; k < classAtom.length; k++) {
                alpha[k][t] = alpha[k][t] * fbScalingConstant[t];
            }

        }

        return alpha;
    }

    private double[][] calcBetaScaled(List<Interpretation> input) {
        assert input != null;
        assert input.size()>0;
        
        if (this.fbScalingConstant == null) {
            throw new IllegalStateException();
        }

        if (input == null || fbScalingConstant.length != input.size()) {
            throw new IllegalArgumentException();
        }

        double[][] beta = new double[classAtom.length][];

        // set beta(k,T) forall k
        for (int k = 0; k < classAtom.length; k++) {
            beta[k] = new double[input.size()];

            beta[k][input.size() - 1] = fbScalingConstant[input.size() - 1];
        }

        // set beta(k,t) forall k and t<T
        for (int t = input.size() - 2; t >= 0; t--) { // everey position
            for (int k = 0; k < classAtom.length; k++) { // every class
                for (int k2 = 0; k2 < classAtom.length; k2++) { // every class

                    Interpretation inter = interMaker(t, input, this.classAtom[k], this.classAtom[k2]);
                    if (t>0) {
                        beta[k][t] += Math.exp(classPotentials.get(k2).getValueFor(inter)) * beta[k2][t + 1];
                    } else {
                        beta[k][t] += Math.exp(classPotentialsFirstPos.get(k2).getValueFor(inter)) * beta[k2][t + 1];
                    }
                    
                }
                beta[k][t] = beta[k][t] * fbScalingConstant[t];
            }
        }
        return beta;
    }
    
    
    private void generateExamplesFirstPos(int i_class, InterpretationExampleContainer examples) {
        generatedExamples.clear();
        
        for (int i_example=0; i_example < examples.size(); i_example++) {
            double value = 0.0d;
            if (classAtom[i_class].isMoreGeneralThan(examples.getOutputSequence(i_example).get(0))) {
                value = 1.0d;
            }
            
            generatedExamples.add(new RegressionExample<Interpretation>(examples.getInputInterpretations(i_example).get(0),value));            
        }
        
    }
    
   

    /**
     * This method generates examples for training a regression model.
     * 
     * @param i_class
     * @param examples
     */

    private void generateExamples(int i_class, InterpretationExampleContainer examples) {
        generatedExamples.clear();

        for (int i_example = 0; i_example < examples.size(); i_example++) {                       
            List<Interpretation> input = examples.getInputInterpretations(i_example);
            List<Atom> output = examples.getOutputSequence(i_example);
            
            assert input.size() == output.size();
            
            //skip empty sequences
            if (input.size()==0)
                continue;

            double[][] alpha = calcAlphaScaled(input);
            double[][] beta = calcBetaScaled(input);
            
            double zk = 0.0d;
            
            for (int k=0; k<classAtom.length; k++) {
                zk += alpha[k][input.size()-1];
            }

            for (int t = 1; t < input.size(); t++) {
                for (int i2_class = 0; i2_class < classAtom.length; i2_class++) {

                    Interpretation inter = this.interMaker(t, input,classAtom[i2_class],classAtom[i_class]);

                    double prob =  beta[i_class][t]
                            * Math.exp(classPotentials.get(i_class).getValueFor(inter))/zk;
                    if (t>0) {
                        prob *= alpha[i2_class][t-1];
                    }

                    double identity = 0.0d;

                    if (t > 0
                            && ((classAtom[i2_class].getTermRepresentation().hasVariables()) ? classAtom[i2_class]
                                    .isMoreGeneralThan(output.get(t - 1))
                                    : classAtom[i2_class].equals(output.get(t - 1)))
                            && ((classAtom[i_class].getTermRepresentation().hasVariables()) ? classAtom[i_class]
                                    .isMoreGeneralThan(output.get(t))
                                    : classAtom[i_class].equals(output.get(t)))) {
                        identity = 1.0d;
                    }
                    
                    //double rand = Math.random()*5 - 2.5;

                    generatedExamples.add(new RegressionExample<Interpretation>(inter, identity - prob));
                    //generatedExamples.add(new RegressionExample<Interpretation>(inter, rand));
                }
            }
        }
        //Logger.getLogger("dummy").info(generatedExamples);
    }

    public List<Atom> classifyViterbi(List<Interpretation> input) {
        assert input != null;
        
        //just for catching the extremal case
        if (input.size()==0)
            return new Vector<Atom>(0);

        double[][] delta = new double[input.size()][]; // delta_t(i)
        // t==firstindex
        int[][] psi = new int[input.size()][]; // psi_t(i) t==firstindex

        // initialization
        for (int t = 0; t < input.size(); t++) {
            delta[t] = new double[classAtom.length];
            psi[t] = new int[classAtom.length];
        }

        for (int i = 0; i < classAtom.length; i++) {
            Interpretation inter = this.interMaker(0, input, firstClassAtom, this.classAtom[i]);

            delta[0][i] = Math.exp(classPotentialsFirstPos.get(i).getValueFor(inter));
            psi[0][i] = 0;
        }

        // recursion
        for (int t = 1; t < input.size(); t++) {
            for (int j = 0; j < classAtom.length; j++) {
                Interpretation inter = this.interMaker(t, input, this.classAtom[0], this.classAtom[j]);

                double max = Math.exp(this.classPotentials.get(j).getValueFor(inter)) * delta[t - 1][0];
                int argmax = 0;

                for (int i = 1; i < this.classAtom.length; i++) { // every
                    // class
                    inter = this.interMaker(t, input, this.classAtom[i], this.classAtom[j]);

                    double tmp = Math.exp(this.classPotentials.get(j).getValueFor(inter)) * delta[t - 1][i];
                    if (tmp >= max) {
                        max = tmp;
                        argmax = i;
                    }
                }
                delta[t][j] = max;
                psi[t][j] = argmax;
            }
        }

        // termination
        int[] qsequence = new int[input.size()];
        double pstar = Double.MIN_VALUE;
        for (int i = 0; i < classAtom.length; i++) {
            if (delta[input.size() - 1][i] > pstar) {
                pstar = delta[input.size() - 1][i];
                qsequence[input.size() - 1] = i;
            }
        }

        for (int t = input.size() - 2; t >= 0; t--) {
            qsequence[t] = psi[t + 1][qsequence[t + 1]];
        }

        List<Atom> outputSequence = new Vector<Atom>(input.size());
        for (int t = 0; t < input.size(); t++) {
            outputSequence.add(classAtom[qsequence[t]]);
        }

        return outputSequence;
    }

    public List<Atom> classifyFB(List<Interpretation> input) {
        if (input == null)
            throw new IllegalArgumentException();
        
        //just for catching the extremal case
        if  (input.size() == 0) 
            return new Vector<Atom>(0);

        Vector<Atom> output = new Vector<Atom>(input.size());

        double[][] alpha = calcAlphaScaled(input);
        double[][] beta = calcBetaScaled(input);
        
        
        Logger.getLogger("fuck").debug(ArrayStuff.toString(alpha));
        Logger.getLogger("fuck").debug(ArrayStuff.toString(beta));
        
        
                

        for (int t = 0; t < input.size(); t++) {
            Logger.getLogger(getClass()).debug(" t=" + t);
            int maxindex = 0;
            double maxProb = alpha[0][t] * beta[0][t];
            
            Logger.getLogger(getClass()).debug("   "+0+" " +maxProb);
            
            

            for (int k = 1; k < classAtom.length; k++) {
                
                double prob = alpha[k][t] * beta[k][t];
                Logger.getLogger(getClass()).debug("   "+k+" " +prob);
                if (prob >= maxProb) {
                    maxProb = prob;
                    maxindex = k;
                }
            }

            Atom maxatom = classAtom[maxindex];

            output.add(classAtom[maxindex]);

        }

        return output;
    }

    /**
     * Samples an integer number distributed like the array.
     * 
     * @param countArray
     * @return
     */
    private int sampleState(int[] countArray) {
        int r = rand.nextInt(ArrayStuff.sumAll(countArray));
        int sum = countArray[0];
        int pos = 1;

        while (pos < countArray.length && sum < r) {
            sum += countArray[pos];
            pos++;
        }

        return pos - 1;
    }

    public Atom classifyFBMaxClassAtom(List<Interpretation> input) {
        assert input != null;
        int[] classCounts = new int[classAtom.length];

        for (Atom a : classifyFB(input)) {
            classCounts[getClassAtomIndex(a)]++;
        }

        return classAtom[ArrayStuff.argmax(classCounts)];
    }

    public Atom classifyViterbiMaxClassAtom(List<Interpretation> input) {
        assert input != null;
        int[] classCounts = new int[classAtom.length];

        for (Atom a : classifyViterbi(input)) {
            classCounts[getClassAtomIndex(a)]++;
        }

        return classAtom[ArrayStuff.argmax(classCounts)];
    }

    /**
     * Calculates the log-likelihood of the output given the input and the
     * current model
     * 
     * @param input
     * @param output
     * @return
     */
    public double getLogLikelihood(List<Interpretation> input, List<Atom> output) {
        if (input == null && output == null && input.size() != output.size() && input.size() == 0) {
            throw new IllegalArgumentException();
        }

        //run forward-step for setting the scaling factors
        double[][] alpha = calcAlphaScaled(input);

        // calc the normalizer
        double logZk = 0.0d;
        for (int t = 0; t < input.size(); t++) {
            logZk += Math.log(fbScalingConstant[t]);
        }
        
        //Logger.getLogger(getClass()).info("Size     = " + input.size());
        //Logger.getLogger(getClass()).info("log(Z(X) = " + result);
        //Logger.getLogger(getClass()).info("Scaling constant = " + ArrayStuff.toString(fbScalingConstant));
        

        double numerator = 0.0d;
        
        for (int t = 0; t < input.size(); t++) {
            Atom previous = (t == 0) ? this.firstClassAtom : output.get(t - 1);
            Atom actual = output.get(t);
            Interpretation inter = this.interMaker(t, input, previous, actual);

            int index = this.getClassAtomIndex(actual);
            if (t>0) {
                numerator += this.classPotentials.get(index).getValueFor(inter);
            } else {
                numerator += this.classPotentialsFirstPos.get(index).getValueFor(inter);                
            }
        }

        return numerator + logZk;
    }
    
    public double getLogLikelihoodLocal(List<Interpretation> input, List<Atom> output) {
        if (input == null && output == null && input.size() != output.size() && input.size() == 0) {
            throw new IllegalArgumentException();
        }

        //run forward-step for setting the scaling factors
        double[][] alpha = calcAlphaScaled(input);
        double[][] beta = calcBetaScaled(input);
        
        double result = 0.0d;


        for (int t = 0; t < input.size(); t++) {            
            int index = this.getClassAtomIndex(output.get(t));

            result += Math.log(alpha[index][t] * beta[index][t]);
        }

        return result;
    }

}
