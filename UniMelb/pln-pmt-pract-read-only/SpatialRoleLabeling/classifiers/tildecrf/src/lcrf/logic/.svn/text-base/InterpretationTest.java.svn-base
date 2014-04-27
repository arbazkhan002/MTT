package lcrf.logic;

import junit.framework.TestCase;

public class InterpretationTest extends TestCase {
    
    public void testConstructor() throws Exception {
        Interpretation i1 = new Interpretation();
        
        assertEquals(null,i1.contains(new Atom("tomato").getTermRepresentation(),new Substitutions()));
        
        i1.add(new Atom("tomato"));
        
        assertEquals(new Substitutions(),i1.contains(new Atom("tomato").getTermRepresentation(),new Substitutions()));
        
        Substitutions x = new Substitutions();
        x.add(new Substitution(new Variable("X"),(new Atom("tomato").getTermRepresentation())));
        
        assertEquals(x,i1.contains(new Atom("X").getTermRepresentation(),new Substitutions()));
    }
        
}
