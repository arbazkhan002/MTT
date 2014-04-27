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
public class Constant implements Term, Serializable {
    private static final long serialVersionUID = 3258135738884175158L;

    private int type;

    public int getType() {
        return type;
    }

    public void setType(int type) {
        this.type = type;
    }

    private String name;

    private List<Term> subterms;

    private List<Variable> containedVariables;

    private int hashCode;

    private String stringrep;

    public Constant(String name, List<Term> subterms) {
        assert name != null;
        assert subterms != null;

        this.name = name;
        this.subterms = subterms;
        this.containedVariables = new Vector<Variable>();

        this.stringrep = this.name;
        if (this.subterms.size() > 0) {
            this.stringrep += "(";
            for (Term t : subterms) {
                this.stringrep += t.toString() + ",";
            }
            this.stringrep = this.stringrep.substring(0, this.stringrep.length() - 1) + ")";
        }

        this.hashCode = this.stringrep.hashCode();

        for (Term subterm : subterms) {            
            if (subterm instanceof Variable) {
                containedVariables.add((Variable) subterm);
            } else if (subterm.hasSubterms()) {
                containedVariables.addAll(subterm.getContainedVariables());
            }
        }
    }

    public Constant(String name) {
        assert name != null;
        this.name = name;
        this.subterms = new Vector<Term>();
        this.containedVariables = new Vector<Variable>(0);

        this.stringrep = this.name;
        if (this.subterms.size() > 0) {
            this.stringrep += "(";
            for (Term t : subterms) {
                this.stringrep += t.toString() + ",";
            }
            this.stringrep = this.stringrep.substring(0, this.stringrep.length() - 1) + ")";
        }

        this.hashCode = this.stringrep.hashCode();
    }

    public String getName() {
        return this.name;
    }

    public List<Term> getSubterms() {
        return subterms;
    }

    public String toString() {
        return this.stringrep;
    }

    public boolean equals(Object anObject) {
        if (this == anObject) {
            return true;
        }
        
        return (anObject instanceof Constant) &&
                stringrep.equals(((Constant) anObject).stringrep);
    }

    public boolean hasSubterms() {
        return this.subterms.size() > 0;
    }

    public boolean containsVariable(Variable v) {
        return containedVariables.contains(v);
    }

    public List<Variable> getContainedVariables() {
        return containedVariables;
    }

    public Constant clone() {
        Vector<Term> clonedSubterms = new Vector<Term>(subterms.size());
        for (Term subterm : subterms) {
            clonedSubterms.add(subterm.clone());
        }

        return new Constant(name, clonedSubterms);
    }

    public int hashCode() {
        return this.hashCode;
    }

    public boolean hasVariables() {
        return containedVariables.size() > 0;
    }

}
