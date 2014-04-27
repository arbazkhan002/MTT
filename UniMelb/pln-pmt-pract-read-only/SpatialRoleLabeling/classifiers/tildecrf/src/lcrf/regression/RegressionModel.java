/**
 * 
 */
package lcrf.regression;

/**
 * @author Bernd Gutmann
 * 
 */
public interface RegressionModel<T> {
    /**
     * Returns the numerical value for the example.
     * 
     * @param example
     * @return
     */
    public double getValueFor(T example);

    /**
     * 
     * @return the number of parameters of the model
     */
    public int getParameterCount();
}
