/**
 * 
 */
package lcrf.regression;

import java.io.Serializable;
import java.text.DecimalFormat;
import java.util.List;
import java.util.Random;

import lcrf.stuff.NumberStorage;
import lcrf.stuff.Timer;

import org.apache.log4j.Logger;

/**
 * @param <T>
 * @author Bernd Gutmann
 * 
 */
public class TrainerWrapper<T> implements RegressionModelTrainer<T>, Serializable {
    private static final long serialVersionUID = 3256444694345955126L;

    public RegressionModelTrainer<T> internalTrainer;

    private RegressionModelStuff<T> stuff;

    private Random randomizer;

    private int subsampleSize;

    private int increaseAfter;

    private int increasement;    

    private boolean enableSubsampling;

    private int trainCounter;

    public TrainerWrapper(RegressionModelTrainer<T> trainer) {
        this(trainer, 0, 0, 1, 0);
    }

    public TrainerWrapper(RegressionModelTrainer<T> trainer, long seed, int subsamplesize, int increaseAfter,
            int increasement) {
        if (trainer == null)
            throw new IllegalArgumentException();
        if (subsamplesize < 0)
            throw new IllegalArgumentException(Integer.toString(subsamplesize));
        if (increaseAfter < 1)
            throw new IllegalArgumentException(Integer.toString(increaseAfter));
        if (increasement < 0)
            throw new IllegalArgumentException(Integer.toString(increasement));        
        this.stuff = new RegressionModelStuff<T>();
        this.internalTrainer = trainer;
        this.subsampleSize = subsamplesize;
        this.increaseAfter = increaseAfter;
        this.increasement = increasement;
        this.randomizer = new Random(seed);

        enableSubsampling = (subsamplesize > 0);

        trainCounter = 0;
    }

    public RegressionModel<T> trainFromExamples(List<RegressionExample<T>> examples) {
        Logger logger = Logger.getLogger(internalTrainer.getClass());
        DecimalFormat d = new DecimalFormat();
        d.setMaximumFractionDigits(6);
        d.setMinimumFractionDigits(6);

        List<RegressionExample<T>> copiedExamples = stuff.cloneExamples(examples);
        List<RegressionExample<T>> subsample = null, copiedSubsample = null;

        if (enableSubsampling) {
            subsample = stuff.getRandomSubSample(examples, subsampleSize, randomizer.nextLong());
            copiedSubsample = stuff.cloneExamples(subsample);
        }

        Timer.startTimer("regressiontraining");
        logger.info("Sample         : " + examples.size() + " examples");
        if (enableSubsampling) {
            logger.info("Used subsample : " + subsample.size() + " examples");
            NumberStorage.add("subsamplesize", subsample.size());
        }

        double avg = stuff.calcAbsAverage(examples);
        NumberStorage.add("avgvaluesample", avg);
        logger.info("avg(abs(val(sample)))    : " + d.format(avg));
        if (enableSubsampling) {
            double avg2 = stuff.calcAbsAverage(subsample);
            NumberStorage.add("avgvaluesubsample", avg2);
            logger.info("avg(abs(val(subsample))) : " + d.format(avg2));
        }
        RegressionModel<T> m = internalTrainer.trainFromExamples((enableSubsampling) ? subsample : examples);

        logger.info("training finished, time " + Timer.getDurationFormatted("regressiontraining"));
        logger.info("error on sample    : " + d.format(stuff.calcAverageError(m, copiedExamples)) + " abs, "
                + d.format(stuff.calcAverageRelativeError(m, copiedExamples)) + " rel");
        if (enableSubsampling) {
            logger.info("error on subsample : " + d.format(stuff.calcAverageError(m, copiedSubsample))
                    + " abs, " + d.format(stuff.calcAverageRelativeError(m, copiedSubsample)) + " rel");
        }

        trainCounter++;
        if (trainCounter % increaseAfter == 0) {
            subsampleSize += increasement;
        }

        return m;
    }

}
