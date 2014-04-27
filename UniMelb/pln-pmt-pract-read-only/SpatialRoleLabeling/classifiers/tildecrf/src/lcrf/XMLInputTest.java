package lcrf;

import java.util.List;

import junit.framework.TestCase;
import lcrf.logic.TermSchema;

import org.apache.log4j.BasicConfigurator;

public class XMLInputTest extends TestCase {
    public void setUp() {
        BasicConfigurator.resetConfiguration();
        BasicConfigurator.configure();
    }

    public void testReadBackgroundKnowledge() {
        WindowMaker wm = XMLInput.makeWindowMakerWithBGKnowledge("stuff/bgknowledge1.xml", 3);

        assertEquals(8, wm.getRealWindowSize());
    }

    public void testReadSchemata() {
        List<TermSchema> schemata = XMLInput.readSchemata("stuff/schemata3.xml");

        assertEquals(2, schemata.size());
    }

    public void testReadSequencesDOM() {
        XMLInput.readSequencesDOM("data/proteinfolds_kristian/fold2l.xml");
    }

    public void testReadInOutExamples() {
        SimpleExampleContainer c1 = XMLInput
                .readInOutExamplesDOM("data/qs-proteins_dietterich/protein_test.xml");
        SimpleExampleContainer c2 = XMLInput
                .readInOutExamplesSAX("data/qs-proteins_dietterich/protein_test.xml");
        assertTrue(c1.haveSameExamples(c2));
    }
}
