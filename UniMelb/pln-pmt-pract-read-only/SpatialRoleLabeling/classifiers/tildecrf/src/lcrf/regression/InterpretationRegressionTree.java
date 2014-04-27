package lcrf.regression;

import java.io.Serializable;
import java.text.DecimalFormat;

import lcrf.logic.Atom;
import lcrf.logic.Interpretation;
import lcrf.logic.Substitutions;
import lcrf.logic.Term;

import org.apache.log4j.Logger;

/**
 * @author Bernd Gutmann
 */
public class InterpretationRegressionTree implements RegressionModel<Interpretation>, Serializable {
    private static final long serialVersionUID = 3906926781389943604L;

    private double value;

    private Atom test;

    private InterpretationRegressionTree trueSubTree;

    private InterpretationRegressionTree falseSubTree;

    private int treeHeight;

    public InterpretationRegressionTree(Atom test) {
        this.test = test;
        this.trueSubTree = null;
        this.falseSubTree = null;
        this.treeHeight = -1;
    }

    public void setTrueSubTree(InterpretationRegressionTree trueSubTree) {
        if (this.trueSubTree != null)
            throw new IllegalStateException();

        this.trueSubTree = trueSubTree;
    }

    public void setFalseSubTree(InterpretationRegressionTree falseSubTree) {
        if (this.falseSubTree != null)
            throw new IllegalStateException();

        this.falseSubTree = falseSubTree;
    }

    public void verifyTree() {
        if (this.test == null) {
            if (this.trueSubTree != null)
                throw new IllegalStateException();
            if (this.falseSubTree != null)
                throw new IllegalStateException();
            this.treeHeight = 0;
        } else {
            if (this.trueSubTree == null)
                throw new IllegalStateException();
            if (this.falseSubTree == null)
                throw new IllegalStateException();
            trueSubTree.verifyTree();
            falseSubTree.verifyTree();
            this.treeHeight = 1 + Math.max(trueSubTree.treeHeight, falseSubTree.treeHeight);
        }
    }

    public InterpretationRegressionTree(double value, Atom test, InterpretationRegressionTree trueSubTree,
            InterpretationRegressionTree falseSubTree) {
        assert ((test == null) && (trueSubTree == null) && (falseSubTree == null) || (test != null)
                && (trueSubTree != null) && (falseSubTree != null));

        this.value = value;
        this.test = test;
        this.trueSubTree = trueSubTree;
        this.falseSubTree = falseSubTree;

        this.treeHeight = (test == null) ? 0 : 1 + Math.max(trueSubTree.treeHeight, falseSubTree.treeHeight);
    }

    public double getValueFor(Interpretation inter) {
        if (inter == null) {
            throw new IllegalArgumentException();
        }

        return getValueForIntern(inter, new Substitutions());
    }

    private double getValueForIntern(Interpretation inter, Substitutions substs) {
        if (this.test == null) {
            return this.value;
        }
        Term testSubstituted = substs.apply(test.getTermRepresentation());

        Substitutions substs2 = inter.contains(testSubstituted, substs);
        if (substs2 != null) {
            return trueSubTree.getValueForIntern(inter, substs2);
        }
        return falseSubTree.getValueForIntern(inter, substs);

    }

    public InterpretationRegressionTree doPrunning(double a) {
        if (test == null)
            return new InterpretationRegressionTree(value, null, null, null);

        InterpretationRegressionTree trueTmp = trueSubTree.doPrunning(a);
        InterpretationRegressionTree falseTmp = falseSubTree.doPrunning(a);

        if (trueTmp.test == null && falseTmp.test == null) {
            if (Math.abs(falseSubTree.value - trueSubTree.value) < a) {
                return new InterpretationRegressionTree((trueTmp.value + falseTmp.value) / 2.0, null, null,
                        null);
            }
        }

        return new InterpretationRegressionTree(value, test, trueTmp, falseTmp);

    }

    public String toDotString() {
        return "digraph g{\n" + toDotStringIntern("I") + "\n}";
    }

    private String toDotStringIntern(String namePrefix) {
        if (this.test == null) {
            DecimalFormat d = new DecimalFormat();
            d.setMaximumFractionDigits(8);
            d.setMinimumFractionDigits(0);
            return namePrefix + "[shape = box,label = \"" + d.format(value) + "\"];\n";
        }

        String result = namePrefix + "[label = \"" + this.test + "\"];\n";
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
        if (anObject instanceof InterpretationRegressionTree) {
            InterpretationRegressionTree lrt2 = (InterpretationRegressionTree) anObject;
            return ((test == null) ? (lrt2.test == null && value == lrt2.value) : test.equals(lrt2.test))
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
        return (test == null) ? 1 : 2 + falseSubTree.getParameterCount() + trueSubTree.getParameterCount();
    }

}
