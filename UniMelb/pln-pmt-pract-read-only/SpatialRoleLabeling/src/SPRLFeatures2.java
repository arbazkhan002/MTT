
import java.util.HashMap;
import java.util.Map;

/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author Matias
 */
public class SPRLFeatures2 {

    private Map<String, Object> f1;
    private Map<String, Object> f2;
    private Map<String, Object> f3;
    public SPRLFeatures2() {
        f1 = new HashMap<String, Object>();
        f2 = new HashMap<String, Object>();
        f3 = new HashMap<String, Object>();
    }
    
    public Map<String, Object> getF1() { return f1; }
    public Map<String, Object> getF2() { return f2; }
    public Map<String, Object> getF3() { return f3; }
    public void putF1(String name, Object value) { f1.put(name, value); }
    public void putF2(String name, Object value) { f2.put(name, value); }
    public void putF3(String name, Object value) { f3.put(name, value); }
    
}
