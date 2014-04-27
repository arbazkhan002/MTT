/**
 * 
 */
package lcrf.logic;

import java.io.Serializable;
import java.util.List;
import java.util.Vector;

/**
 * @author Bernd Gutmann
 * 
 */
public class StringConstant implements Term, Serializable {
    private static final long serialVersionUID = 3258411737761134385L;

    private int type;

    public int getType() {
        return type;
    }

    public void setType(int type) {
        this.type = type;
    }

    private String content;

    private int hashCode;

    private String stringrep;

    public StringConstant(String content) {
        this.content = content;
        this.stringrep = '\'' + content + '\'';
        this.hashCode = this.stringrep.hashCode();
    }

    public String toString() {
        return this.stringrep;
    }

    public boolean equals(Object anObject) {
        if (this == anObject) {
            return true;
        }
        if (anObject instanceof StringConstant) {
            return this.content.equals(((StringConstant) anObject).content);
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
        return new Vector<Variable>(0);
    }

    public StringConstant clone() {
        return new StringConstant(content);
    }

    public int hashCode() {
        return this.hashCode;
    }

    public boolean hasVariables() {
        return false;
    }

}
