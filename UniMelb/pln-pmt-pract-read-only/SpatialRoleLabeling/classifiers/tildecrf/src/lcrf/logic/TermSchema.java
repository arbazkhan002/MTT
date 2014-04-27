/**
 * 
 */
package lcrf.logic;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Vector;

import org.apache.log4j.Logger;


/**
 * @author bgutmann
 * 
 */
public class TermSchema implements Iterator<Term>, Serializable {
    private static final long serialVersionUID = 3258408430669936432L;

    private int schemaType;

    public static final String UNBOUNDEDVAR = "__UNBOUNDEDVAR";

    public static final String BOUNDEDVAR = "__BOUNDEDVAR";

    private Term t;

    private List<Variable> freeVariables;

    private HashMap<Variable, List<Term>> hInitial;

    private HashMap<Variable, List<Term>> hActual;

    private int[] currentTermIndex;

    private int[] maxTermIndex;

    private Term nextTerm;

    /**
     * represents the constant term
     * only valid for terms without variables.
     * 
     * @param t
     */
    public TermSchema(Term t, int schemaType) {
        this(t, new HashMap<Variable, List<Term>>(), schemaType);
    }

    public TermSchema(Term t, HashMap<Variable, List<Term>> h, int schemaType) {
        if (h==null || t==null)
            throw new IllegalArgumentException(t + ", " + h);

        this.schemaType = schemaType;
        this.t = t;
        this.hInitial = h;
        freeVariables = t.getContainedVariables();
        
        Logger.getLogger(getClass()).debug(freeVariables);

        currentTermIndex = new int[freeVariables.size()];
        maxTermIndex = new int[freeVariables.size()];
        for (int i = 0; i < freeVariables.size(); i++) {
            assert h.containsKey(freeVariables.get(i));
            assert h.get(freeVariables.get(i)) != null;
            assert h.get(freeVariables.get(i)).size() > 0;
        }

        iterator(new Vector<Variable>(0), 0);
        setNextTerm();
    }

    public int getSchemaType() {
        return schemaType;
    }

    private void setNextTerm() {
        Substitutions substs = new Substitutions();
        for (int i = 0; i < freeVariables.size(); i++) {
            Variable head = freeVariables.get(i);
            Term body = hActual.get(head).get(currentTermIndex[i]);            
            substs.add(new Substitution(head, body));
        }
        nextTerm = substs.apply(t);
        nextTerm.setType(schemaType);
    }

    /**
     * 
     * @return <tt>true</tt> when overflow has happened
     */
    private boolean switchToNextSubstitution() {
        if (this.currentTermIndex.length == 0) {
            return true; // only one state: {}
        }

        currentTermIndex[0]++;
        int index = 0;
        while (index < this.currentTermIndex.length && currentTermIndex[index] >= maxTermIndex[index]) {
            currentTermIndex[index] = 0;
            index++;
            if (index < this.currentTermIndex.length) {
                currentTermIndex[index]++;
            }
        }

        return index == currentTermIndex.length;
    }

 

    public boolean hasNext() {
        return nextTerm != null;
    }

    public Term next() {
        Term result = nextTerm;
        if (result == null) {
            throw new NoSuchElementException();
        }

        if (this.switchToNextSubstitution() == false) {
            setNextTerm();
        } else {
            nextTerm = null;
        }

        return result;
    }

    public void remove() {
        throw new UnsupportedOperationException();
    }

    public Iterator<Term> iterator(List<Variable> boundedVariables, int actualDepth) {
        assert boundedVariables != null;
        
        
        // process bounded/unboundedVars
        hActual = new HashMap<Variable, List<Term>>(this.freeVariables.size());
        Vector<Variable> boundedVarsInThisTerm = new Vector<Variable>();
        for (Variable var : freeVariables) {
            //Logger.getLogger(getClass()).warn(var+ " fuuuuuuuuck "+var.getVariableType());
            List<Term> entriesInitial = hInitial.get(var);
            List<Term> entriesActual = new Vector<Term>(entriesInitial.size() + boundedVariables.size());
                       

            for (Term entry : entriesInitial) {
                if (!(entry instanceof Variable)) {
                    entriesActual.add(entry);
                } else {
                    Variable v = (Variable) entry;
                    

                    if (v.getName().startsWith(TermSchema.BOUNDEDVAR)) {
                /*        String restname = v.getName().substring(TermSchema.BOUNDEDVAR.length());

                        if (restname.length() > 0) {
                            try {
                                Logger.getLogger(this.getClass()).info("actualDepth = " + actualDepth);
                                Logger.getLogger(this.getClass()).info("restname    = " + restname);                                
                                int number = Integer.parseInt(restname);
                                Logger.getLogger(this.getClass()).info("number      = " + number);
                                if (actualDepth >= number) {
                                    Logger.getLogger(this.getClass()).info("added boundedVars");
                                    entriesActual.addAll(boundedVariables);
                                }
                            } catch (NumberFormatException e) {
                                e.printStackTrace();
                                throw new RuntimeException(e.getMessage());
                            }
                        } else {
                            Logger.getLogger(this.getClass()).info("added boundedVars without test");*/
                        /*for (Variable boundedVariable : boundedVariables) {
                            //Logger.getLogger(getClass()).info(boundedVariable.getVariableType() + " " + var.getVariableType());
                            if (boundedVariable.getVariableType() == var.getVariableType())
                                entriesActual.add(boundedVariable);
                        }*/
                            entriesActual.addAll(boundedVariables);
                        //}
                    } else if (v.getName().startsWith(TermSchema.UNBOUNDEDVAR)) {
                        //Logger.getLogger(getClass()).debug(t+" "+ var +" unbounded variable before added "+v+" "+var.getVariableType());
                        int counter = 0;
                        Variable vAdd;
                        do {
                            vAdd = new Variable("__" + Integer.toString(counter));
                            counter++;
                            //FIXME double used bounded Vars! (evt. types??)
                        } while (boundedVariables.contains(vAdd) || boundedVarsInThisTerm.contains(vAdd));
                        
                        boundedVarsInThisTerm.add(vAdd);
                        
                        //todo make it better with user settable types
                        
                        //vAdd.setVariableType(var.getVariableType());
                        //Logger.getLogger(getClass()).debug(t+" " +var +" unbounded variable added "+vAdd+" "+vAdd.getVariableType());
                        entriesActual.add(vAdd);
                    } else {
                        entriesActual.add(v);
                    }
                }
            }

            hActual.put(var, entriesActual);
        }

        // reset to initial state
        for (int i = 0; i < currentTermIndex.length; i++) {
            currentTermIndex[i] = 0;
            maxTermIndex[i] = hActual.get(freeVariables.get(i)).size();
        }

        setNextTerm();
        return this;
    }

    public String toString() {
        return "( " + this.t + " :: " + hInitial + " )";
    }

}
