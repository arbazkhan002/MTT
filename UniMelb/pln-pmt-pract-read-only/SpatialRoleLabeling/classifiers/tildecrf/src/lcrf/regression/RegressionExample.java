/**
 * 
 */
package lcrf.regression;

/**
 * @author bgutmann
 * 
 */
public class RegressionExample<T> {
    public double weight;
    
    public double value;

    public T content;

    public Object auxObject;

    public RegressionExample(T content, double value) {
        this.value = value;
        this.content = content;
        this.auxObject = null;
        
        this.weight = 1.0d;
    }

    public String toString() {
        return content.toString() + " : " + value;
    }

}
