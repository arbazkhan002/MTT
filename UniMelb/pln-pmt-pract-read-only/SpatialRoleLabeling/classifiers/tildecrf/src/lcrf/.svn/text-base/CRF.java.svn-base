/*
 * Created on 08.03.2005
 */
package lcrf;

import java.io.Serializable;
import java.math.MathContext;
import java.util.List;
import java.util.Random;
import java.util.Vector;

import lcrf.counting.CountingExample;
import lcrf.counting.LogicalCountingTree;
import lcrf.counting.LogicalCountingTreeTrainer;
import lcrf.logic.Atom;
import lcrf.logic.Constant;
import lcrf.logic.Interpretation;
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
public class CRF implements Serializable {
    private static final long serialVersionUID = 3690191044994151731L;

    // specifies how long the pseudo likelihood should be used
    // for generating the regession examples
    public static final int PSEUDOLIKELIHOODTRAINSTEPS = 0;

    // FIXME we generate n times the same potential with pseudo likelihood

    private MathContext mathContext;

    private Atom[] classAtom;

    // set by alphaScaled
    private double[] fbScalingConstant;

    private Vector<RegressionModelSummer<List<Atom>>> classPotentials;

    // filled by generateExamples
    private List<RegressionExample<List<Atom>>> generatedExamples;

    private RegressionModelTrainer<List<Atom>> regressionModelTrainer;

    private LogicalCountingTreeTrainer countingTreeTrainer;

    private Atom firstClassAtom;

    private WindowMaker wm;

    private Vector<Vector<Atom>> observedClassAtoms;

    private Vector<LogicalCountingTree> classCountingTree;

    private int traincounter;

    private Random rand;

    
    /**
     * 
     * @param classAtom
     * @param regressionModelTrainer
     * @param windowSize
     * @param countingTreeTrainer
     */
    public CRF(List<Atom> classAtom, RegressionModelTrainer<List<Atom>> regressionModelTrainer,
            int windowSize, LogicalCountingTreeTrainer countingTreeTrainer) {
        this(classAtom, regressionModelTrainer, new WindowMaker(windowSize), countingTreeTrainer, 123456);
    }

    
    /**
     * 
     * @param classAtom
     * @param regressionModelTrainer
     * @param windowMaker
     * @param countingTreeTrainer
     * @param seed
     */
    public CRF(List<Atom> classAtom, RegressionModelTrainer<List<Atom>> regressionModelTrainer,
            WindowMaker windowMaker, LogicalCountingTreeTrainer countingTreeTrainer, long seed) {
        if (classAtom == null || classAtom.size() == 0)
            throw new IllegalArgumentException();

        this.classAtom = classAtom.toArray(new Atom[0]);
        this.regressionModelTrainer = regressionModelTrainer;
        this.wm = windowMaker;
        this.countingTreeTrainer = countingTreeTrainer;
        this.firstClassAtom = new Atom(new Constant("f_i_r_s_t_c_l_a_s_s_ATOM"));

        this.classPotentials = new Vector<RegressionModelSummer<List<Atom>>>(this.classAtom.length);
        for (int c = 0; c < this.classAtom.length; c++) {
            this.classPotentials.add(c, new RegressionModelSummer<List<Atom>>());
        }

        this.traincounter = 0;
        this.rand = new Random(seed);

        this.mathContext = new MathContext(10);
    }

    /**
     * This method takes all sequences, generates for each class atom that has
     * variables training examples and trains a logical counting tree.
     * 
     * @param ex
     */
    private void generateCountingTrees(ExampleContainer ex) {
        Vector<CountingExample> countingExamples = new Vector<CountingExample>(ex.size()
                * (int) ex.averageSequenceLength() + 1);

        observedClassAtoms = new Vector<Vector<Atom>>(classAtom.length);
        classCountingTree = new Vector<LogicalCountingTree>(classAtom.length);

        for (int i = 0; i < classAtom.length; i++) {
            Atom a0 = classAtom[i];
            if (!a0.getTermRepresentation().hasVariables()) {
                Vector<Atom> observed = new Vector<Atom>(1);
                observed.add(a0);
                observedClassAtoms.add(i, observed);
                classCountingTree.add(i, null);
            } else {
                Vector<Atom> observed = new Vector<Atom>();
                countingExamples.clear();

                for (int j = 0; j < ex.size(); j++) {
                    List<Atom> input = ex.getInputSequence(j);
                    List<Atom> output = ex.getOutputSequence(j);

                    wm.setInputsequence(input);

                    for (int t = 0; t < input.size(); t++) {
                        Atom a = output.get(t);
                        // this atom is relevant for this class atom
                        if (a0.isMoreGeneralThan(a)) {
                            int pos = observed.indexOf(a);
                            // we haven't seen it yet
                            if (pos == -1) {
                                observed.add(a);
                                pos = observed.indexOf(a, observed.size() - 1);
                            }
                            if (pos == -1)
                                throw new IllegalStateException();
                            // generate training example for counting tree
                            List<Atom> window = wm.make(t, (t == 0) ? firstClassAtom : output.get(t - 1),
                                    output.get(t));

                            countingExamples.add(new CountingExample(window, pos));
                        }
                    }
                }

                // now train counting tree from examples
                if (observed.size() == 0) {
                    throw new IllegalStateException(
                            "We havent seen any training examples for this class atom");
                }

                classCountingTree.add(i, countingTreeTrainer.trainFromExamples(countingExamples, observed
                        .size()));
                observedClassAtoms.add(i, observed);
            }
        }
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
     * Calls trainOneStep <pre>steps</pre> times.
     * 
     * @param examples 
     * @param steps
     */
    public void train(ExampleContainer examples, int steps) {
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
    public void trainOneStep(ExampleContainer ex) {
        Logger logger = Logger.getLogger(this.getClass());
        if (ex == null)
            throw new IllegalArgumentException();

        if (observedClassAtoms == null)
            generateCountingTrees(ex);

        Vector<RegressionModel<List<Atom>>> gradientPotentials = new Vector<RegressionModel<List<Atom>>>(
                classAtom.length);

        if (generatedExamples == null) {
            generatedExamples = new Vector<RegressionExample<List<Atom>>>(ex.size() * classAtom.length
                    * (int) ex.averageSequenceLength(), 50);
        } else {
            generatedExamples.clear();
        }

        // train gradient-potential for each class
        Timer.startTimer("crf.trainstep");
        for (int c = 0; c < classAtom.length; c++) {
            Timer.startTimer("crf.genExamples");

            if (traincounter < CRF.PSEUDOLIKELIHOODTRAINSTEPS) {
                logger.info("generate examples for classAtom[" + c + "]=" + this.classAtom[c]
                        + ", use pseudo-likelihood");
                
                generateExamplesPseudo(c, ex);
            } else {
                logger.info("generate examples for classAtom[" + c + "]=" + this.classAtom[c]
                        + ", use likelihood");
                generateExamples(c, ex);
            }

            logger.info(generatedExamples.size() + " examples have been generated, Time "
                    + Timer.getDurationFormatted("crf.genExamples"));

            /*
             * HashSet<List<Atom>> allExamples = new HashSet<List<Atom>>(generatedExamples.size());
             * for (RegressionExample<List<Atom>> exa:generatedExamples)
             * allExamples.add(exa.content); logger.info(allExamples.size() + "
             * different window bodies have been generated");
             */

            // List<TermSchema> schemata =
            // ((LogicalRegressionTreeTrainer)(((TrainerWrapper)regressionModelTrainer).internalTrainer)).schemata;
            // LogicalRegressionTreeTrainer specialTrainer = new
            // LogicalRegressionTreeTrainer(5,1,schemata,wm.getFieldTypes());
            // RegressionModelTrainer<List<Atom>> specialTrainerWrapper = new
            // TrainerWrapper<List<Atom>>(specialTrainer);
            // if (c == 0) {
            // logger.info("Use normal Trainer");
            gradientPotentials.add(c, this.regressionModelTrainer.trainFromExamples(generatedExamples));
            /*
             * } else { logger.info("Use special Trainer");
             * gradientPotentials.add(c,
             * specialTrainerWrapper.trainFromExamples(generatedExamples)); }
             */

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


    /**
     * This method is the forward step of the fb-algorithm. KnownOutput contains
     * the elements of the output sequence that are already known. Both list
     * have to be equally long, unknown output elements are null.
     * 
     * @param input
     * @param knownOutput
     * @return
     */
    private double[][] calcAlpha(List<Atom> input, List<Atom> knownOutput) {
        assert input != null;
        assert knownOutput != null;
        assert input.size() == knownOutput.size();

        double[][] alpha = new double[this.classAtom.length][];

        wm.setInputsequence(input);

        // calc values a(k,0) forall k
        for (int k = 0; k < classAtom.length; k++) {
            alpha[k] = new double[input.size()];
            List<Atom> window = wm.make(0, firstClassAtom, this.classAtom[k]);
            if (knownOutput.get(0) == null || knownOutput.get(0).equals(classAtom[k])) {
                alpha[k][0] = Math.exp(classPotentials.get(k).getValueFor(window));
            } else {
                alpha[k][0] = 0.0;
            }
        }

        // calc values a(k,t) forall k and t>
        for (int t = 1; t < input.size(); t++) { // everey position
            for (int k = 0; k < this.classAtom.length; k++) { // every class
                if (knownOutput.get(t) == null || knownOutput.get(t).equals(classAtom[k])) {
                    for (int k2 = 0; k2 < this.classAtom.length; k2++) { // every
                        // class
                        List<Atom> window = wm.make(t, this.classAtom[k2], this.classAtom[k]);
                        alpha[k][t] += Math.exp(classPotentials.get(k).getValueFor(window))
                                * alpha[k2][t - 1];
                    }
                } else {
                    alpha[k][t] = 0.0;
                }
            }
        }

        return alpha;
    }

    private double[][] calcAlpha(List<Atom> input) {
        double[][] alpha = new double[this.classAtom.length][];

        wm.setInputsequence(input);

        // calc values a(k,0) forall k
        for (int k = 0; k < classAtom.length; k++) {
            alpha[k] = new double[input.size()];
            List<Atom> window = wm.make(0, firstClassAtom, this.classAtom[k]);
            alpha[k][0] = Math.exp(classPotentials.get(k).getValueFor(window));
        }

        // calc values a(k,t) forall k and t>
        for (int t = 1; t < input.size(); t++) { // everey position
            for (int k = 0; k < this.classAtom.length; k++) { // every class
                for (int k2 = 0; k2 < this.classAtom.length; k2++) { // every
                    // class
                    List<Atom> window = wm.make(t, this.classAtom[k2], this.classAtom[k]);
                    alpha[k][t] += Math.exp(classPotentials.get(k).getValueFor(window)) * alpha[k2][t - 1];
                }
            }
        }

        return alpha;
    }

    private double[][] calcAlphaScaled(List<Atom> input) {
        double[][] alpha = new double[this.classAtom.length][];
        fbScalingConstant = new double[input.size()];

        wm.setInputsequence(input);

        // calc values a(k,0) forall k
        for (int k = 0; k < classAtom.length; k++) {
            alpha[k] = new double[input.size()];
            List<Atom> window = wm.make(0, firstClassAtom, this.classAtom[k]);
            alpha[k][0] = Math.exp(classPotentials.get(k).getValueFor(window));
            fbScalingConstant[0] += alpha[k][0];
        }

        // normalize alpha[_][0]
        for (int k = 0; k < classAtom.length; k++) {
            alpha[k][0] = alpha[k][0] / fbScalingConstant[0];
        }

        // calc values a(k,t) forall k and t>
        for (int t = 1; t < input.size(); t++) { // everey position
            for (int k = 0; k < this.classAtom.length; k++) { // every class
                for (int k2 = 0; k2 < this.classAtom.length; k2++) { // every
                    // class
                    List<Atom> window = wm.make(t, this.classAtom[k2], this.classAtom[k]);
                    alpha[k][t] += Math.exp(classPotentials.get(k).getValueFor(window)) * alpha[k2][t - 1];
                }
                fbScalingConstant[t] += alpha[k][t];
            }
            // normalize alpha[_][t]
            for (int k = 0; k < classAtom.length; k++) {
                alpha[k][t] = alpha[k][t] / fbScalingConstant[t];
            }

        }

        return alpha;
    }

    /**
     * @param input
     * @param knownOutput
     * @return
     */
    private double[][] calcBeta(List<Atom> input, List<Atom> knownOutput) {
        double[][] beta = new double[classAtom.length][];

        wm.setInputsequence(input);

        // set beta(k,T) forall k
        for (int k = 0; k < classAtom.length; k++) {
            beta[k] = new double[input.size()];
            if (knownOutput.get(input.size() - 1) == null
                    || knownOutput.get(input.size() - 1).equals(classAtom[k])) {
                beta[k][input.size() - 1] = 1.0;
            } else {
                beta[k][input.size() - 1] = 0.0;
            }
        }

        // set beta(k,t) forall k and t<T
        for (int t = input.size() - 2; t >= 0; t--) { // everey position
            for (int k = 0; k < classAtom.length; k++) { // every class
                if (knownOutput.get(input.size() - 1) == null
                        || knownOutput.get(input.size() - 1).equals(classAtom[k])) {
                    for (int k2 = 0; k2 < classAtom.length; k2++) { // every
                        // class
                        List<Atom> window = wm.make(t + 1, this.classAtom[k], this.classAtom[k2]);
                        beta[k][t] += Math.exp(classPotentials.get(k2).getValueFor(window)) * beta[k2][t + 1];
                    }
                } else {
                    beta[k][t] = 0.0;
                }
            }
        }
        return beta;
    }

    private double[][] calcBeta(List<Atom> input) {
        double[][] beta = new double[classAtom.length][];

        wm.setInputsequence(input);

        // set beta(k,T) forall k
        for (int k = 0; k < classAtom.length; k++) {
            beta[k] = new double[input.size()];
            beta[k][input.size() - 1] = 1.0;
        }

        // set beta(k,t) forall k and t<T
        for (int t = input.size() - 2; t >= 0; t--) { // everey position
            for (int k = 0; k < classAtom.length; k++) { // every class
                for (int k2 = 0; k2 < classAtom.length; k2++) { // every class
                    List<Atom> window = wm.make(t + 1, this.classAtom[k], this.classAtom[k2]);
                    beta[k][t] += Math.exp(classPotentials.get(k2).getValueFor(window)) * beta[k2][t + 1];
                }
            }
        }
        return beta;
    }

    private double[][] calcBetaScaled(List<Atom> input) {
        if (this.fbScalingConstant == null) {
            throw new IllegalStateException();
        }

        if (input == null || fbScalingConstant.length != input.size()) {
            throw new IllegalArgumentException();
        }

        double[][] beta = new double[classAtom.length][];

        wm.setInputsequence(input);

        // set beta(k,T) forall k
        for (int k = 0; k < classAtom.length; k++) {
            beta[k] = new double[input.size()];
            
            //FIXME
            beta[k][input.size() - 1] = 1.0 / fbScalingConstant[input.size() - 1];
        }

        // set beta(k,t) forall k and t<T
        for (int t = input.size() - 2; t >= 0; t--) { // everey position
            for (int k = 0; k < classAtom.length; k++) { // every class
                for (int k2 = 0; k2 < classAtom.length; k2++) { // every class
                    List<Atom> window = wm.make(t + 1, this.classAtom[k], this.classAtom[k2]);
                    beta[k][t] += Math.exp(classPotentials.get(k2).getValueFor(window)) * beta[k2][t + 1];
                }
                beta[k][t] = beta[k][t] / fbScalingConstant[t];
            }
        }
        return beta;
    }

    

    /**
     * This method generates examples for training a regression model.
     * 
     * @param i_class
     * @param examples
     */

    private void generateExamples(int i_class, ExampleContainer examples) {
        generatedExamples.clear();

        for (int i_example = 0; i_example < examples.size(); i_example++) {
            List<Atom> input = examples.getInputSequence(i_example);
            List<Atom> output = examples.getOutputSequence(i_example);

            wm.setInputsequence(input);

            // inserted ..Scaled
            double[][] alpha = calcAlphaScaled(input);
            double[][] beta = calcBetaScaled(input);

            // calc the normalizer
            /*
             * double zk = 0.0d; for (int k = 0; k < classAtom.length; k++) { zk +=
             * alpha[k][input.size() - 1]; }
             */

            for (int t = 0; t < input.size(); t++) {
                for (int i2_class = 0; i2_class < classAtom.length; i2_class++) {
                    List<Atom> window = wm.make(t, this.classAtom[i2_class], this.classAtom[i_class]);

                    double prob = alpha[i2_class][Math.max(t - 1, 0)] * beta[i_class][t]
                            * Math.exp(classPotentials.get(i_class).getValueFor(window));

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

                    RegressionExample<List<Atom>> ex = new RegressionExample<List<Atom>>(window, identity - prob);
                    ex.weight = (identity == 1.0d) ? this.classAtom.length*this.classAtom.length -1 : 1.0d;
                    generatedExamples.add(ex);
                }
            }
        }
    }

    /**
     * @param i_class
     * @param examples
     */
    private void generateExamplesPseudo(int i_class, ExampleContainer examples) {
        generatedExamples.clear();

        for (int i_example = 0; i_example < examples.size(); i_example++) {
            List<Atom> input = examples.getInputSequence(i_example);
            List<Atom> output = examples.getOutputSequence(i_example);

            wm.setInputsequence(input);

            // FIXME first and last position of the sequences are omitted
            for (int t = 1; t < input.size() - 1; t++) {
                double denom = 0.0d;

                for (int i3_class = 0; i3_class < classAtom.length; i3_class++) {
                    List<Atom> window1 = wm.make(t, output.get(t - 1), classAtom[i3_class]);
                    List<Atom> window2 = wm.make(t, classAtom[i3_class], output.get(t + 1));

                    double pot1 = this.classPotentials.get(i3_class).getValueFor(window1);
                    double pot2 = this.classPotentials.get(getClassAtomIndex(output.get(t + 1))).getValueFor(
                            window2);

                    denom += Math.exp(pot1 + pot2);
                }

                for (int i2_class = 0; i2_class < classAtom.length; i2_class++) {
                    List<Atom> window1 = wm.make(t, output.get(t - 1), classAtom[i_class]);
                    List<Atom> window2 = wm.make(t, classAtom[i_class], output.get(t + 1));

                    List<Atom> window3 = wm.make(t, output.get(t - 1), classAtom[i2_class]);
                    List<Atom> window4 = wm.make(t, classAtom[i2_class], output.get(t + 1));

                    List<Atom> window = wm.make(t, classAtom[i2_class], classAtom[i_class]);

                    double pot1 = this.classPotentials.get(i_class).getValueFor(window1);
                    double pot2 = this.classPotentials.get(getClassAtomIndex(output.get(t + 1))).getValueFor(
                            window2);
                    double pot3 = this.classPotentials.get(i2_class).getValueFor(window3);
                    double pot4 = this.classPotentials.get(getClassAtomIndex(output.get(t + 1))).getValueFor(
                            window4);

                    double id1 = 0.0d, id2 = 0.0d, id3 = 0.0d, id4 = 0.0d, id5 = 0.0d, id6 = 0.0d;

                    if (((classAtom[i_class].getTermRepresentation().hasVariables()) ? classAtom[i_class]
                            .isMoreGeneralThan(output.get(t)) : classAtom[i_class].equals(output.get(t)))
                            && ((classAtom[i2_class].getTermRepresentation().hasVariables()) ? classAtom[i2_class]
                                    .isMoreGeneralThan(output.get(t - 1))
                                    : classAtom[i2_class].equals(output.get(t - 1)))) {
                        id1 = 1.0d;
                    }

                    if (((classAtom[i_class].getTermRepresentation().hasVariables()) ? classAtom[i_class]
                            .isMoreGeneralThan(output.get(t + 1)) : classAtom[i_class].equals(output
                            .get(t + 1)))
                            && ((classAtom[i2_class].getTermRepresentation().hasVariables()) ? classAtom[i2_class]
                                    .isMoreGeneralThan(output.get(t))
                                    : classAtom[i2_class].equals(output.get(t)))) {
                        id2 = 1.0d;
                    }

                    if ((classAtom[i2_class].getTermRepresentation().hasVariables()) ? classAtom[i2_class]
                            .isMoreGeneralThan(output.get(t - 1)) : classAtom[i2_class].equals(output
                            .get(t - 1))) {
                        id3 = 1.0d;
                    }

                    if ((classAtom[i2_class].getTermRepresentation().hasVariables()) ? classAtom[i2_class]
                            .isMoreGeneralThan(output.get(t - 1)) : classAtom[i2_class].equals(output
                            .get(t - 1))) {
                        id3 = 1.0d;
                    }

                    if ((classAtom[i_class].getTermRepresentation().hasVariables()) ? classAtom[i_class]
                            .isMoreGeneralThan(output.get(t + 1)) : classAtom[i_class].equals(output
                            .get(t + 1))
                            && i_class == i2_class) {
                        id4 = 1.0d;
                    }

                    if ((classAtom[i_class].getTermRepresentation().hasVariables()) ? classAtom[i_class]
                            .isMoreGeneralThan(output.get(t + 1)) : classAtom[i_class].equals(output
                            .get(t + 1))) {
                        id5 = 1.0d;
                    }

                    if ((classAtom[i2_class].getTermRepresentation().hasVariables()) ? classAtom[i2_class]
                            .isMoreGeneralThan(output.get(t - 1)) : classAtom[i_class].equals(output
                            .get(t + 1))
                            && i_class == i2_class) {
                        id6 = 1.0d;
                    }

                    double value = id1 + id2
                            + (Math.exp(pot1 + pot2) * (id3 + id4) + Math.exp(pot3 + pot4) * (id5 + id6))
                            / denom;

                    generatedExamples.add(new RegressionExample<List<Atom>>(window, value));
                }
            }
        }
    }

    /**
     * @param input
     * @param knownOutput
     * @return
     */
    public List<Atom> classifyViterbi(List<Atom> input, List<Atom> knownOutput) {
        assert input != null;

        double[][] delta = new double[input.size()][]; // delta_t(i)
        // t==firstindex
        int[][] psi = new int[input.size()][]; // psi_t(i) t==firstindex

        // initialization
        for (int t = 0; t < input.size(); t++) {
            delta[t] = new double[classAtom.length];
            psi[t] = new int[classAtom.length];
        }

        wm.setInputsequence(input);

        for (int k = 0; k < classAtom.length; k++) {
            if (knownOutput.get(0) == null || knownOutput.get(0).equals(classAtom[k])) {
                delta[0][k] = Math.exp(classPotentials.get(k).getValueFor(
                        wm.make(0, firstClassAtom, this.classAtom[k])));
            } else {
                delta[0][k] = 0.0;
            }
            psi[0][k] = 0;
        }

        // recursion
        for (int t = 1; t < input.size(); t++) {
            for (int k = 0; k < classAtom.length; k++) {
                List<Atom> window = wm.make(t, this.classAtom[0], this.classAtom[k]);
                double max = Math.exp(this.classPotentials.get(k).getValueFor(window)) * delta[t - 1][0];
                int argmax = 0;

                for (int k2 = 1; k2 < this.classAtom.length; k2++) { // every
                    // class
                    window = wm.make(t, this.classAtom[k2], this.classAtom[k]);
                    double tmp = 0.0;
                    if (knownOutput.get(t) == null || knownOutput.get(t).equals(classAtom[k])) {
                        tmp = Math.exp(this.classPotentials.get(k).getValueFor(window)) * delta[t - 1][k2];
                    }
                    if (tmp > max) {
                        max = tmp;
                        argmax = k2;
                    }
                }
                delta[t][k] = max;
                psi[t][k] = argmax;
            }
        }

        // termination
        int[] qsequence = new int[input.size()];
        double pstar = Double.NEGATIVE_INFINITY;
        // double pstar = Double.MIN_VALUE;
        for (int k = 0; k < classAtom.length; k++) {
            if (delta[input.size() - 1][k] > pstar) {
                pstar = delta[input.size() - 1][k];
                qsequence[input.size() - 1] = k;
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

    public List<Atom> classifyViterbi(List<Atom> input) {
        assert input != null;

        double[][] delta = new double[input.size()][]; // delta_t(i)
        // t==firstindex
        int[][] psi = new int[input.size()][]; // psi_t(i) t==firstindex

        // initialization
        for (int t = 0; t < input.size(); t++) {
            delta[t] = new double[classAtom.length];
            psi[t] = new int[classAtom.length];
        }

        wm.setInputsequence(input);

        for (int i = 0; i < classAtom.length; i++) {
            delta[0][i] = Math.exp(classPotentials.get(i).getValueFor(
                    wm.make(0, firstClassAtom, this.classAtom[i])));
            psi[0][i] = 0;
        }

        // recursion
        for (int t = 1; t < input.size(); t++) {
            for (int j = 0; j < classAtom.length; j++) {
                List<Atom> window = wm.make(t, this.classAtom[0], this.classAtom[j]);
                double max = Math.exp(this.classPotentials.get(j).getValueFor(window)) * delta[t - 1][0];
                int argmax = 0;

                for (int i = 1; i < this.classAtom.length; i++) { // every
                    // class
                    window = wm.make(t, this.classAtom[i], this.classAtom[j]);
                    double tmp = Math.exp(this.classPotentials.get(j).getValueFor(window)) * delta[t - 1][i];
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

    public List<Atom> classifyFB(List<Atom> input, List<Atom> knownOutput) {
        if (input == null)
            throw new IllegalArgumentException();

        Vector<Atom> output = new Vector<Atom>(input.size());

        double[][] alpha = calcAlpha(input, knownOutput);
        double[][] beta = calcBeta(input, knownOutput);

        for (int t = 0; t < input.size(); t++) {
            // if we know the output-atom already, just copy it
            // into the output
            if (knownOutput.get(t) != null) {
                output.add(knownOutput.get(t));
                continue;
            }
            int maxindex = 0;
            double maxProb = alpha[0][t] * beta[0][t];

            /*
             * double zk = 0; //normalizer for (int i=0; i <classAtom.length;
             * i++) { zk += alpha[i][t] * beta[i][t]; }
             */

            for (int k = 1; k < classAtom.length; k++) {
                double prob = alpha[k][t] * beta[k][t];
                if (prob >= maxProb) {
                    maxProb = prob;
                    maxindex = k;
                }
            }

            Atom maxatom = classAtom[maxindex];

            if (maxatom.getTermRepresentation().hasVariables()) {
                // FIXME wm should have the actual input sequence?
                List<Atom> window = wm.make(t, (t == 0) ? firstClassAtom : output.get(t - 1), maxatom);
                int state = sampleState(classCountingTree.get(maxindex).getCountArrayFor(window));
                output.add(observedClassAtoms.get(maxindex).get(state));
            } else {
                output.add(classAtom[maxindex]);
            }
        }

        return output;
    }

    public List<Atom> classifyFB(List<Atom> input) {
        if (input == null)
            throw new IllegalArgumentException();

        Vector<Atom> output = new Vector<Atom>(input.size());

        double[][] alpha = calcAlpha(input);
        double[][] beta = calcBeta(input);

        for (int t = 0; t < input.size(); t++) {
            int maxindex = 0;
            double maxProb = alpha[0][t] * beta[0][t];

            /*
             * double zk = 0; //normalizer for (int i=0; i <classAtom.length;
             * i++) { zk += alpha[i][t] * beta[i][t]; }
             */

            for (int k = 1; k < classAtom.length; k++) {
                double prob = alpha[k][t] * beta[k][t];
                if (prob >= maxProb) {
                    maxProb = prob;
                    maxindex = k;
                }
            }

            Atom maxatom = classAtom[maxindex];

            if (maxatom.getTermRepresentation().hasVariables()) {
                // FIXME wm should have the actual input sequence?
                List<Atom> window = wm.make(t, (t == 0) ? firstClassAtom : output.get(t - 1), maxatom);
                int state = sampleState(classCountingTree.get(maxindex).getCountArrayFor(window));
                output.add(observedClassAtoms.get(maxindex).get(state));
            } else {
                output.add(classAtom[maxindex]);
            }
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

    public Atom classifyFBMaxClassAtom(List<Atom> input) {
        assert input != null;
        
        int[] classCounts = new int[classAtom.length];

        for (Atom a : classifyFB(input)) {
            classCounts[getClassAtomIndex(a)]++;
        }

        return classAtom[ArrayStuff.argmax(classCounts)];
    }

    public Atom classifyViterbiMaxClassAtom(List<Atom> input) {
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
    public double getLogLikelihood(List<Atom> input, Atom classification) {
        if (input == null || classification == null) {
            throw new IllegalArgumentException();
        }
    
        //extremal case
        if (input.size() == 0) {
                return Math.log(1/classAtom.length);
        }

        //run forward-step for setting the scaling factors
        double[][] alpha = calcAlphaScaled(input);

        // calc the normalizer
        double logZk = 0.0d;
        for (int t = 0; t < input.size(); t++) {
            logZk += Math.log(fbScalingConstant[t]);
        }
        

        double numerator = 0.0d;        
        int index = this.getClassAtomIndex(classification);
        
        for (int t = 0; t < input.size(); t++) {
            Atom previous = (t == 0) ? this.firstClassAtom : classification;            
            List<Atom> window = this.wm.make(t,previous,classification);            

            numerator += this.classPotentials.get(index).getValueFor(window);
        }

        return numerator + logZk;
    }

    
    
    /**
     * Calculates the log-likelihood of the output given the input and the
     * current model
     * 
     * @param input
     * @param output
     * @return
     */
    public double getLogLikelihood(List<Atom> input, List<Atom> output) {
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
        

        double numerator = 0.0d;
        for (int t = 0; t < input.size(); t++) {
            Atom previous = (t == 0) ? this.firstClassAtom : output.get(t - 1);
            Atom actual = output.get(t);
            List<Atom> window = this.wm.make(t,previous,actual);

            int index = this.getClassAtomIndex(actual);

            numerator += this.classPotentials.get(index).getValueFor(window);
        }

        return numerator + logZk;
    }
    
    
    /**
     * 
     * @param input
     * @param output
     * @return
     */
    public double getLogLikelihoodLocal(List<Atom> input, List<Atom> output) {
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
