/**
 * 
 */
package lcrf;

import java.util.List;
import java.util.Vector;

import lcrf.logic.Atom;
import lcrf.stuff.ArrayStuff;

/**
 * @author Bernd Gutmann
 */
public class ClassificationExampleContainer implements ExampleContainer {
    private Vector<String> sequenceIDs;
    
    private Vector<List<Atom>> inputSequences;

    private Vector<Atom> outputClassAtoms;

    private Vector<Atom> classAtoms;

    public ClassificationExampleContainer() {
        this.sequenceIDs = new Vector<String>();
        this.inputSequences = new Vector<List<Atom>>();
        this.outputClassAtoms = new Vector<Atom>();
        this.classAtoms = new Vector<Atom>();
    }
    
    public void addExample(List<Atom> input, Atom classAtom) {
        addExample(input,classAtom,"null");
    }

    public void addExample(List<Atom> input, Atom classAtom, String id) {
        assert input != null;
        assert classAtom != null;

        this.inputSequences.add(input);
        this.outputClassAtoms.add(classAtom);
        this.sequenceIDs.add(id);

        if (!classAtoms.contains(classAtom)) {
            classAtoms.add(classAtom);
        }

        assert inputSequences.size() == outputClassAtoms.size();
    }
    
    public void addExamples(List<List<Atom>> inputs, Atom classAtom,List<String> ids) {
        assert inputs != null;
        assert classAtom != null;
        assert ids != null;
        assert inputs.size() == ids.size();

        this.inputSequences.addAll(inputs);
        this.sequenceIDs.addAll(ids);
        for (int i = 0; i < inputs.size(); i++) {
            this.outputClassAtoms.add(classAtom);
        }

        if (!classAtoms.contains(classAtom)) {
            classAtoms.add(classAtom);
        }
        assert inputSequences.size() == outputClassAtoms.size();
    }


    public void addExamples(List<List<Atom>> inputs, Atom classAtom) {
        assert inputs != null;
        assert classAtom != null;

        this.inputSequences.addAll(inputs);
        for (int i = 0; i < inputs.size(); i++) {
            this.outputClassAtoms.add(classAtom);
            this.sequenceIDs.add("null");
        }

        if (!classAtoms.contains(classAtom)) {
            classAtoms.add(classAtom);
        }
        assert inputSequences.size() == outputClassAtoms.size();
    }

    public void addExamples(ClassificationExampleContainer ex2) {
        assert ex2 != null;
        
        for (int i = 0; i < ex2.size(); i++) {
            addExample(ex2.getInputSequence(i), ex2.getClassAtom(i),ex2.getSequenceId(i));
        }
        assert inputSequences.size() == outputClassAtoms.size();
    }

    public void sortClassAtoms() {
        // do bubble sort over class atoms
        for (int upper = classAtoms.size() - 1; upper > 0; upper--) {
            for (int i = 0; i < upper; i++) {
                if (classAtoms.get(i).toString().compareTo(classAtoms.get(i + 1).toString()) > 0) {
                    Atom tmp = classAtoms.set(i, classAtoms.get(i + 1));
                    classAtoms.set(i + 1, tmp);
                }
            }
        }
    }

    public Atom getClassAtom(int i) {
        return outputClassAtoms.get(i);
    }

    public int size() {
        return this.inputSequences.size();
    }

    public List<Atom> getInputSequence(int n) {
        return this.inputSequences.get(n);
    }
    
    public String getSequenceId(int n) {
        return this.sequenceIDs.get(n);
    }

    public List<List<Atom>> getAllExamples() {
        return this.inputSequences;
    }

    public List<Atom> getOutputSequence(int n) {
        int size = this.inputSequences.get(n).size();
        Atom a = this.outputClassAtoms.get(n);
        List<Atom> outputSequence = new Vector<Atom>(size);

        for (int i = 0; i < size; i++) {
            outputSequence.add(a);
        }

        return outputSequence;
    }

    public List<Atom> getClassAtoms() {
        return this.classAtoms;
    }

    public ClassificationExampleContainer getSubfold(int folds, int foldnr, long seed) {
        assert folds > 0;
        assert folds <= this.inputSequences.size();
        assert foldnr >= 0;
        assert foldnr < folds;

        int[] swaparray = ArrayStuff.getRandomizedIdendityArray(this.inputSequences.size(), seed);
        int foldsize = this.inputSequences.size() / folds;
        int startindex = foldnr * foldsize;
        int stopindex = (foldnr == folds - 1) ? this.inputSequences.size() : startindex + foldsize;

        ClassificationExampleContainer resultFold = new ClassificationExampleContainer();
        for (int i = startindex; i < stopindex; i++) {
            resultFold.addExample(inputSequences.get(swaparray[i]), getClassAtom(swaparray[i]),this.getSequenceId(swaparray[i]));
        }

        return resultFold;
    }

    public ClassificationExampleContainer getSubfoldInverse(int folds, int foldnr, long seed) {
        assert folds > 0;
        assert folds <= this.inputSequences.size();
        assert foldnr >= 0;
        assert foldnr < folds;

        int[] swaparray = ArrayStuff.getRandomizedIdendityArray(this.inputSequences.size(), seed);
        int foldsize = this.inputSequences.size() / folds;
        int startindex = foldnr * foldsize;
        int stopindex = (foldnr == folds - 1) ? this.inputSequences.size() : startindex + foldsize;

        ClassificationExampleContainer resultFold = new ClassificationExampleContainer();
        for (int i = 0; i < startindex; i++) {
            resultFold.addExample(inputSequences.get(swaparray[i]), getClassAtom(swaparray[i]),this.getSequenceId(swaparray[i]));
        }
        for (int i = stopindex; i < this.inputSequences.size(); i++) {
            resultFold.addExample(inputSequences.get(swaparray[i]), getClassAtom(swaparray[i]),this.getSequenceId(swaparray[i]));
        }

        return resultFold;
    }

    /**
     * This method extracts all examples from this ExampleContainer of class a.
     * 
     * @param a
     *            an Atom, of which examples should be contained in this
     *            container
     * @return a List of examples
     */
    public List<List<Atom>> getExamplesForAtom(Atom a) {
        if (a == null) {
            throw new IllegalArgumentException();
        }

        Vector<List<Atom>> examples = new Vector<List<Atom>>();
        for (int i = 0; i < this.size(); i++) {
            if (this.getClassAtom(i).equals(a)) {
                examples.add(this.getInputSequence(i));
            }
        }

        return examples;
    }

    public boolean haveSameExamples(ClassificationExampleContainer ex2) {
        if (ex2 == null) {
            return false;
        }

        if (this == ex2) {
            return true;
        }

        if (ex2.size() != this.size()) {
            return false;
        }

        for (int i = 0; i < this.size(); i++) {
            int i2 = ex2.inputSequences.indexOf(this.getInputSequence(i));
            if (i2 < 0 || !getClassAtom(i).equals(ex2.getClassAtom(i2))) {
                return false;
            }

            i2 = inputSequences.indexOf(ex2.getInputSequence(i));
            if (i2 < 0 || !getClassAtom(i2).equals(ex2.getClassAtom(i))) {
                return false;
            }

        }

        return true;

    }

    public String toString() {
        String result = "ClassificationExampleContainer : size=" + size() + ", " + this.classAtoms;
        for (int i = 0; i < size(); i++) {
            result += "\n" + i + ". c=" + getClassAtom(i) + " id="+getSequenceId(i)+" " + inputSequences.get(i);
        }
        return result;
    }

    public String toStringShort() {
        return "ClassificationExampleContainer : size=" + size() + ", " + this.classAtoms;
    }

    public double averageSequenceLength() {
        int sum = 0;
        for (int i = 0; i < size(); i++) {
            sum += getInputSequence(i).size();
        }
        return (double) sum / (double) size();
    }

}
