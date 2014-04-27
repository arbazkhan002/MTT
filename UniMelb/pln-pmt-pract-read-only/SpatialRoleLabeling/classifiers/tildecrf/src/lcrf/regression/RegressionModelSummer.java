/**
 * 
 */
package lcrf.regression;

import java.util.HashMap;
import java.util.Vector;

import org.apache.log4j.Logger;

/**
 * @author Bernd Gutmann
 */
public class RegressionModelSummer<T> implements RegressionModel<T> {
    private static final long serialVersionUID = 3257001064342564913L;

    private Vector<RegressionModel<T>> subModels;

    private HashMap<T, Double> cache;

    public RegressionModelSummer() {
        subModels = new Vector<RegressionModel<T>>(30);
    }

    public void addSubModel(RegressionModel<T> subModel) {
        if (subModel == null) {
            throw new IllegalArgumentException();
        }

        subModels.add(subModel);
    }

    public double getValueFor(T input) {
        double result = 0.0;

        for (int i = 0; i < subModels.size(); i++) {

            result += subModels.get(i).getValueFor(input);
        }
        
        /*if (subModels.size()>0) {
            Logger.getLogger("erhu").debug(input + " " + result);
        }*/

        return result;
    }

    public int getParameterCount() {
        if (subModels.size() == 0) {
            return 0;
        }

        int sum = 0;
        for (RegressionModel<T> subModel : subModels) {
            sum += subModel.getParameterCount();
        }

        return sum;
    }
}
