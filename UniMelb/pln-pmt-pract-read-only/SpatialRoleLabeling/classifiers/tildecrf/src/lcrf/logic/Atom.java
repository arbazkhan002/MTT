/*
 * Created on 03.03.2005
 *
 */
package lcrf.logic;

import java.io.Serializable;
import java.io.StringReader;

import lcrf.logic.parser.AtomParser;
import lcrf.logic.parser.ParseException;

/**
 * @author Bernd Gutmann
 * 
 */
public class Atom implements Serializable {
    private static final long serialVersionUID = 3256445815315510578L;

    private String name;

    private Term t;

    private int h;
    
    private String firstPredicate;

    public Atom(String name) throws ParseException {
        assert name != null;

        this.name = name;
        this.t = new AtomParser(new StringReader(name)).Term();
        this.h = t.hashCode();
        
        if (t instanceof Constant) {
            firstPredicate = ((Constant) t).getName();
        } else {
            firstPredicate = null;
        }
    }

    public Atom(Term t) {
        assert t != null;
        this.name = t.toString();
        this.t = t;
        this.h = t.hashCode();
        
        if (t instanceof Constant) {
            firstPredicate = ((Constant) t).getName();
        } else {
            firstPredicate = null;
        }
    }

    public Term getTermRepresentation() {
        return t;
    }

    public boolean isMoreGeneralThan(Atom anAtom) {
        return Unificator.findSpecialisation(t, anAtom.t, new Substitutions()) != null;
    }

    public boolean equals(Object anObject) {
        if (this == anObject) {
            return true;
        }

        if (anObject instanceof Atom) {
            return t.equals(((Atom) anObject).t);
        }
        return false;
    }

    public String toString() {
        return this.name;
    }

    public int hashCode() {
        return h;
    }

    public String getFirstPredicate() {
        return firstPredicate;
    }
    

}
