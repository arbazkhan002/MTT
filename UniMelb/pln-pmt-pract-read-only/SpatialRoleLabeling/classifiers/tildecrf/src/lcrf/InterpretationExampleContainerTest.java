package lcrf;

import junit.framework.TestCase;

public class InterpretationExampleContainerTest extends TestCase {
    public void testSimple() {
        InterpretationExampleContainer c = XMLInput.readInterpreationExamplesDOM("stuff/simleint1.xml");
        
        System.out.println(c.toStringLong());
    }
    
    public void testDietterichTest() {
        InterpretationExampleContainer c = XMLInput.readInterpreationExamplesDOM("stuff/prot_09_test.xml");
        //InterpretationExampleContainer c2 = XMLInput.readInterpreationExamplesDOM("stuff/prot_09_train.xml");
        
        
        
    }

}
