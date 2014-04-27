/**
 * 
 */
package lcrf.regression;

import java.util.List;

/**
 * @author Bernd Gutmann
 * 
 */
public interface RegressionModelTrainer<T> {
    /**
     * 
     * @param examples
     * @param values
     * @param classes
     * @return
     */
    public RegressionModel<T> trainFromExamples(List<RegressionExample<T>> examples);
}
