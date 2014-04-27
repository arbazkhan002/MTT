/**
 * 
 */
package lcrf.stuff;

import java.io.BufferedWriter;
import java.io.File;
import java.text.DecimalFormat;

import org.apache.log4j.Logger;

/**
 * @author Bernd Gutmann
 * 
 */
public class FileWriter {
    public static void writeToFile(String filename, String content, boolean append) {
        try {
            File file = new File(filename);
            BufferedWriter writer = new BufferedWriter(new java.io.FileWriter(file,append));
            writer.write(content);
            writer.close();
            Logger.getLogger(FileWriter.class).info("Written to file : " + filename);
        } catch (Exception e) {
            Logger.getLogger(FileWriter.class).error("IO-Error");
        }

    }

    
    public static void writeToFile(String filename, String content) {
        FileWriter.writeToFile(filename,content,false);
    }

    public static void writeToFile(String prefix, String suffix, String content) {
        int counter = 0;
        DecimalFormat formatter = new DecimalFormat();
        formatter.setMinimumIntegerDigits(4);
        formatter.setMaximumFractionDigits(0);
        formatter.setGroupingUsed(false);
        File file;
        String filename;
        do {
            counter++;
            filename = prefix + formatter.format(counter) + suffix;
            file = new File(filename);
        } while (file.exists());

        FileWriter.writeToFile(filename, content);
    }
}
