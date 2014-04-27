/**
 * 
 */
package lcrf.logic;

import java.io.Serializable;
import java.util.List;
import java.util.Vector;

/**
 * @author bgutmann
 * 
 */
public class NumberConstant implements Term, Serializable {

    private static final long serialVersionUID = 3257567325799659319L;

    private int type;

    public int getType() {
        return type;
    }

    public void setType(int type) {
        this.type = type;
    }

    private int number;

    private int hashCode;

    private String stringrep;

    public NumberConstant(int number) {
        this.number = number;
        this.stringrep = Integer.toString(number);
        this.hashCode = stringrep.hashCode();
    }

    public String toString() {
        return stringrep;
    }

    public boolean equals(Object anObject) {
        if (this == anObject) {
            return true;
        }
        if (anObject instanceof NumberConstant) {
            return this.number == ((NumberConstant) anObject).number;
        }
        return false;
    }

    public boolean hasSubterms() {
        return false;
    }

    public boolean containsVariable(Variable v) {
        return false;
    }

    public List<Variable> getContainedVariables() {
        return new Vector<Variable>();
    }

    public NumberConstant clone() {
        return new NumberConstant(number);
    }

    public int hashCode() {
        return this.hashCode;
    }

    public boolean hasVariables() {
        return false;
    }

}
