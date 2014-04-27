package lcrf.regression;

import java.util.Vector;

import junit.framework.TestCase;
import lcrf.logic.Atom;
import lcrf.logic.Interpretation;
import lcrf.logic.parser.ParseException;

import org.apache.log4j.BasicConfigurator;

public class InterpretationRegressionTreeTrainerTest extends TestCase {
    
    public void setUp() {
        BasicConfigurator.resetConfiguration();
        BasicConfigurator.configure();
    }
    
    
    public void testBinaryRepresentation() throws ParseException{
        Vector<RegressionExample<Interpretation>> examplesStrings = new Vector<RegressionExample<Interpretation>>();
        Vector<RegressionExample<Interpretation>> examplesTerms = new Vector<RegressionExample<Interpretation>>();
        
        
        for (int a=0; a<2; a++) {
            for (int b=0; b<2; b++) {
                for (int c=0; c<2; c++) {
                    for (int d=0; d<2; d++) {
                        for (int e=0; e<2; e++) {
                            Interpretation interString = new Interpretation();
                            Interpretation interTerm = new Interpretation();
                            double value = 0.0;
                            if (a==1) {
                                value += 1.0;
                                interString.add(new Atom("posa"));
                                interTerm.add(new Atom("pos(a)"));
                            }
                            if (b==1) {
                                value += 2.0;
                                interString.add(new Atom("posb"));
                                interTerm.add(new Atom("pos(b)"));
                            }
                            if (c==1) {
                                value += 4.0;
                                interString.add(new Atom("posc"));
                                interTerm.add(new Atom("pos(c)"));
                            }
                            if (d==1) {
                                value += 8.0;
                                interString.add(new Atom("posd"));
                                interTerm.add(new Atom("pos(d)"));
                            }
                            if (e==1) {
                                value += 16.0;
                                interString.add(new Atom("pose"));
                                interTerm.add(new Atom("pos(e)"));
                            }
                            
                            examplesStrings.add(new RegressionExample<Interpretation>(interString,value));
                            examplesTerms.add(new RegressionExample<Interpretation>(interTerm,value));
                        }   
                    }   
                }   
            }   
        }
        
        InterpretationRegressionTreeTrainer t = new InterpretationRegressionTreeTrainer(200,1);
        
        t.trainFromExamples(examplesStrings);
        t.trainFromExamples(examplesTerms);        
    }

}
