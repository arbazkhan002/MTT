package lcrf;

import java.io.BufferedWriter;
import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Vector;

import lcrf.logic.Atom;
import lcrf.logic.Interpretation;
import lcrf.stuff.ArrayStuff;

import org.apache.log4j.Logger;

/**
 * @author Bernd Gutmann
 * 
 */
public class InterpretationExampleContainer  {
    private Vector<String> sequenceIDs;
    
    private Vector<List<Interpretation>> inputInterpretations;

    private Vector<List<Atom>> outputSequences;

    private Vector<Atom> classAtoms;

    public InterpretationExampleContainer(Vector<Atom> classAtoms) {
        assert classAtoms != null;
        
        this.classAtoms = classAtoms;
        this.sequenceIDs = new Vector<String>();
        this.inputInterpretations = new Vector<List<Interpretation>>();
        this.outputSequences = new Vector<List<Atom>>();
    }

    public InterpretationExampleContainer(int size, Vector<Atom> classAtoms) {
        assert size >= 0;
        assert classAtoms != null;

        this.classAtoms = classAtoms;
        this.sequenceIDs = new Vector<String>(size);
        this.inputInterpretations = new Vector<List<Interpretation>>(size);
        this.outputSequences = new Vector<List<Atom>>(size);        
    }
    
    public void addExample(List<Interpretation> inputInterpretation, List<Atom> outputSequence) {
        addExample(inputInterpretation,outputSequence,null);
    }

    public void addExample(List<Interpretation> inputInterpretation, List<Atom> outputSequence, String id) {
        assert inputInterpretation != null;
        assert outputSequence != null;
        assert inputInterpretation.size() == outputSequence.size();

        outer: for (int i = 0; i < outputSequence.size(); i++) {
            if (classAtoms.contains(outputSequence.get(i)))
                continue;
            for (Atom a : classAtoms) {
                if (a.isMoreGeneralThan(outputSequence.get(i)))
                    continue outer;
            }
            throw new IllegalArgumentException(inputInterpretation.toString() + "->" + outputSequence.toString()
                    + " at " + i);
        }

        inputInterpretations.add(inputInterpretation);
        outputSequences.add(outputSequence);
        sequenceIDs.add(id);
    }

    public void addExamples(InterpretationExampleContainer ex2) {
        if (ex2 != null) {
            for (int i = 0; i < ex2.size(); i++) {
                addExample(ex2.getInputInterpretations(i), ex2.getOutputSequence(i));
            }

            for (Atom a : ex2.classAtoms) {
                if (!classAtoms.contains(a)) {
                    classAtoms.add(a);
                }
            }
        }
    }

    public int size() {
        return this.inputInterpretations.size();
    }

    public List<Interpretation> getInputInterpretations(int n) {
        return this.inputInterpretations.get(n);
    }

    public List<Atom> getOutputSequence(int n) {
        return this.outputSequences.get(n);
    }

    public InterpretationExampleContainer getSubfold(int folds, int foldnr, long seed) {
        assert folds > 0;
        assert folds <= this.size();
        assert foldnr >= 0;
        assert foldnr < folds;

        int[] swaparray = ArrayStuff.getRandomizedIdendityArray(this.size(), seed);
        int foldsize = this.size() / folds;
        int startindex = foldnr * foldsize;
        int stopindex = (foldnr == folds) ? this.size() : startindex + foldsize;

        InterpretationExampleContainer resultFold = new InterpretationExampleContainer(foldsize, classAtoms);
        for (int i = startindex; i < stopindex; i++) {
            resultFold.addExample(this.getInputInterpretations(swaparray[i]), this.getOutputSequence(swaparray[i]));
        }

        return resultFold;
    }

    public InterpretationExampleContainer getSubfoldInverse(int folds, int foldnr, long seed) {
        assert folds > 0;
        assert folds <= this.inputInterpretations.size();
        assert foldnr >= 0;
        assert foldnr < folds;

        int[] swaparray = ArrayStuff.getRandomizedIdendityArray(this.size(), seed);
        int foldsize = this.size() / folds;
        int startindex = foldnr * foldsize;
        int stopindex = (foldnr == folds - 1) ? this.size() : startindex + foldsize;

        InterpretationExampleContainer resultFold = new InterpretationExampleContainer(size() * (folds - 1) / folds,
                classAtoms);
        for (int i = 0; i < startindex; i++) {
            resultFold.addExample(inputInterpretations.get(swaparray[i]), outputSequences.get(swaparray[i]));
        }
        for (int i = stopindex; i < this.inputInterpretations.size(); i++) {
            resultFold.addExample(inputInterpretations.get(swaparray[i]), outputSequences.get(swaparray[i]));
        }

        return resultFold;

    }

    public boolean haveSameExamples(InterpretationExampleContainer ex2) {
        if (ex2 == null || size() != ex2.size()) {
            return false;
        }

        for (int i = 0; i < size(); i++) {
            int i2 = ex2.inputInterpretations.indexOf(getInputInterpretations(i));
            if (i2 < 0 || !this.getOutputSequence(i).equals(ex2.getOutputSequence(i2))) {
                return false;
            }

            i2 = inputInterpretations.indexOf(ex2.getInputInterpretations(i));
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
            for (int i = 0; i < this.inputInterpretations.size(); i++) {
                List<Interpretation> input = inputInterpretations.get(i);
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
            averageLength += getInputInterpretations(i).size();
        }
        return (double) averageLength / (double) size();
    }

    public String toString() {
        return "InterpretationExampleContainer, " + size() + " examples, atoms are " + this.classAtoms;
    }
    
    public String toStringLong() {                
        return "InterpretationExampleContainer("+classAtoms+","+inputInterpretations+","+outputSequences+","+sequenceIDs+")";
    }
    
}
