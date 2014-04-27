package lcrf;

import java.io.BufferedWriter;
import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Vector;

import lcrf.logic.Atom;
import lcrf.stuff.ArrayStuff;

import org.apache.log4j.Logger;

/**
 * @author Bernd Gutmann
 * 
 */
public class SimpleExampleContainer implements ExampleContainer {
    private Vector<List<String>> sequenceIDs;
    
    private Vector<List<Atom>> inputSequences;

    private Vector<List<Atom>> outputSequences;

    private Vector<Atom> classAtoms;

    public SimpleExampleContainer(Vector<Atom> classAtoms) {
        assert classAtoms != null;
        
        this.classAtoms = classAtoms;
        this.inputSequences = new Vector<List<Atom>>();
        this.outputSequences = new Vector<List<Atom>>();
    }

    public SimpleExampleContainer(int size, Vector<Atom> classAtoms) {
        assert size >= 0;
        assert classAtoms != null;

        this.classAtoms = classAtoms;
        this.inputSequences = new Vector<List<Atom>>(size);
        this.outputSequences = new Vector<List<Atom>>(size);        
    }

    public void addExample(List<Atom> inputSequence, List<Atom> outputSequence) {
        assert inputSequence != null;
        assert outputSequence != null;
        assert inputSequence.size() == outputSequence.size();

        outer: for (int i = 0; i < outputSequence.size(); i++) {
            if (classAtoms.contains(outputSequence.get(i)))
                continue;
            for (Atom a : classAtoms) {
                if (a.isMoreGeneralThan(outputSequence.get(i)))
                    continue outer;
            }
            throw new IllegalArgumentException(inputSequence.toString() + "->" + outputSequence.toString()
                    + " at " + i);
        }

        inputSequences.add(inputSequence);
        outputSequences.add(outputSequence);
    }

    public void addExamples(SimpleExampleContainer ex2) {
        if (ex2 != null) {
            for (int i = 0; i < ex2.size(); i++) {
                addExample(ex2.getInputSequence(i), ex2.getOutputSequence(i));
            }

            for (Atom a : ex2.classAtoms) {
                if (!classAtoms.contains(a)) {
                    classAtoms.add(a);
                }
            }
        }
    }

    public int size() {
        return this.inputSequences.size();
    }

    public List<Atom> getInputSequence(int n) {
        return this.inputSequences.get(n);
    }

    public List<Atom> getOutputSequence(int n) {
        return this.outputSequences.get(n);
    }

    public SimpleExampleContainer getSubfold(int folds, int foldnr, long seed) {
        assert folds > 0;
        assert folds <= this.size();
        assert foldnr >= 0;
        assert foldnr < folds;

        int[] swaparray = ArrayStuff.getRandomizedIdendityArray(this.size(), seed);
        int foldsize = this.size() / folds;
        int startindex = foldnr * foldsize;
        int stopindex = (foldnr == folds) ? this.size() : startindex + foldsize;

        SimpleExampleContainer resultFold = new SimpleExampleContainer(foldsize, classAtoms);
        for (int i = startindex; i < stopindex; i++) {
            resultFold.addExample(this.getInputSequence(swaparray[i]), this.getOutputSequence(swaparray[i]));
        }

        return resultFold;
    }

    public SimpleExampleContainer getSubfoldInverse(int folds, int foldnr, long seed) {
        assert folds > 0;
        assert folds <= this.inputSequences.size();
        assert foldnr >= 0;
        assert foldnr < folds;

        int[] swaparray = ArrayStuff.getRandomizedIdendityArray(this.size(), seed);
        int foldsize = this.size() / folds;
        int startindex = foldnr * foldsize;
        int stopindex = (foldnr == folds - 1) ? this.size() : startindex + foldsize;

        SimpleExampleContainer resultFold = new SimpleExampleContainer(size() * (folds - 1) / folds,
                classAtoms);
        for (int i = 0; i < startindex; i++) {
            resultFold.addExample(inputSequences.get(swaparray[i]), outputSequences.get(swaparray[i]));
        }
        for (int i = stopindex; i < this.inputSequences.size(); i++) {
            resultFold.addExample(inputSequences.get(swaparray[i]), outputSequences.get(swaparray[i]));
        }

        return resultFold;

    }

    public boolean haveSameExamples(SimpleExampleContainer ex2) {
        if (ex2 == null || size() != ex2.size()) {
            return false;
        }

        for (int i = 0; i < size(); i++) {
            int i2 = ex2.inputSequences.indexOf(getInputSequence(i));
            if (i2 < 0 || !this.getOutputSequence(i).equals(ex2.getOutputSequence(i2))) {
                return false;
            }

            i2 = inputSequences.indexOf(ex2.getInputSequence(i));
            if (i2 < 0 || !this.getOutputSequence(i2).equals(ex2.getOutputSequence(i))) {
                return false;
            }
        }

        return true;
    }

    public void writeToMalletFile(String filename) {
        try {
            File file = new File(filename);
            BufferedWriter writer = new BufferedWriter(new java.io.FileWriter(file));
            for (int i = 0; i < this.inputSequences.size(); i++) {
                List<Atom> input = inputSequences.get(i);
                List<Atom> output = outputSequences.get(i);

                assert input.size() == output.size();
                if (input.size() > 0) {
                    writer.write("CAPITAL " + input.get(0) + " " + output.get(0) + "\n");
                    for (int j = 1; j < input.size(); j++) {
                        writer.write(input.get(j) + " " + output.get(j) + "\n");
                    }
                    writer.write("\n");
                }
            }
            writer.close();
        } catch (IOException e) {
            Logger.getLogger(this.getClass()).error("IO-Error");
        }

    }

    public List<Atom> getClassAtoms() {
        return classAtoms;
    }

    public double averageSequenceLength() {
        int averageLength = 0;
        for (int i = 0; i < size(); i++) {
            averageLength += getInputSequence(i).size();
        }
        return (double) averageLength / (double) size();
    }

    public String toString() {
        return "SimpleExampleContainer, " + size() + " examples, atoms are " + this.classAtoms;
    }
}
