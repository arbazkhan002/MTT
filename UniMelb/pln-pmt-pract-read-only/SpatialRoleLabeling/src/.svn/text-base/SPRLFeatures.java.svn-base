
import edu.stanford.nlp.ling.TaggedWord;
import edu.stanford.nlp.trees.TypedDependency;
import java.util.*;

/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author Matias
 */
public class SPRLFeatures {
    private Map<String, Object> f1;
    private Map<String, Object> f2;
    private Map<String, Object> f3;
    public SPRLFeatures() {
        f1 = new HashMap<String, Object>();
        f2 = new HashMap<String, Object>();
        f3 = new HashMap<String, Object>();
    }
    
    public Map<String, Object> getF1() { return f1; }
    public Map<String, Object> getF2() { return f2; }
    public Map<String, Object> getF3() { return f3; }

    //Method to find the F1 positive instances
    void findF1pos(int w, 
                ArrayList<TaggedWord> tSentence,
                List<TypedDependency> tdl
                ) {
        
        f1.put("WORD_FORM", tSentence.get(w).word());
        f1.put("WORD_POS", tSentence.get(w).tag());
        //Dependency with the head on syntactic tree
        Iterator<TypedDependency> itdl = tdl.iterator();
        while(itdl.hasNext()) {
            //Obtain here the DPRL
            String dprl = itdl.next().dep().nodeString();
            if(dprl.equals(tSentence.get(w).word())) {
                f1.put("WORD_DPRL", dprl);
                break;
            }
        }

        //System.out.println(tSentence);
        //System.out.println(tdl);
        //System.out.println("tSentence: " + tSentence.size());
        //System.out.println("tdl: " + tdl.size());
            
    }
    
    //Method to find the F1 negative instances
    void findF1neg() {
        //TODO
    }
    
    //Method to find the F2 positive instances
    void findF2pos(int k,
                List<String> sentenceSpatialIndicators,
                List<Integer> sentenceSpatialIndicatorsIndex,
                List<Integer> sentenceSpatialIndicatorsWordCount,
                List<String> listHeadWordsPOS,
                Stemmer stemmer, 
                ArrayList<TaggedWord> tSentence
                ) {
        
        f2.clear();
        f2.put("SPATIAL_INDICATOR", sentenceSpatialIndicators.get(k));
        f2.put("SPATIAL_INDICATOR_LEMMA", stemmer.stem(sentenceSpatialIndicators.get(k)));
        f2.put("SPATIAL_INDICATOR_POS", tSentence.get(sentenceSpatialIndicatorsIndex.get(k)).tag());
        for(int idx = sentenceSpatialIndicatorsIndex.get(k)-1; idx >=0; idx--){
            //HEAD1 features, searches to the left part
            if(listHeadWordsPOS.contains(tSentence.get(idx).tag())){
                f2.put("HEAD1", tSentence.get(idx).word());
                f2.put("HEAD1_POS", tSentence.get(idx).tag());                                                        
                f2.put("HEAD1_LEMMA", stemmer.stem(tSentence.get(idx).word()));
                break;
            }
        }
        for(int idx = sentenceSpatialIndicatorsIndex.get(k)+sentenceSpatialIndicatorsWordCount.get(k); idx < tSentence.size(); idx++){
            //HEAD2 features, searches to the right part
            if(listHeadWordsPOS.contains(tSentence.get(idx).tag())){
                f2.put("HEAD2", tSentence.get(idx).word());
                f2.put("HEAD2_POS", tSentence.get(idx).tag());                            
                f2.put("HEAD2_LEMMA", stemmer.stem(tSentence.get(idx).word()));
                break;
            }
        }        
    }

    //Method to find the F2 negative instances
    void findF2neg(int k,
                int idx,
                List<List<String>> possibleSpatialIndicators,
                List<String> listHeadWordsPOS,
                Stemmer stemmer,
                ArrayList<TaggedWord> tSentence
                ) {
              
        f2.clear();
        f2.put("SPATIAL_INDICATOR", join(possibleSpatialIndicators.get(k)," "));
        f2.put("SPATIAL_INDICATOR_LEMMA", stemmer.stem(join(possibleSpatialIndicators.get(k)," ")));
        f2.put("SPATIAL_INDICATOR_POS", tSentence.get(idx).tag());
        for(int idxx = idx-1; idxx >=0; idxx--){
            if(listHeadWordsPOS.contains(tSentence.get(idxx).tag())){
                f2.put("HEAD1", tSentence.get(idxx).word());
                f2.put("HEAD1_POS", tSentence.get(idxx).tag());                                                        
                f2.put("HEAD1_LEMMA", stemmer.stem(tSentence.get(idxx).word()));
                break;
            }
        }
        for(int idxx = idx+possibleSpatialIndicators.get(k).size(); idxx < tSentence.size(); idxx++){
            if(listHeadWordsPOS.contains(tSentence.get(idxx).tag())){
                f2.put("HEAD2", tSentence.get(idxx).word());
                f2.put("HEAD2_POS", tSentence.get(idxx).tag());                            
                f2.put("HEAD2_LEMMA", stemmer.stem(tSentence.get(idxx).word()));
                break;
            }
        }
    }
    
    //Method to find the F3 positive instances
    void findF3pos() {
        //TODO
        //f3 : Relation features between w and SI (k)
        //TODO: PATH
        //TODO: Binary linear position of w respect SI (k)
        //TODO: Distance??
    }
    
    //Method to find the F3 negative instances
    void findF3neg() {
        //TODO
    }
    
    public static String join(Collection s, String delimiter) {
        StringBuffer buffer = new StringBuffer();
        Iterator iter = s.iterator();
        while (iter.hasNext()) {
            buffer.append(iter.next());
            if (iter.hasNext()) {
                buffer.append(delimiter);
            }
        }
        return buffer.toString();
    }

}
