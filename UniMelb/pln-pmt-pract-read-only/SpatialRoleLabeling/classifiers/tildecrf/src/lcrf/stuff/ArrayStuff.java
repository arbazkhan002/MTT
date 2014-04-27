/*
 * ArrayStuff.java
 *
 * Albert-Ludwig-University Freiburg
 * Probabalistic Logic Learning
 * Practical
 * Winterterm 2003/2004
 *
 * Coded by Bernd Gutmann <bgutmann@informatik.uni-freiburg.de>
 */

package lcrf.stuff;

import java.util.List;
import java.util.Random;

/**
 * This class provides some often used lowlevel array routines.
 * 
 * @author Bernd Gutmann
 * @version 15 Dez 2003, 19:43
 */

public class ArrayStuff {

    /**
     * example removeTrueNodes([0,1,4] , [True,False,True,False,False]) = [1,4]
     * 
     * @param ar
     * @param remove
     * @return the array ar, where all entries are removed that are true in
     *         remove
     */
    public static int[] removeTrueEntries(int[] ar, boolean[] remove) {
        if (ar == null || remove == null) {
            return ar;
        }
        int length = 0;
        for (int i = 0; i < ar.length; i++) {
            if (remove[ar[i]] == false) {
                length++;
            }
        }
        int[] result = new int[length];
        int pointer = 0;
        for (int i = 0; i < ar.length; i++) {
            if (remove[ar[i]] == false) {
                result[pointer] = ar[i];
                pointer++;
            }
        }

        return result;

    }

    /**
     * @return true if n appears somewhere in ar false otherwise or if ar is
     *         null
     */
    public static boolean appearsInArray(int[] ar, int n) {
        return (indexInArray(ar, n) > -1);
    }

    /**
     * @return index, if ar[index] = n -1 otherwise
     */
    public static int indexInArray(int[] ar, int n) {
        if (ar == null) {
            return -1;
        }
        for (int i = 0; i < ar.length; i++) {
            if (ar[i] == n) {
                return i;
            }
        }
        return -1;
    }

    /**
     * @return an int-array of size filled with true values.
     */
    public static boolean[] getTrueArray(int size) {
        boolean[] tmpArray = new boolean[size];

        for (int i = 0; i < size; i++) {
            tmpArray[i] = true;
        }
        return tmpArray;
    }

    public static int[] getRandomizedIdendityArray(int size, long seed) {
        assert size > 0;

        int[] result = new int[size];
        for (int i = 0; i < size; i++) {
            result[i] = i;
        }

        Random random = new Random(seed);

        for (int i = 0; i < size; i++) {
            int i2 = random.nextInt(size);

            int tmp = result[i];
            result[i] = result[i2];
            result[i2] = tmp;
        }

        return result;
    }

    /**
     * <p>
     * This methods generates an int-array of the same size as ar.
     * </p>
     * <p>
     * If ar[i] is true, then result[i]=j, if ar[i] is the j. true value in ar.<br
     * If ar[i] is false, then result[i]=-1.
     * </p>
     * <p>
     * Example: {true, false, true,false,true} leads to {0, -1, 1, -1, 2}.
     * </p>
     */
    public static int[] booleanArrayToIntArray(boolean[] ar) {
        int[] tmp = new int[ar.length];
        int pointer = 0;

        for (int i = 0; i < ar.length; i++) {
            tmp[i] = (ar[i]) ? pointer++ : -1;
        }
        return tmp;
    }

    public static int[] translateUsingIndex(int[] ar, int[] index) {
        if (ar == null) {
            return null;
        }

        int[] tmp = new int[ar.length];

        for (int i = 0; i < ar.length; i++) {
            tmp[i] = index[ar[i]];

        }
        return tmp;
    }

    /**
     * The result is the number of nonnegative numbers in ar.
     */
    public static int countPositives(int[] ar) {
        int n = 0;

        for (int i = 0; i < ar.length; i++) {
            if (ar[i] > -1) {
                n++;
            }
        }
        return n;
    }

    public static int countTrues(boolean[] ar) {
        int count = 0;
        for (int i = 0; ar != null && i < ar.length; i++) {
            if (ar[i]) {
                count++;
            }
        }
        return count;
    }

    /**
     * The result is the number of nonnegative numbers in ar. Where ar is
     * adressed indirect via index.
     */
    public static int countPositivesIndirect(int[] ar, int[] index) {
        int n = 0;

        for (int i = 0; i < ar.length; i++) {
            if (index[ar[i]] > -1) {
                n++;
            }
        }
        return n;
    }

    /**
     * @param ar
     *            an int-array, must not be null
     * @param target
     *            a int value, which has to be removed from ar
     * @return the ar array without the target value
     */
    public static int[] removeFromArray(int[] ar, int target) {
        int n = 0;

        // how big has has result to be
        for (int i = 0; i < ar.length; i++) {
            if (ar[i] != target) {
                n++;
            }
        }

        int[] cleanedAr = new int[n];

        for (int i = 0; i < n; i++) {
            int j = 0;

            while (ar[j] == target) {
                j++;
            }
            cleanedAr[i] = ar[j];
        }
        return cleanedAr;
    }

    public static int[] combineArrays(int[] ar1, int[] ar2) {
        if (ar1 == null)
            return ar2;
        if (ar2 == null)
            return ar1;

        int size = ar1.length;
        for (int i = 0; i < ar2.length; i++) {
            if (!appearsInArray(ar1, ar2[i]))
                size++;
        }

        int[] result = new int[size];
        for (int i = 0; i < ar1.length; i++) {
            result[i] = ar1[i];
        }
        int pointer = ar1.length;
        for (int i = 0; i < ar2.length; i++) {
            if (!appearsInArray(ar1, ar2[i])) {
                result[pointer] = ar2[i];
                pointer++;
            }
        }

        return result;
    }

    public static void printArray(int[] ar) {
        System.out.print("[");
        for (int i = 0; i < ar.length; i++) {
            System.out.print(ar[i] + "  ");
        }
        System.out.println("]");
    }

    public static void printArray(double[] ar) {
        System.out.print("[");
        for (int i = 0; i < ar.length; i++) {
            System.out.print(ar[i] + "  ");
        }
        System.out.println("]");
    }

    public static void printArray(boolean[] ar) {
        System.out.print("[");
        for (int i = 0; i < ar.length; i++) {
            System.out.print(ar[i] + "  ");
        }
        System.out.println("]");
    }
    
    public static String toString(double[][] ar) {
        if (ar == null) {
            return "null";
        }
        
        if (ar.length == 0) {
            return "{ }";
        }

        String result = "";
        for (double[] part : ar) {            
            result += ArrayStuff.toString(part) + ",\n ";
        }
        return "{\n" + result.substring(0, result.length() - 2) + "\n}";        
    }

    public static String toString(Object[] ar) {
        if (ar == null) {
            return "null";
        }
        
        if (ar.length == 0) {
            return "{ }";
        }

        String result = "";
        for (Object o : ar) {            
            result += o + ", ";
        }
        return "{" + result.substring(0, result.length() - 2) + "}";
    }
    
    public static String toString(double[] ar) {
        if (ar == null) {
            return "null";
        }
        
        if (ar.length == 0) {
            return "{ }";
        }

        String result = "";
        for (Object o : ar) {
            result += o + ", ";
        }
        return "{" + result.substring(0, result.length() - 2) + "}";
    }


    public static String toString(int[] ar) {
        if (ar == null) {
            return "null";
        }

        String result = "";
        for (Object o : ar) {
            result += o + ", ";
        }
        return "{" + result.substring(0, result.length() - 2) + "}";
    }

    public static double[] cloneArray(double[] ar) {
        if (ar == null)
            return null;
        double[] result = new double[ar.length];
        System.arraycopy(ar, 0, result, 0, ar.length);
        return result;
    }

    public static int argmax(int[] a) {
        if (a == null) {
            throw new IllegalArgumentException("Input must not be null.");
        }

        int argmax = 0;

        for (int i = 1; i < a.length; i++) {
            if (a[i] > a[argmax]) {
                argmax = i;
            }
        }

        return argmax;
    }

    /**
     * adds the both integer arrays elementwise. both arrays must have the same
     * length
     * 
     * @param a
     * @param b
     */
    public static int[] addToTheArray(int[] a, int[] b) {
        if (a == null || b == null || a.length != b.length) {
            throw new IllegalArgumentException();
        }

        int[] result = new int[a.length];

        for (int i = 0; i < a.length; i++) {
            result[i] = a[i] + b[i];
        }

        return result;
    }

    public static int sumAll(int[] a) {
        if (a == null)
            throw new IllegalArgumentException();

        int sum = 0;
        for (int i = 0; i < a.length; i++) {
            sum += a[i];
        }
        return sum;
    }

    public static boolean arrayEquals(int[] a1, int[] a2) {
        if (a1 == null || a2 == null) {
            return a1 == null && a2 == null;
        }
        if (a1.length != a2.length) {
            return false;
        }
        for (int i = 0; i < a1.length; i++) {
            if (a1[i] != a2[i])
                return false;
        }
        return true;
    }
    
    
    
    
    
    public static String toConfusionMatrix (List names, int[][] counts) {
        assert names != null;
        assert counts != null;
        assert names.size() == counts.length;
        
        int correct=0;
        int all=0;
        
        String result = "Confusion matrix:\n";
        for (Object o:names) {
            result += "\t" + o;
        }
        result += "\n";
        
        for (int i=0; i<names.size(); i++) {
            assert counts[i] != null;
            assert names.size() == counts[i].length;
            
            result += names.get(i);
            for (int j=0; j<counts[i].length; j++) {
                result += "\t"+counts[i][j];
                all += counts[i][j];
                if (i==j) 
                    correct += counts[i][j];                
            }
            result += "\n";            
        }
        result += "Accuracy : " +( (double) correct / (double) all) + "\n";
        
        return result;                                                
    }
}
