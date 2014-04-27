package lcrf.regression;

import java.io.Serializable;
import java.text.DecimalFormat;
import java.util.List;

import lcrf.logic.Atom;
import lcrf.logic.Substitutions;
import lcrf.logic.UnificationJob;
import lcrf.logic.Unificator;

/**
 * @author Bernd Gutmann
 */
public class LogicalRegressionTree implements RegressionModel<List<Atom>>, Serializable {
    private static final long serialVersionUID = 3906926781389943604L;

    private double value;

    private UnificationJob job;

    private LogicalRegressionTree trueSubTree;

    private LogicalRegressionTree falseSubTree;

    private int treeHeight;

    public LogicalRegressionTree(double value, UnificationJob job, LogicalRegressionTree trueSubTree,
            LogicalRegressionTree falseSubTree) {
        assert ((job == null) && (trueSubTree == null) && (falseSubTree == null) || (job != null)
                && (trueSubTree != null) && (falseSubTree != null));

        this.value = value;
        this.job = job;
        this.trueSubTree = trueSubTree;
        this.falseSubTree = falseSubTree;

        this.treeHeight = (job == null) ? 0 : 1 + Math.max(trueSubTree.treeHeight, falseSubTree.treeHeight);
    }

    public double getValueFor(List<Atom> window) {
        if (window == null) {
            throw new IllegalArgumentException();
        }

        return getValueForIntern(window, new Substitutions());
    }

    private double getValueForIntern(List<Atom> window, Substitutions substs) {
        if (this.job == null) {
            return this.value;
        }

        Substitutions substs2 = Unificator.findMGU(window, job, substs.clone());
        if (substs2 != null) {
            return trueSubTree.getValueForIntern(window, substs2);
        }

        return falseSubTree.getValueForIntern(window, substs);
    }

    public LogicalRegressionTree doPrunning(double a) {
        if (job == null)
            return new LogicalRegressionTree(value, null, null, null);

        LogicalRegressionTree trueTmp = trueSubTree.doPrunning(a);
        LogicalRegressionTree falseTmp = falseSubTree.doPrunning(a);

        if (trueTmp.job == null && falseTmp.job == null) {
            if (Math.abs(falseSubTree.value - trueSubTree.value) < a) {
                return new LogicalRegressionTree((trueTmp.value + falseTmp.value) / 2.0, null, null, null);
            }
        }

        return new LogicalRegressionTree(value, job, trueTmp, falseTmp);

    }

    public String toDotString() {
        return "digraph g{\n" + toDotStringIntern("I") + "\n}";
    }

    private String toDotStringIntern(String namePrefix) {
        if (this.job == null) {
            DecimalFormat d = new DecimalFormat();
            d.setMaximumFractionDigits(8);
            d.setMinimumFractionDigits(0);
            return namePrefix + "[shape = box,label = \"" + d.format(value) + "\"];\n";
        }

        String result = namePrefix + "[label = \"" + this.job + "\"];\n";
        result += namePrefix + " -> " + namePrefix + "T" + " [label=\"True\"];\n";
        result += namePrefix + " -> " + namePrefix + "F" + " [label=\"False\"];\n";
        result += trueSubTree.toDotStringIntern(namePrefix + "T");
        result += falseSubTree.toDotStringIntern(namePrefix + "F");

        return result;
    }

    public String toString() {
        if (this.job == null) {
            return "{" + this.value + "}";
        }

        return " { " + this.job + " : " + this.trueSubTree + ";  \\+" + this.job + " : " + this.falseSubTree
                + " } ";
    }

    public int hashCode() {
        if (this.job == null) {
            return (int) (this.value * 36612.3);
        }

        return job.hashCode() * ((trueSubTree.hashCode() * 8) ^ falseSubTree.hashCode());
    }

    public boolean equals(Object anObject) {
        if (this == anObject) {
            return true;
        }
        if (anObject instanceof LogicalRegressionTree) {
            LogicalRegressionTree lrt2 = (LogicalRegressionTree) anObject;
            return ((job == null) ? (lrt2.job == null && value == lrt2.value) : job.equals(lrt2.job))
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
        return (job == null) ? 1 : 2 + falseSubTree.getParameterCount() + trueSubTree.getParameterCount();
    }

}
