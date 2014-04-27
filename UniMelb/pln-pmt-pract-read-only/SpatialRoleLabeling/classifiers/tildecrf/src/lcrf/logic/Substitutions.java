package lcrf.logic;

import java.util.Vector;

/**
 * @author Bernd Gutmann
 */
public class Substitutions implements Cloneable {
    Vector<Substitution> rules;

    private boolean cloneMarker;
        

    public Substitutions() {
        this(new Vector<Substitution>(5));
    }

    public Substitutions(Vector<Substitution> rules) {
        cloneMarker = false;
        this.rules = rules;
    }

    public void add(Substitution rule) {
        if (cloneMarker) {
            //this instance is cloned, or has a cloned partner
            //therefor we must make a new rules vector
            //to prevent side effects
            Vector<Substitution> rules2 = new Vector<Substitution>(this.rules.size() + 1);
            for (int i = 0; i < rules.size(); i++) {
                rules2.add(rules.get(i));
            }
            this.rules = rules2;
            cloneMarker = false;
        }
        rules.add(rule);
    }

    public void addAndApplyToOldRules(Substitution rule) {
        if (cloneMarker) {
            Vector<Substitution> rules2 = new Vector<Substitution>(this.rules.size() + 1);
            for (int i = 0; i < rules.size(); i++) {
                rules2.add(rules.get(i));
            }
            this.rules = rules2;
            cloneMarker = false;
        }
        for (int i = 0; i < this.rules.size(); i++) {
            Substitution oldRule = rules.elementAt(i);
            oldRule.body = rule.apply(oldRule.body);
        }
        rules.add(rule);

    }

    public Term apply(Term t) {
        if (!t.hasVariables()) {
            return t;
        }

        Term tmpTerm = t;
        for (int i = 0; i < this.rules.size(); i++) {
            tmpTerm = rules.elementAt(i).apply(tmpTerm);
        }

        return tmpTerm;
    }

    public Term getSubstitutionFor(Variable v) {
        for (Substitution s : rules) {
            if (s.head.equals(v)) {
                return s.body;
            }
        }

        return v;
    }

    public String toString() {
        return this.rules.toString();
    }

    public int hashCode() {
        return rules.hashCode();
    }

    public boolean equals(Object anObject) {
        if (this == anObject) {
            return true;
        }

        if (anObject instanceof Substitutions) {
            return ((Substitutions) anObject).rules.equals(rules);
        }

        return false;
    }
    
    public int size() {
        return rules.size();
    }

    /**
     * 
     * deep copy
     * 
     * @return
     */
    public Substitutions clone() {
        Substitutions pseudoClonedInstance = new Substitutions(rules);
        pseudoClonedInstance.cloneMarker = true;
        cloneMarker = true;

        return pseudoClonedInstance;
    }
    
    
    public Substitutions realclone() {
        Substitutions clonedInstance = new Substitutions();
        
        for (Substitution s  : rules) {
            clonedInstance.add(s);
        }
        
        
        return clonedInstance;
    }

}
