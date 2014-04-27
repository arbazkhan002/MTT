/**
 * 
 */
package lcrf.stuff;

import java.text.DecimalFormat;
import java.util.HashMap;
import java.util.Vector;

/**
 * @author bgutmann
 * 
 */
public class NumberStorage {
    private static HashMap<String, Vector<Double>> storage;

    private static void init() {
        if (NumberStorage.storage == null) {
            NumberStorage.storage = new HashMap<String, Vector<Double>>(10);
        }
    }

    public static void add(String name, double value) {
        NumberStorage.init();

        if (!NumberStorage.storage.containsKey(name)) {
            NumberStorage.storage.put(name, new Vector<Double>(50));
        }

        NumberStorage.storage.get(name).add(value);
    }

    public static String getValuesFor(String name) {
        NumberStorage.init();

        DecimalFormat formatter = new DecimalFormat();
        formatter.setGroupingUsed(false);

        String result = "";

        if (!NumberStorage.storage.containsKey(name))
            return result;

        for (Double value : NumberStorage.storage.get(name)) {
            result += formatter.format(value.doubleValue()) + "\n";
        }

        return result.substring(0, result.length());
    }

    public static void writeContentToLogFiles() {
        NumberStorage.init();
        for (String key : NumberStorage.storage.keySet()) {
            FileWriter.writeToFile("testresults/data_" + key, ".dat", getValuesFor(key));
        }
    }

}
