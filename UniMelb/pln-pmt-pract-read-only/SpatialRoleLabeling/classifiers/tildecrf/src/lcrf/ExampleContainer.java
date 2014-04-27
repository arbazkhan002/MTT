package lcrf;

import java.util.List;

import lcrf.logic.Atom;

/**
 * This class is a container for training examples. Each training example
 * consists of a input sequence and a output sequence of the same length. The
 * sequences are implemented as Lists which contain Atoms. Further the container
 * has a list of so called class atoms. Every atom that appears somewhere in the
 * output of a example is a logically specialization of one of these class
 * atoms.
 * 
 * @see lcrf.logic.Atom
 * @author Bernd Gutmann
 */

public interface ExampleContainer {
    /**
     * @return The number of examples this container consists of.
     */
    int size();

    /**
     * @return The average length of the sequences in this container.
     */
    double averageSequenceLength();

    /**
     * @param <code>n</code> a number between <code>0</code> and
     *            <code>size()-1</code>
     * @return Returns the input sequence of the nth. training example.
     */
    List<Atom> getInputSequence(int n);

    /**
     * @param <code>n</code> a number between <code>0</code> and
     *            <code>size()-1</code>
     * @return Returns the output sequence of the nth. training example.
     */
    List<Atom> getOutputSequence(int n);

    /**
     * @return A list that contains all class atoms of the examples in this
     *         container.
     */
    List<Atom> getClassAtoms();

    /**
     * This method is used to split the examples randomly into folds of equal
     * size. With <code>folds</code> you say how many folds of the same size
     * you want. If <code>size()</code> is not dividable by <code>folds</code>
     * than the last fold <code>folds-1</code> is smaller than the the others.
     * With <code>foldnr</code> you say which fold you want. And with
     * <code>seed</code> you finally you define the seed for the random number
     * generator.
     * 
     * @param folds
     *            a number greater <code>2</code>
     * @param foldnr
     *            a number in the intervall from <code>0</code> to
     *            <code>size()-1</code>
     * @param seed
     *            a arbitrary number
     * @return a new example container that consists of all training examples of
     *         <code>fold</code>
     */
    ExampleContainer getSubfold(int folds, int foldnr, long seed);

    /**
     * This method is used to split the examples randomly into folds of equal
     * size. With <code>folds</code> you say how many folds of the same size
     * you want. If <code>size()</code> is not dividable by <code>folds</code>
     * than the last fold <code>folds-1</code> is smaller than the the others.
     * With <code>foldnr</code> you say which fold should be trown away. And
     * with <code>seed</code> you finally you define the seed for the random
     * number generator.
     * 
     * @param folds
     *            a number greater <code>2</code>
     * @param foldnr
     *            a number in the intervall from <code>0</code> to
     *            <code>size()-1</code>
     * @param seed
     *            a arbitrary number
     * @return a new example container that consists of all training examples
     *         except those in fold <code>fold</code>
     */
    ExampleContainer getSubfoldInverse(int folds, int foldnr, long seed);
}
