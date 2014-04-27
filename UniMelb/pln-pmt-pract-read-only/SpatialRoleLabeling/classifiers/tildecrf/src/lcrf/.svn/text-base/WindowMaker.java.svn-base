/*
 * Created on 09.03.2005
 *
 */
package lcrf;

import java.io.Externalizable;
import java.io.IOException;
import java.io.ObjectInput;
import java.io.ObjectOutput;
import java.util.List;
import java.util.Vector;

import lcrf.logic.Atom;
import lcrf.logic.Constant;
import lcrf.stuff.ArrayStuff;

import org.apache.log4j.Logger;

import xprolog.Engine;
import xprolog.ParseException;

/**
 * @author Bernd Gutmann
 * 
 */
public class WindowMaker implements Externalizable {
    private static final long serialVersionUID = 3257844368319459635L;

    public static final int FIELDINPUT = 1;

    public static final int FIELDOUTPUT = 2;

    public static final int FIELDDIVERSE = 4;

    private Atom startatom;

    private Atom stopatom;

    private Atom trueAtom;

    private Atom falseAtom;

    private int windowSizeHalfed;

    private int realWindowSize;

    private Engine prolog;

    private List<String> featureNames;

    private List<Atom> input;

    private String prologPart;

    /**
     * Generates a default WindowMaker with windowSize 5 and no
     * backgroundknowledge
     * 
     */
    public WindowMaker() {
        init(5, null, null);
    }

    public WindowMaker(int windowSize) {
        init(windowSize, null, null);
    }

    public WindowMaker(int windowSize, String prologPart, List<String> featureNames) {
        init(windowSize, prologPart, featureNames);
    }

    private void init(int windowSize, String prologPart, List<String> featureNames) {
        if (windowSize < 1 || windowSize % 2 == 0) {
            throw new IllegalArgumentException(Integer.toString(windowSize));
        }

        startatom = new Atom(new Constant("sequence_start"));
        stopatom = new Atom(new Constant("sequence_end"));
        trueAtom = new Atom(new Constant("t"));
        falseAtom = new Atom(new Constant("f"));

        this.windowSizeHalfed = windowSize / 2;
        this.prologPart = prologPart;

        if (prologPart != null) {
            try {
                prolog = new Engine(prologPart);
            } catch (ParseException e) {
                throw new RuntimeException("ParseError at WindowMake\n" + e.getMessage());
            }
            this.featureNames = featureNames;
        } else {
            prolog = null;
            this.featureNames = null;
        }

        realWindowSize = windowSizeHalfed * 2 + 3
                + ((this.featureNames == null) ? 0 : this.featureNames.size());
    }

    public int getRealWindowSize() {
        return realWindowSize;
    }

    public void setInputsequence(List<Atom> input) {
        if (input == null)
            throw new IllegalArgumentException();

        this.input = input;

        if (prolog != null) { // assert sequence in prolog
            try {
                prolog.setQuery("retractall( sequence/2 )");
                for (int t = 0; t < input.size(); t++) {
                    // FIXME Integer toString Conversion produces .
                    prolog.setQuery("assert( sequence(" + t + "," + input.get(t) + ") )");
                }
            } catch (ParseException e) {
                throw new RuntimeException(e.getMessage());
            }
        }
    }

    public List<Atom> make(int t, Atom previousClassAtom,Atom classatom) {
        assert classatom != null;

        Vector<Atom> window = new Vector<Atom>(realWindowSize);

        window.add(previousClassAtom);
        window.add(classatom);
        
        // do we need start-symbols?
        int pos = t - windowSizeHalfed;
        int restsize = 2 * windowSizeHalfed + 1;
        while (pos < 0) {
            pos++;
            restsize--;
            window.add(startatom);
        }
        while (pos < input.size() && restsize > 0) {
            window.add(input.get(pos));
            pos++;
            restsize--;
        }
        while (restsize > 0) {
            restsize--;
            window.add(stopatom);
        }

        if (featureNames != null) {

            try {
                for (int i = 0; i < featureNames.size(); i++) {
                    // FIXME Integer toString Conversion produces .
                    if (prolog.setQuery(featureNames.get(i) + "(" + t + ")")) {
                        window.add(trueAtom);
                    } else {
                        window.add(falseAtom);
                    }
                }

            } catch (ParseException e) {
                throw new RuntimeException(e.getMessage());

            }
        }
        return window;
    }

    /**
     * Only used for testing
     * 
     * @return the atom that is used as start symbol
     */
    public Atom getStartAtom() {
        return startatom;
    }

    /**
     * Only used for testing
     * 
     * @return the atom that is used as stop symbol
     */
    public Atom getStopAtom() {
        return stopatom;
    }

    public Atom getTrueAtom() {
        return trueAtom;
    }

    public Atom getFalseAtom() {
        return falseAtom;
    }

    public String toString() {
        return "WindowMaker(" + (this.windowSizeHalfed * 2 + 1) + "," + this.prologPart + " " + featureNames
                + ")";
    }

    public boolean equals(Object anObject) {
        if (this == anObject)
            return true;

        if (anObject instanceof WindowMaker) {
            WindowMaker wm2 = (WindowMaker) anObject;

            return windowSizeHalfed == wm2.windowSizeHalfed
                    && getRealWindowSize() == wm2.getRealWindowSize()
                    && ((prologPart == null) ? wm2.prologPart == null : prologPart.equals(wm2.prologPart))
                    && ((featureNames == null) ? wm2.featureNames == null : featureNames
                            .equals(wm2.featureNames));
        }
        return false;
    }

    /**
     * produces an int-array that containes for each field the type
     * 
     * @return
     */
    public int[] getFieldTypes() {
        int[] result = new int[getRealWindowSize()];
        result[0] = WindowMaker.FIELDOUTPUT;        
        result[1] = WindowMaker.FIELDOUTPUT;
        
        int pos = 2;
        while (pos < (windowSizeHalfed * 2 + 1)) {
            result[pos] = WindowMaker.FIELDINPUT;
            pos++;
        }
        
        while (pos < getRealWindowSize()) {
            result[pos] = WindowMaker.FIELDDIVERSE;
            pos++;
        }
        
        Logger.getLogger(getClass()).info(ArrayStuff.toString(result));

        return result;
    }
    
    /**
     * A prolog list with the output fields as numbers
     * e.g.<pre>[1,2,3,4]</pre>.
     * @return
     */
    public String getOutputFields() {
        String result = "[2";
        
        for (int i=1; i< windowSizeHalfed*2+1; i++) {
            result += "," + Integer.toString(i+2);
        }
        
        return result+"]";                
    }

    
    public void writeExternal(ObjectOutput out) throws IOException {
        out.writeObject(new Integer(windowSizeHalfed * 2 + 1));
        out.writeObject(prologPart);
        out.writeObject(featureNames);
    }

        
    public void readExternal(ObjectInput in) throws IOException, ClassNotFoundException {
        int a = ((Integer) in.readObject()).intValue();
        String b = (String) in.readObject();
        List<String> c = ((List<String>) in.readObject());

        init(a, b, c);
    }

}
