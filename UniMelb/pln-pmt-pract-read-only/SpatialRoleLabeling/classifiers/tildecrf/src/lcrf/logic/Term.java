/*
 * Created on 23.03.2005
 *
 */
package lcrf.logic;

import java.util.List;

/**
 * @author bernd
 * 
 */
public interface Term {
    public boolean hasSubterms();

    public boolean containsVariable(Variable v);

    public List<Variable> getContainedVariables();

    public boolean hasVariables();

    public Term clone();

    /**
     * used by SchemaUnificationGenerator
     * 
     * @return
     */
    public int getType();

    /**
     * dito
     * 
     * @return
     */
    public void setType(int type);
}
