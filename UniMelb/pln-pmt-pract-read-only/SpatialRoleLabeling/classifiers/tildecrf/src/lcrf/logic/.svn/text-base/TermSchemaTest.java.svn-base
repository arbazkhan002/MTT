package lcrf.logic;

import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Vector;

import junit.framework.TestCase;

import org.apache.log4j.BasicConfigurator;

public class TermSchemaTest extends TestCase {
    public void setUp() {
        BasicConfigurator.resetConfiguration();
        BasicConfigurator.configure();
    }

    public void testSchemaWithNoFreeVariables() throws Exception {
        Term schemaTerm = (new Atom("i(am(a(simple(term))))")).getTermRepresentation();        
        Iterator<Term> termiterator = new TermSchema(schemaTerm, 2).iterator(new Vector<Variable>(),0);
        
        assertTrue(termiterator.hasNext());
        Term t = termiterator.next();
        assertEquals(schemaTerm, t);
        assertEquals(2,t.getType());
        assertFalse(termiterator.hasNext());
    }

    public void testSchemaWithOneFreeVariable() throws Exception {
        int schemaType = 45;
        
        Term schemaTerm = (new Atom("i(am(a(elaborated(Term))))")).getTermRepresentation();
        HashMap<Variable, List<Term>> h = new HashMap<Variable, List<Term>>();
        List<Term> substitutions1 = new Vector<Term>();
        substitutions1.add(new NumberConstant(42));
        substitutions1.add(new StringConstant("P equals NP"));
        h.put(new Variable("Term"), substitutions1);

        TermSchema schema = new TermSchema(schemaTerm, h, schemaType);
        Iterator<Term> termiterator = schema.iterator(new Vector<Variable>(),0);
        
        assertTrue(termiterator.hasNext());
        Term t = termiterator.next();
        assertEquals((new Atom("i(am(a(elaborated(42))))")).getTermRepresentation(), t);
        assertEquals(schemaType,t.getType());
        
        assertTrue(termiterator.hasNext());        
        Term t2 = termiterator.next();
        assertEquals((new Atom("i(am(a(elaborated('P equals NP'))))")).getTermRepresentation(),t2);
        assertEquals(schemaType,t.getType());
        
        assertFalse(termiterator.hasNext());
    }

    public void testSchemaWithOneFreeVariableAndBoundedVars() throws Exception {
        int schemaType = 46;
        int freeVariableType = 373;
        
        Term schemaTerm = (new Atom("i(am(a(elaborated(Term))))")).getTermRepresentation();
        schemaTerm.getContainedVariables().get(0).setVariableType(freeVariableType);
        HashMap<Variable, List<Term>> h = new HashMap<Variable, List<Term>>();
        List<Term> substitutions1 = new Vector<Term>();
        substitutions1.add(new NumberConstant(42));
        substitutions1.add(new StringConstant("P equals NP"));
        substitutions1.add(new Variable(TermSchema.UNBOUNDEDVAR));
        substitutions1.add(new Variable(TermSchema.BOUNDEDVAR));        
        h.put(new Variable("Term"), substitutions1);
        
        
        List<Variable> boundedVars = new Vector<Variable>();

        TermSchema schema = new TermSchema(schemaTerm, h, schemaType);
        Iterator<Term> termiterator = schema.iterator(boundedVars,0);
        
        assertTrue(termiterator.hasNext());
        Term t1 = termiterator.next();
        assertEquals((new Atom("i(am(a(elaborated(42))))")).getTermRepresentation(), t1);
        assertEquals(schemaType,t1.getType());
        
        assertTrue(termiterator.hasNext());
        Term t2 = termiterator.next();
        assertEquals((new Atom("i(am(a(elaborated('P equals NP'))))")).getTermRepresentation(), t2);
        assertEquals(schemaType,t2.getType());
        
        assertTrue(termiterator.hasNext());
        Term t3 = termiterator.next();
        assertEquals((new Atom("i(am(a(elaborated(__0))))")).getTermRepresentation(), t3);
        assertEquals(schemaType,t3.getType());
        assertEquals(freeVariableType,t3.getContainedVariables().get(0).getVariableType());
        
        assertFalse(termiterator.hasNext());

        boundedVars.add(new Variable("__0"));
        termiterator = schema.iterator(boundedVars,0);
        assertTrue(termiterator.hasNext());
        assertEquals((new Atom("i(am(a(elaborated(42))))")).getTermRepresentation(), termiterator.next());
        assertTrue(termiterator.hasNext());
        assertEquals((new Atom("i(am(a(elaborated('P equals NP'))))")).getTermRepresentation(), termiterator
                .next());
        assertTrue(termiterator.hasNext());
        assertEquals((new Atom("i(am(a(elaborated(__1))))")).getTermRepresentation(), termiterator.next());
        assertFalse(termiterator.hasNext());
        
        Variable v2 = new Variable("__1");
        v2.setVariableType(freeVariableType);
        boundedVars.add(v2);
        termiterator = schema.iterator(boundedVars,0);
        assertTrue(termiterator.hasNext());
        assertEquals((new Atom("i(am(a(elaborated(42))))")).getTermRepresentation(), termiterator.next());
        assertTrue(termiterator.hasNext());
        assertEquals((new Atom("i(am(a(elaborated('P equals NP'))))")).getTermRepresentation(), termiterator
                .next());
        assertTrue(termiterator.hasNext());
        assertEquals((new Atom("i(am(a(elaborated(__2))))")).getTermRepresentation(), termiterator.next());
        assertTrue(termiterator.hasNext());               
        assertEquals((new Atom("i(am(a(elaborated(__1))))")).getTermRepresentation(), termiterator.next());
        assertFalse(termiterator.hasNext());
    }

    public void testSchemaWithTwoFreeVariables() throws Exception {
        Term schemaTerm = (new Atom("i(am(a(very,elaborated(Term),_OK)))")).getTermRepresentation();
        HashMap<Variable, List<Term>> h = new HashMap<Variable, List<Term>>();
        List<Term> substitutions1 = new Vector<Term>();
        substitutions1.add(new NumberConstant(42));
        substitutions1.add(new StringConstant("P equals NP"));
        List<Term> substitutions2 = new Vector<Term>();
        substitutions2.add(new NumberConstant(123456));
        substitutions2.add(new StringConstant("just kidding"));
        h.put(new Variable("Term"), substitutions1);
        h.put(new Variable("_OK"), substitutions2);

        TermSchema schema = new TermSchema(schemaTerm, h, 0);
        Iterator<Term> termiterator = schema.iterator(new Vector<Variable>(),0);
        assertTrue(termiterator.hasNext());
        assertEquals((new Atom("i(am(a(very,elaborated(42),123456)))")).getTermRepresentation(), termiterator
                .next());
        assertTrue(termiterator.hasNext());
        assertEquals((new Atom("i(am(a(very,elaborated('P equals NP'),123456)))")).getTermRepresentation(),
                termiterator.next());
        assertTrue(termiterator.hasNext());
        assertEquals((new Atom("i(am(a(very,elaborated(42),'just kidding')))")).getTermRepresentation(),
                termiterator.next());
        assertTrue(termiterator.hasNext());
        assertEquals((new Atom("i(am(a(very,elaborated('P equals NP'),'just kidding')))"))
                .getTermRepresentation(), termiterator.next());
        assertFalse(termiterator.hasNext());

    }

}
