package lcrf.logic;

import java.io.StringReader;
import java.util.Vector;

import junit.framework.TestCase;
import lcrf.logic.parser.AtomParser;

public class AtomParserTest extends TestCase {
    public void testConstant() throws Exception {

        AtomParser parser = new AtomParser(new StringReader(" dog  (  A )"));
        Term t_parsed = parser.Term();
        Vector<Term> subterms = new Vector<Term>();
        subterms.add(new Variable("A"));
        Constant t_constructed = new Constant("dog", subterms);
        assertEquals(t_constructed, t_parsed);
    }

    public void testConstant2() throws Exception {
        AtomParser parser = new AtomParser(new StringReader("a(  a(b))"));
        Term t_parsed = parser.Term();
        Vector<Term> subterms = new Vector<Term>();
        subterms.add(new Constant("b", new Vector<Term>()));
        Vector<Term> subterms2 = new Vector<Term>();
        subterms2.add(new Constant("a", subterms));

        Constant t_constructed = new Constant("a", subterms2);
        assertEquals(t_constructed, t_parsed);

    }

    public void testConstant3() throws Exception {
        AtomParser parser = new AtomParser(new StringReader("a(  a(b,'hello'), 42)"));
        Term t_parsed = parser.Term();

        Vector<Term> subterms = new Vector<Term>();
        subterms.add(new Constant("b"));
        subterms.add(new StringConstant("hello"));

        Vector<Term> subterms2 = new Vector<Term>();
        subterms2.add(new Constant("a", subterms));
        subterms2.add(new NumberConstant(42));

        Constant t_constructed = new Constant("a", subterms2);
        assertEquals(t_constructed, t_parsed);
    }

}
