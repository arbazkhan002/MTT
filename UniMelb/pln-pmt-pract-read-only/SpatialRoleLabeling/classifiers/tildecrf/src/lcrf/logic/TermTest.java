package lcrf.logic;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.Vector;

import junit.framework.TestCase;

public class TermTest extends TestCase {
    public void testContainsVariable() {
        Term t1 = new Variable("X");
        Term t2 = new StringConstant("hitchhiker");
        Vector<Term> subterms = new Vector<Term>();
        subterms.add(t1);
        subterms.add(t2);
        Constant t3 = new Constant("m", subterms);

        assertTrue(t1.containsVariable(new Variable("X")));
        assertFalse(t2.containsVariable(new Variable("X")));
        assertTrue(t3.containsVariable(new Variable("X")));
    }

    public void testSerialization1() throws Exception {
        Term t1 = new Atom("the(dog,is,green(with,'a',long,nose(8)))").getTermRepresentation();

        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        new ObjectOutputStream(baos).writeObject(t1);
        ByteArrayInputStream bais = new ByteArrayInputStream(baos.toByteArray());
        Object o = new ObjectInputStream(bais).readObject();        

        assertTrue(o instanceof Term);
        assertEquals(t1, (Term) o);
        assertFalse(t1 == o);
    }

}
