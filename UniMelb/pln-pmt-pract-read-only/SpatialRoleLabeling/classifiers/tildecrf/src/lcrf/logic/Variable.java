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
public class Variable implements Term, Serializable {
    private static final long serialVersionUID = 3906927872328413232L;

    private int type;
    
    private int variableType;

    private String name;

    private Vector<Variable> containedVariables;

    private int hashCode;

    public Variable(String name) {
        this.name = name;
        this.hashCode = name.hashCode();
    }

    public String toString() {
        //return name + "["+type+","+variableType+"]";
        return name;
    }

    public boolean equals(Object anObject) {
        if (this == anObject) {
            return true;
        }
        if (anObject instanceof Variable) {
            return name.equals(((Variable) anObject).name);
        }
        return false;
    }

    public boolean hasSubterms() {
        return false;
    }

    public boolean containsVariable(Variable v) {
        return v.name.equals(this.name);
    }

    public List<Variable> getContainedVariables() {
        if (containedVariables == null) {
            containedVariables = new Vector<Variable>(1);
            containedVariables.add(this);
        }
        return containedVariables;
    }

    public int getType() {
        return type;
    }

    public void setType(int type) {
        this.type = type;
    }

    public Variable clone() {
        Variable result = new Variable(name);
        result.setVariableType(variableType);
        result.setType(type);
        return result;
    }

    public String getName() {
        return name;
    }

    public int hashCode() {
        return this.hashCode;
    }

    public boolean hasVariables() {
        return true;
    }

    public int getVariableType() {
        return variableType;
    }
    

    public void setVariableType(int variableType) {
        this.variableType = variableType;
    }
    

}
