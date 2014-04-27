package lcrf.counting;

import java.io.Serializable;
import java.util.List;

import lcrf.logic.Atom;
import lcrf.logic.Substitutions;
import lcrf.logic.UnificationJob;
import lcrf.logic.Unificator;
import lcrf.stuff.ArrayStuff;

/**
 * 
 * 
 * @author Bernd Gutmann
 */
public class LogicalCountingTree implements Serializable {
    /**
     * 
     */
    private static final long serialVersionUID = 3617296722641237559L;

    private int[] countArray;

    private UnificationJob job;

    private LogicalCountingTree trueSubTree;

    private LogicalCountingTree falseSubTree;

    private int treeHeight;

    public LogicalCountingTree(int[] countArray, UnificationJob job, LogicalCountingTree trueSubTree,
            LogicalCountingTree falseSubTree) {
        assert ((job == null) && (trueSubTree == null) && (falseSubTree == null) && (countArray != null)
                && (countArray.length > 0) || (job != null) && (trueSubTree != null)
                && (falseSubTree != null) && (countArray == null));

        this.countArray = countArray;
        this.job = job;
        this.trueSubTree = trueSubTree;
        this.falseSubTree = falseSubTree;

        this.treeHeight = (job == null) ? 0 : 1 + Math.max(trueSubTree.treeHeight, falseSubTree.treeHeight);
    }

    public int[] getCountArrayFor(List<Atom> window) {
        if (window == null) {
            throw new IllegalArgumentException();
        }

        return getCountArrayForIntern(window, new Substitutions());
    }

    private int[] getCountArrayForIntern(List<Atom> window, Substitutions substs) {
        if (this.job == null) {
            return countArray;
        }

        Substitutions substs2 = Unificator.findMGU(window, job, substs.clone());
        if (substs2 != null) {
            return trueSubTree.getCountArrayForIntern(window, substs2);
        }

        return falseSubTree.getCountArrayForIntern(window, substs);
    }

    public String toDotString() {
        return "digraph g{\n" + toDotStringIntern("I") + "\n}";
    }

    private String toDotStringIntern(String namePrefix) {
        if (this.job == null) {
            String label = "";
            int sum = 0;
            for (int i = 0; i < countArray.length; i++) {
                label += i + " : " + countArray[i] + "\\n";
                sum += countArray[i];
            }
            label += "Sum = " + sum;
            return namePrefix + "[shape = box,label = \"" + label + "\"];\n";
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
            return "{" + ArrayStuff.toString(countArray) + "}";
        }

        return " { " + this.job + " : " + this.trueSubTree + ";  \\+" + this.job + " : " + this.falseSubTree
                + " } ";
    }

    public boolean equals(Object anObject) {
        if (this == anObject) {
            return true;
        }
        if (anObject instanceof LogicalCountingTree) {
            LogicalCountingTree lrt2 = (LogicalCountingTree) anObject;
            return ((job == null) ? lrt2.job == null : job.equals(lrt2.job))
                    && ((trueSubTree == null) ? lrt2.trueSubTree == null : trueSubTree
                            .equals(lrt2.trueSubTree))
                    && ((falseSubTree == null) ? lrt2.falseSubTree == null : falseSubTree
                            .equals(lrt2.falseSubTree))
                    && ArrayStuff.arrayEquals(countArray, lrt2.countArray);
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
