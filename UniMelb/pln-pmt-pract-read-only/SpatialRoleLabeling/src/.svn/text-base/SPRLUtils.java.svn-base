
import edu.stanford.nlp.ling.TaggedWord;
import java.util.ArrayList;

/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author Matias
 */
public class SPRLUtils {
    
    public static void restoreElidedLetters(ArrayList<TaggedWord> tSentence) {
        for (int w=0; w<tSentence.size(); w++) {
            String word = tSentence.get(w).word();
            if("n't".equals(word)) {
                tSentence.get(w).setWord("not");
                if("ca".equals(tSentence.get(w-1).word()))
                    tSentence.get(w-1).setWord("can");
                //And so on...
            }
        }
    }

    public static String constructRestoredSentence(ArrayList<TaggedWord> tSentence) {
        String result = "";
        for (int w=0; w<tSentence.size(); w++) {
            String word = tSentence.get(w).word();
            result+= word + " ";
        }
        return result;
    }
    
}
