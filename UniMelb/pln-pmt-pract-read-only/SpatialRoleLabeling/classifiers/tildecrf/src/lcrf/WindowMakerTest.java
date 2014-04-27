/*
 * Created on 09.03.2005
 *
 */
package lcrf;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.List;
import java.util.Vector;

import junit.framework.TestCase;
import lcrf.logic.Atom;
import lcrf.logic.parser.ParseException;

/**
 * @author Bernd Gutmann
 * 
 */
public class WindowMakerTest extends TestCase {
    Atom a1, a2, a3, a4, a5, a6;

    List<Atom> example1;

    List<Atom> example2;

    List<Atom> example3;

    public void setUp() throws ParseException {
        a1 = new Atom("Kandel");
        a2 = new Atom("Platte");
        a3 = new Atom("Hinterwaldkopf");
        a4 = new Atom("Feldberg");
        a5 = new Atom("Stuebenwasen");
        a6 = new Atom("Schauinsland");

        example1 = new Vector<Atom>(3);
        example1.add(a1);
        example1.add(a2);
        example1.add(a3);

        example2 = new Vector<Atom>(3);
        example2.add(a6);
        example2.add(a5);
        example2.add(a4);

        example3 = new Vector<Atom>(3);
        example3.add(a1);
        example3.add(a5);
        example3.add(a4);
    }

    public void test1() throws ParseException {
        WindowMaker wm = new WindowMaker(3);
        wm.setInputsequence(example1);

        List<Atom> window = wm.make(1, new Atom("Marker1"),new Atom("Marker2"));

        assertEquals(5, window.size());
        assertEquals(new Atom("Marker1"), window.get(0));
        assertEquals(new Atom("Marker2"), window.get(1));
        assertEquals(new Atom("Kandel"), window.get(2));
        assertEquals(new Atom("Platte"), window.get(3));
        assertEquals(new Atom("Hinterwaldkopf"), window.get(4));
        
    }

    public void test2() throws ParseException {
        WindowMaker wm = new WindowMaker(3);
        wm.setInputsequence(example1);
        List<Atom> window = wm.make(2, new Atom("Marker"),new Atom("Marker2"));
        assertEquals(5, window.size());
        assertEquals(new Atom("Marker"), window.get(0));
        assertEquals(new Atom("Marker2"), window.get(1));
        assertEquals(new Atom("Platte"), window.get(2));
        assertEquals(new Atom("Hinterwaldkopf"), window.get(3));
        assertEquals(wm.getStopAtom(), window.get(4));
        
    }

    public void test3() throws ParseException {
        WindowMaker wm = new WindowMaker(3);
        wm.setInputsequence(example1);
        List<Atom> window = wm.make(0, new Atom("Marker"),new Atom("Marker2"));

        assertEquals(5, window.size());
        assertEquals(new Atom("Marker"), window.get(0));
        assertEquals(new Atom("Marker2"), window.get(1));
        assertEquals(wm.getStartAtom(), window.get(2));
        assertEquals(new Atom("Kandel"), window.get(3));
        assertEquals(new Atom("Platte"), window.get(4));
        
    }

    public void test4() throws ParseException {
        WindowMaker wm = new WindowMaker(21);
        wm.setInputsequence(example1);
        List<Atom> window = wm.make(0, new Atom("Marker"),new Atom("Marker2"));

        assertEquals(23, window.size());
        assertEquals(new Atom("Marker"), window.get(0));       
        assertEquals(new Atom("Marker2"), window.get(1));
        
        assertEquals(wm.getStartAtom(), window.get(2));
        assertEquals(wm.getStartAtom(), window.get(3));
        assertEquals(wm.getStartAtom(), window.get(4));
        assertEquals(wm.getStartAtom(), window.get(5));
        assertEquals(wm.getStartAtom(), window.get(6));
        assertEquals(wm.getStartAtom(), window.get(7));
        assertEquals(wm.getStartAtom(), window.get(8));
        assertEquals(wm.getStartAtom(), window.get(9));
        assertEquals(wm.getStartAtom(), window.get(10));
        assertEquals(wm.getStartAtom(), window.get(11));        
        assertEquals(new Atom("Kandel"), window.get(12));
        assertEquals(new Atom("Platte"), window.get(13));
        assertEquals(new Atom("Hinterwaldkopf"), window.get(14));

        
    }

    public void testBackgroundKnowledge1() throws ParseException {
        String prologPart = "sameAsNext(N) :- sequence(N,X), N2 is N+1, sequence(N2,X)."
                + "sameAsLast(N) :- sequence(N,X), N2 is N-1, sequence(N2,X)."
                + "inBlock(N) :- sameAsNext(N), sameAsLast(N).";

        Vector<String> featureNames = new Vector<String>();
        featureNames.add("sameAsNext");
        featureNames.add("sameAsLast");
        featureNames.add("inBlock");

        Vector<Atom> sequence = new Vector<Atom>();
        sequence.add(new Atom("red"));
        sequence.add(new Atom("red"));
        sequence.add(new Atom("red"));
        sequence.add(new Atom("blue"));
        sequence.add(new Atom("blue"));
        sequence.add(new Atom("red"));

        WindowMaker wm = new WindowMaker(1, prologPart, featureNames);

        wm.setInputsequence(sequence);
        List<Atom> window = wm.make(0, new Atom("42"),new Atom("21"));

        assertEquals(6, window.size());
        assertEquals(new Atom("42"), window.get(0));
        assertEquals(new Atom("21"), window.get(1));
        assertEquals(new Atom("red"), window.get(2));        
        assertEquals(new Atom("t"), window.get(3));
        assertEquals(new Atom("f"), window.get(4));
        assertEquals(new Atom("f"), window.get(5));

        window = wm.make(1, new Atom("42"),new Atom("21"));
        assertEquals(6, window.size());
        assertEquals(new Atom("42"), window.get(0));
        assertEquals(new Atom("21"), window.get(1));
        assertEquals(new Atom("red"), window.get(2));        
        assertEquals(new Atom("t"), window.get(3));
        assertEquals(new Atom("t"), window.get(4));
        assertEquals(new Atom("t"), window.get(5));

        window = wm.make(2, new Atom("42"),new Atom("21"));
        assertEquals(6, window.size());
        assertEquals(new Atom("42"), window.get(0));
        assertEquals(new Atom("21"), window.get(1));
        assertEquals(new Atom("red"), window.get(2));       
        assertEquals(new Atom("f"), window.get(3));
        assertEquals(new Atom("t"), window.get(4));
        assertEquals(new Atom("f"), window.get(5));

        window = wm.make(3, new Atom("42"),new Atom("21"));
        assertEquals(6, window.size());
        assertEquals(new Atom("42"), window.get(0));
        assertEquals(new Atom("21"), window.get(1));
        assertEquals(new Atom("blue"), window.get(2));
        assertEquals(new Atom("t"), window.get(3));
        assertEquals(new Atom("f"), window.get(4));
        assertEquals(new Atom("f"), window.get(5));

        window = wm.make(4, new Atom("42"),new Atom("21"));
        assertEquals(6, window.size());
        assertEquals(new Atom("42"), window.get(0));
        assertEquals(new Atom("21"), window.get(1));
        assertEquals(new Atom("blue"), window.get(2));
        assertEquals(new Atom("f"), window.get(3));
        assertEquals(new Atom("t"), window.get(4));
        assertEquals(new Atom("f"), window.get(5));

        window = wm.make(5, new Atom("42"),new Atom("21"));
        assertEquals(6, window.size());
        assertEquals(new Atom("42"), window.get(0));
        assertEquals(new Atom("21"), window.get(1));
        assertEquals(new Atom("red"), window.get(2));
        assertEquals(new Atom("f"), window.get(3));
        assertEquals(new Atom("f"), window.get(4));
        assertEquals(new Atom("f"), window.get(5));
    }

    public void testSerialization() throws Exception {
        String prologPart = "sameAsNext(N) :- sequence(N,X), N2 is N+1, sequence(N2,X)."
                + "sameAsLast(N) :- sequence(N,X), N2 is N-1, sequence(N2,X)."
                + "inBlock(N) :- sameAsNext(N), sameAsLast(N).";

        Vector<String> featureNames = new Vector<String>();
        featureNames.add("sameAsNext");
        featureNames.add("sameAsLast");
        featureNames.add("inBlock");

        WindowMaker wm = new WindowMaker(1, prologPart, featureNames);

        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oas = new ObjectOutputStream(baos);
        oas.writeObject(wm);

        ByteArrayInputStream bais = new ByteArrayInputStream(baos.toByteArray());
        ObjectInputStream ois = new ObjectInputStream(bais);
        Object o1 = ois.readObject();

        assertEquals(wm, o1);
    }
    
    public void testGetOutputFields() {
        WindowMaker wm=new WindowMaker(3,null,null);
        assertEquals("[2,3,4]",wm.getOutputFields());
    }

}
