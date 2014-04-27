/**
 * 
 */
package lcrf.logic;

import java.util.Vector;

/**
 * @author Bernd Gutmann
 *
 */
public class Interpretation {
    private Interpretation fatherInterpretation;
    
    private Vector<Atom> atoms;
    
    public Interpretation() {
        atoms = new Vector<Atom>();
    }
    
    public Interpretation(int size) {
        atoms = new Vector<Atom>(size);
    }
        
    public Interpretation(Interpretation father) {
        fatherInterpretation = father;
        atoms = new Vector<Atom>();
    }        
    
    public void add(Atom a) {
        assert a!=null;
        assert a.getTermRepresentation() instanceof Constant;
        assert a.getTermRepresentation().hasVariables() == false;
        
        int pos=0;
        
        while (pos<atoms.size() &&
               atoms.get(pos).getTermRepresentation().toString().compareTo(a.getTermRepresentation().toString())<0) {
            pos++;
        }
                                        
        atoms.add(pos,a);
    }
    
    public Substitutions contains(Term t, Substitutions substs) {
        assert t!=null;  
        
        if (fatherInterpretation != null) {
            Substitutions result = fatherInterpretation.contains(t, substs);
            if (result != null) {
                return result;
            }
        }
                
        
        if (t.hasVariables() == false) {
            String query = t.toString();
            
            for (Atom aintern:atoms) {
                String internStr = aintern.toString();
                
                int cmp = internStr.compareTo(query);
                
                if (cmp == 0) {
                    return new Substitutions();
                }
                
                if (cmp > 0) {
                    return null;
                }                        
            } 
            return null;
        }
        
        for (Atom aintern:atoms) {
            Substitutions mgu = Unificator.findMGU(aintern.getTermRepresentation(),t,substs.clone());
            
            if (mgu != null)
                return mgu;
        }
        
        return null;
    }
    
    public Atom get(int i) {
        if (i<atoms.size()) {
            return atoms.get(i);
        }
        
        if (fatherInterpretation != null) {
            return fatherInterpretation.get(i-atoms.size());
        }
        
        throw new IndexOutOfBoundsException(Integer.toString(i));
    }
    
    public int size() {
        if (fatherInterpretation == null) {
            return atoms.size();
        }
        
        return atoms.size()+fatherInterpretation.size();
    }
    
    
    public Interpretation clone() {
        if (fatherInterpretation != null) 
            throw new IllegalStateException();
        Interpretation myClone = new Interpretation();
        myClone.atoms = (Vector<Atom>) atoms.clone();
        
        return myClone;
    }
        
    public String toString() {
        if (fatherInterpretation == null)
            return atoms.toString();
        
            return "("+fatherInterpretation+" , "+
            atoms.toString()+")";
    }
    
    public int hashCode() {               
        if (fatherInterpretation != null) {
            return atoms.hashCode() * 2 ^ fatherInterpretation.hashCode();
        }
        
        return atoms.hashCode();
    }
    

}
