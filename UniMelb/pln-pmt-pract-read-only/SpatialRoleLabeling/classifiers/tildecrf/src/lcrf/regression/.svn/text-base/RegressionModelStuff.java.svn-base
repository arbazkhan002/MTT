package lcrf.regression;

import java.io.Serializable;
import java.util.List;
import java.util.Vector;

import lcrf.stuff.ArrayStuff;

import org.apache.log4j.Logger;

/**
 * @author Bernd Gutmann
 */
public class RegressionModelStuff<T> implements Serializable {
    private static final long serialVersionUID = 3618133433826488888L;

    public double calcAverageError(RegressionModel<T> model, List<RegressionExample<T>> examples) {
        assert model != null;
        assert examples != null;

        double error = 0;
        for (int i = 0; i < examples.size(); i++) {
            error += Math.abs(model.getValueFor(examples.get(i).content) - examples.get(i).value);
        }

        return (examples.size() > 0) ? error / examples.size() : 0;
    }

    public double calcAverageRelativeError(RegressionModel<T> model, List<RegressionExample<T>> examples) {
        assert model != null;
        assert examples != null;

        if (examples.size() == 0) {
            return 0.0;
        }

        double sum = 0.0;
        int counter = 0;
        for (RegressionExample<T> e : examples) {
            if (e.value != 0.0) {
                counter++;
                sum += Math.abs((model.getValueFor(e.content) - e.value) / e.value);
            }
        }

        assert sum >= 0;

        return (counter > 0) ? sum / counter : 0.0;
    }

    public void logExamples(List<T> examples, List<Double> values) {
        Logger logger = Logger.getLogger(this.getClass());
        for (int i = 0; i < examples.size(); i++) {
            logger.info(examples.get(i) + " : " + values.get(i));
        }
    }

    public List<RegressionExample<T>> cloneExamples(List<RegressionExample<T>> examples) {
        assert examples != null;

        Vector<RegressionExample<T>> examples2 = new Vector<RegressionExample<T>>(examples.size());
        for (RegressionExample<T> e : examples) {
            examples2.add(e);
        }

        return examples2;
    }

    public final double calcAverage(List<RegressionExample<T>> examples) {
        assert examples != null;
        if (examples.size() == 0) {
            return 0.0;
        }
        double sum = 0.0;
        for (RegressionExample e : examples) {
            sum += e.value;
        }

        return sum / examples.size();
    }

    public final double calcAbsAverage(List<RegressionExample<T>> examples) {
        assert examples != null;
        if (examples.size() == 0) {
            return 0.0;
        }
        double sum = 0.0;
        for (RegressionExample e : examples) {
            sum += Math.abs(e.value);
        }

        return sum / examples.size();
    }

    public List<RegressionExample<T>> getRandomSubSample(List<RegressionExample<T>> examples, int size,
            long seed) {
        assert examples != null;

        int endsize = Math.min(size, examples.size());
        int[] switchArray = ArrayStuff.getRandomizedIdendityArray(endsize, seed);
        Vector<RegressionExample<T>> examples2 = new Vector<RegressionExample<T>>(endsize);

        for (int i = 0; i < endsize; i++) {
            examples2.add(examples.get(switchArray[i]));
        }

        return examples2;
    }

    /*
     * public int[] getClassCountarray(List<RegressionExample<T>> examples,
     * int classes) { assert examples != null; assert classes>0; int[] result =
     * new int[classes]; for (int i=0; i<examples.size(); i++) { if
     * (examples.get(i).classNumber>-1) { result[examples.get(i).classNumber]++ ; } }
     * return result; }
     */
}
