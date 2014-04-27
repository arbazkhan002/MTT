/**
 * 
 */
package lcrf.regression;

import java.util.List;
import java.util.Vector;

import lcrf.logic.Atom;
import lcrf.logic.Variable;

/**
 * @author Bernd Gutmann
 */

public class ExploreJob<T> {
    // the average value of the covered regression examples
    private double average;

    // the variables that are contained in the testsSoFar
    private Vector<Variable> boundedVars;

    // the depth of the node to explore, the root has depth 0
    private int depth;

    // the covered regression examples
    private List<RegressionExample<T>> examples;

    // if null this node shall become the root node
    private InterpretationRegressionTree father;

    // the tests that were made on the path comming to this node
    private Vector<Atom> testsSoFar;

    // if true, this node becomses the true child
    // else it becomes the fals child
    private boolean trueChild;

    public ExploreJob(List<RegressionExample<T>> examples, double average,
            InterpretationRegressionTree father, boolean trueChild, int depth, Vector<Variable> boundedVars,
            Vector<Atom> testsSoFar) {
        assert examples != null;        
        assert depth >=0;
        assert boundedVars != null;
        assert testsSoFar != null;        
        
        this.examples = examples;
        this.average = average;
        this.father = father;
        this.trueChild = trueChild;
        this.depth = depth;

        this.boundedVars = boundedVars;
        this.testsSoFar = testsSoFar;
    }

    /**
     * should be called after this job was done. all references will be nulled
     * to prevent a memory leak
     */
    public void clear() {
        examples.clear();
        examples = null;
        father = null;
        boundedVars = null;
        testsSoFar = null;
    }

    public double getAverage() {
        return average;
    }

    public Vector<Variable> getBoundedVars() {
        return boundedVars;
    }

    public int getDepth() {
        return depth;
    }

    public List<RegressionExample<T>> getExamples() {
        return examples;
    }

    public InterpretationRegressionTree getFather() {
        return father;
    }

    public Vector<Atom> getTestsSoFar() {
        return testsSoFar;
    }

    public boolean isTrueChild() {
        return trueChild;
    }

    public String toString() {
        return "(" + examples.size() + "," + average + "," + trueChild + "," + depth + ")";
    }

}
