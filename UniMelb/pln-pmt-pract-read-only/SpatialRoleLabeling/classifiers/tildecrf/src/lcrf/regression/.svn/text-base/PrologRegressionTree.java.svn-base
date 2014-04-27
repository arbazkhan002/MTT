package lcrf.regression;

import java.io.Serializable;
import java.text.DecimalFormat;
import java.util.List;

import lcrf.logic.Atom;
import xprolog.Engine;
import xprolog.ParseException;

/**
 * @author Bernd Gutmann
 */

// FIXME this class is not implemented completely yet
public class PrologRegressionTree implements RegressionModel<List<Atom>>, Serializable {
    private static final long serialVersionUID = 3906926781389943604L;

    private double value;

    private String test;

    private PrologRegressionTree trueSubTree;

    private PrologRegressionTree falseSubTree;

    private int treeHeight;

    private Engine prologEngine;

    // FIXME delete me!
    public int dirty_ExampleSize = 0;

    public PrologRegressionTree(double value, String test, PrologRegressionTree trueSubTree,
            PrologRegressionTree falseSubTree, Engine prologEngine) {
        assert ((test == null) && (trueSubTree == null) && (falseSubTree == null) || (test != null)
                && (trueSubTree != null) && (falseSubTree != null));
        assert test == null || prologEngine != null;

        this.value = value;
        this.test = test;
        this.trueSubTree = trueSubTree;
        this.falseSubTree = falseSubTree;

        this.treeHeight = (test == null) ? 0 : 1 + Math.max(trueSubTree.treeHeight, falseSubTree.treeHeight);

        this.prologEngine = prologEngine;
    }

    public double getValueFor(List<Atom> window) {
        assert window != null;

        if (test == null) {
            return value;
        }

        // transform the content into prolog notation
        String prologTerm = ",[";
        boolean notfirst = false;
        for (Atom atom : window) {
            if (notfirst) {
                prologTerm = prologTerm.concat(",");
            }
            notfirst = true;
            prologTerm = prologTerm.concat(atom.toString());
        }
        prologTerm = prologTerm.concat("])");

        return getValueForIntern(prologTerm, "");
    }

    private double getValueForIntern(String example, String testsSoFar) {
        if (test == null) {
            return value;
        }

        String query = "listsucceds([".concat(testsSoFar).concat("],").concat(test).concat(example);

        String newTests = (testsSoFar.equals("")) ? "" : testsSoFar.concat(",");

        try {
            if (prologEngine.setQuery(query)) {
                return trueSubTree.getValueForIntern(example, newTests.concat(test));
            } else {
                return falseSubTree.getValueForIntern(example, newTests.concat("not(").concat(test).concat(
                        ")"));
            }
        } catch (ParseException e) {
            throw new RuntimeException(e);
        }
    }

    /*
     * public PrologRegressionTree doPrunning(double a) { if (job == null)
     * return new PrologRegressionTree(value, null,null,null);
     * PrologRegressionTree trueTmp = trueSubTree.doPrunning(a);
     * PrologRegressionTree falseTmp = falseSubTree.doPrunning(a); if
     * (trueTmp.job == null && falseTmp.job == null) { if
     * (Math.abs(falseSubTree.value-trueSubTree.value)<a) { return new
     * PrologRegressionTree((trueTmp.value + falseTmp.value)/2.0,
     * null,null,null); } } return new PrologRegressionTree(value, job,trueTmp,
     * falseTmp); }
     */

    public String toDotString() {
        return "digraph g{\n" + toDotStringIntern("I") + "\n}";
    }

    private String toDotStringIntern(String namePrefix) {
        if (this.test == null) {
            DecimalFormat d = new DecimalFormat();
            d.setMaximumFractionDigits(8);
            d.setMinimumFractionDigits(0);
            return namePrefix + "[shape = box,label = \"" + dirty_ExampleSize + " : " + d.format(value)
                    + "\"];\n";
        }

        String result = namePrefix + "[label = \"" + dirty_ExampleSize + " : " + this.test + "\"];\n";
        result += namePrefix + " -> " + namePrefix + "T" + " [label=\"True\"];\n";
        result += namePrefix + " -> " + namePrefix + "F" + " [label=\"False\"];\n";
        result += trueSubTree.toDotStringIntern(namePrefix + "T");
        result += falseSubTree.toDotStringIntern(namePrefix + "F");

        return result;
    }

    public String toString() {
        if (this.test == null) {
            return "{" + this.value + "}";
        }

        return " { " + this.test + " : " + this.trueSubTree + ";  \\+" + this.test + " : "
                + this.falseSubTree + " } ";
    }

    public int hashCode() {
        if (this.test == null) {
            return (int) (this.value * 36612.3);
        }

        return test.hashCode() * ((trueSubTree.hashCode() * 8) ^ falseSubTree.hashCode());
    }

    public boolean equals(Object anObject) {
        if (this == anObject) {
            return true;
        }
        if (anObject instanceof PrologRegressionTree) {
            PrologRegressionTree lrt2 = (PrologRegressionTree) anObject;
            return ((test == null) ? (lrt2.test == null && value == lrt2.value) : (test.equals(lrt2.test)))
                    && ((trueSubTree == null) ? lrt2.trueSubTree == null : trueSubTree
                            .equals(lrt2.trueSubTree))
                    && ((falseSubTree == null) ? lrt2.falseSubTree == null : falseSubTree
                            .equals(lrt2.falseSubTree));
        }
        return false;
    }

    /**
     * Counts the number of parameters this regression tree has : every inner
     * node counts twice (atom + decision position) and every leaf counts one
     * (the value).
     * 
     * @return the number of parameters that this regression model has
     */
    public int getParameterCount() {
        return (test == null) ? 1 : 1 + falseSubTree.getParameterCount() + trueSubTree.getParameterCount();
    }

}
