package lcrf.logic;

import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Vector;

import junit.framework.TestCase;

public class SchemaUnificationJobGeneratorTest extends TestCase {
    private TermSchema schema1;

    private TermSchema schema2;

    public void setUp() throws Exception {
        Term schemaTerm1 = new Atom("value(X,Y)").getTermRepresentation();
        HashMap<Variable, List<Term>> h1 = new HashMap<Variable, List<Term>>();
        List<Term> substitutions11 = new Vector<Term>();
        substitutions11.add(new StringConstant("width"));
        substitutions11.add(new Constant("height"));
        List<Term> substitutions12 = new Vector<Term>();
        substitutions12.add(new NumberConstant(123));
        substitutions12.add(new StringConstant("456"));
        h1.put(new Variable("X"), substitutions11);
        h1.put(new Variable("Y"), substitutions12);
        schema1 = new TermSchema(schemaTerm1, h1, 0);

        Term schemaTerm2 = new Variable("EVERYTHING");
        HashMap<Variable, List<Term>> h2 = new HashMap<Variable, List<Term>>();
        List<Term> substitutions21 = new Vector<Term>();
        substitutions21.add(new StringConstant("belchen"));
        substitutions21.add(new Constant("rinken"));
        h2.put(new Variable("EVERYTHING"), substitutions21);

        schema1 = new TermSchema(schemaTerm1, h1, 0);
        schema2 = new TermSchema(schemaTerm2, h2, 1);
    }

    public void testWithNoExamples() {
        List<TermSchema> schemata = new Vector<TermSchema>(1);
        schemata.add(schema1);
        Iterator<UnificationJob> iterator = new SchemaUnificationJobGenerator(0, schemata,
                new Vector<Variable>(),0);
        assertFalse(iterator.hasNext());
        try {
            iterator.next();
            fail("No Excpetion was thrown");
        } catch (NoSuchElementException e) {
            // everzthing is fine
        }

    }

    public void testWithOneExamples() throws Exception {
        List<TermSchema> schemata = new Vector<TermSchema>(1);
        schemata.add(schema1);

        Iterator<UnificationJob> iterator = new SchemaUnificationJobGenerator(1, schemata,
                new Vector<Variable>(),0);
        assertTrue(iterator.hasNext());
        assertEquals(new UnificationJob(0, new Atom("value('width',123)").getTermRepresentation()), iterator
                .next());
        assertTrue(iterator.hasNext());
        assertEquals(new UnificationJob(0, new Atom("value(height,123)").getTermRepresentation()), iterator
                .next());
        assertTrue(iterator.hasNext());
        assertEquals(new UnificationJob(0, new Atom("value('width','456')").getTermRepresentation()),
                iterator.next());
        assertTrue(iterator.hasNext());
        assertEquals(new UnificationJob(0, new Atom("value(height,'456')").getTermRepresentation()), iterator
                .next());
        assertFalse(iterator.hasNext());
        try {
            iterator.next();
            fail("No Excpetion was thrown");
        } catch (NoSuchElementException e) {
            // everzthing is fine
        }

    }

    public void testWithOneExamples2() throws Exception {
        List<TermSchema> schemata = new Vector<TermSchema>(1);
        schemata.add(schema1);
        schemata.add(schema2);

        Iterator<UnificationJob> iterator = new SchemaUnificationJobGenerator(1, schemata,
                new Vector<Variable>(),0);
        assertTrue(iterator.hasNext());
        assertEquals(new UnificationJob(0, new Atom("value('width',123)").getTermRepresentation()), iterator
                .next());
        assertTrue(iterator.hasNext());
        assertEquals(new UnificationJob(0, new Atom("value(height,123)").getTermRepresentation()), iterator
                .next());
        assertTrue(iterator.hasNext());
        assertEquals(new UnificationJob(0, new Atom("value('width','456')").getTermRepresentation()),
                iterator.next());
        assertTrue(iterator.hasNext());
        assertEquals(new UnificationJob(0, new Atom("value(height,'456')").getTermRepresentation()), iterator
                .next());
        assertTrue(iterator.hasNext());
        assertEquals(new UnificationJob(0, new Atom("'belchen'").getTermRepresentation()), iterator.next());
        assertTrue(iterator.hasNext());
        assertEquals(new UnificationJob(0, new Atom("rinken").getTermRepresentation()), iterator.next());
        assertFalse(iterator.hasNext());
        try {
            iterator.next();
            fail("No Excpetion was thrown");
        } catch (NoSuchElementException e) {
            // everzthing is fine
        }

    }

}
