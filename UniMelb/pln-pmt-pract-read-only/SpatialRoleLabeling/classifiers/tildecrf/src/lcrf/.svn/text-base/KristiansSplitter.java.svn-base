/**
 * 
 */
package lcrf;

import java.util.List;

import lcrf.stuff.FileWriter;

/**
 * @author bgutmann
 *
 */
public class KristiansSplitter {
    
    public static void main (String[] args) {
        SimpleExampleContainer cont = XMLInput.readInOutExamplesDOM("problem4.xml");
        
        String head="%%% -*- Mode: Prolog; -*\n"+
        "%specify the class atoms\n"+
        "classes([city(a),city(b),city(c),city(d)]).\n\n"+
        "%%%%%%%%%%  Parameters\n"+
        "windowSize(2).\n" +
        "inputPositions([1,2,3,4,5]).\n"+
        "min_NodeSplitSize(5).\n"+
        "min_NodeSplitVariance(0.000001).\n"+
        "max_LeafCount(32).\n"+
        "%%%%%%%%%% Parameters\n"+
        "test(outActIs(Elem)) :-\n"+
        "    classes(Classes),\n"+
        "    member(Elem,Classes).\n"+
        "test(outPrevIs(Elem)) :-\n"+
        "    classes(Classes),\n"+
        "    member(Elem,Classes).\n"+
        "test(outSame).\n"+
        "boundedTest(OldVars,containsAt(Pos,a(A,S))) :-\n"+
        "    inputPositions(Positions),\n"+
        "    member(Pos,Positions),\n"+
        "    (member(A,OldVars);member(A,[1,2,3,4,5,6,7,8,_SomeAct])),\n"+
        "    (member(S,OldVars);member(S,[normal,fast,_SomeSpeed])).\n"+
        "%specify the possible tests\n"+
        "succeds(outActIs(Elem),head(_,Elem,_)).\n"+
        "succeds(outPrevIs(Elem),head(_,_,Elem)).\n"+
        "succeds(outSame,head(_,Elem,Elem)).\n"+
        "succeds(containsAt(Pos,Elem),head(Window,_,_)) :-\n"+
        "    nth(Pos,Window,Elem).\n\n";
                
        for (int fold=0; fold<10; fold++) {
            SimpleExampleContainer train=cont.getSubfoldInverse(10,fold,34l);
            SimpleExampleContainer test=cont.getSubfold(10,fold,34l);
            
            
            String trainPrologFile = "";            
            for (int i=0; i<train.size(); i++) {
                String now = " (\n  "+
                             toPrologList(train.getInputSequence(i))+
                             ",\n  "+
                             toPrologList(train.getOutputSequence(i))+
                             "\n )\n";
                trainPrologFile += now;
                if (i+1<train.size()) {
                    trainPrologFile += ",\n";
                }               
            }            
            String trainOut = "training_set(\n[\n"+trainPrologFile+"]).\n\n";
            
            String testPrologFile = "";            
            for (int i=0; i<test.size(); i++) {
                String now = " (\n  "+
                             toPrologList(test.getInputSequence(i))+
                             ",\n  "+
                             toPrologList(test.getOutputSequence(i))+
                             "\n )\n";
                testPrologFile += now;
                if (i+1<test.size()) {
                    testPrologFile += ",\n";
                }               
            }            
            String testOut = "test_set(\n[\n"+testPrologFile+"]).\n";
            
            String content = head+trainOut + testOut;
            
            FileWriter.writeToFile("activity_split"+fold+".pl",content);

            
            
            
        }
    }
    
    public static String toPrologList(List l) {
        String result="";
        for (Object o:l) {
            result += o.toString() + ", ";
        }
        
        return "["+result.substring(0,result.length()-2)+"]";
    }

}
