/**
 * 
 */
package lcrf.stuff;

import java.util.HashMap;

/**
 * @author Bernd Gutmann
 * 
 */
public class Timer {
    private static HashMap<String, Long> timers;

    public static void init() {
        if (Timer.timers == null) {
            Timer.timers = new HashMap<String, Long>(10);
        }
    }

    public static void startTimer(String name) {
        Timer.init();

        if (timers.containsKey(name)) {
            timers.remove(name);
        }

        timers.put(name, new Long(System.currentTimeMillis()));
    }

    public static long getDuration(String name) {
        Timer.init();
        if (timers.containsKey(name)) {
            return System.currentTimeMillis() - timers.get(name).longValue();
        }
        return 0;
    }

    public static String getDurationFormatted(String name) {
        Timer.init();
        long t = 0;
        if (timers.containsKey(name)) {
            t = System.currentTimeMillis() - timers.get(name).longValue();
        }

        int msec = (int) (t % 1000);
        t /= 1000;

        int sec = (int) (t % 60);
        t /= 60;

        String result = Integer.toString(msec);
        while (result.length() < 3) {
            result = result + "0";
        }

        if (sec == 0 && t == 0) {
            return "0," + result + " sec";
        }

        result = Integer.toString(sec) + "," + result + " sec";

        if (t == 0) {
            return result;
        }

        return Long.toString(t) + " min " + result;
    }
}
