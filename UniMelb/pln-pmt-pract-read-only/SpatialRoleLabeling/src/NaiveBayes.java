
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;

/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author Bogdan
 */
public class NaiveBayes {
    protected List<Map<String, Object>> instances;
    protected List<String> classes;
    protected List<String> possibleClasses;
    protected List<String> attributes;
    public NaiveBayes(String[] classes, String[] attributes){
        this.possibleClasses = Arrays.asList(classes);
        this.classes = new ArrayList<String>();
        this.attributes = Arrays.asList(attributes);
        this.instances = new ArrayList<Map<String, Object>>();
    }
    public void learn(Map<String, Object> instance, String cls){
        classes.add(cls);
        instances.add(instance);
    }
    public String classify(Map<String, Object> instance){
        double maxProbability = 0.0;
        String maxClass = "";
        for(int i = 0; i < classes.size(); i++){
            double currentProbability = 1.0;
            String currentClass = classes.get(i);
            for(int j = 0; j < attributes.size(); j++){
                String attrName = attributes.get(j);
                if(!instance.containsKey(attrName)){
                    currentProbability *= probability(attrName, null, currentClass)+(0.1/((double)instances.size()));
                } else {
                    currentProbability *= probability(attrName, instance.get(attrName), currentClass)+(0.1/((double)instances.size()));
                }
            }
            if(currentProbability > maxProbability){
                maxProbability = currentProbability;
                maxClass = currentClass;
            }
        }
        System.err.println("class: "+maxClass+" probability: "+maxProbability);
        return maxClass;
    }
    
    protected double probability(String attr, Object value, String cls){
        long noInstances = 0;
        for(int i = 0; i < instances.size(); i++){
            if(value == null){
                if(classes.get(i).equals(cls) && !instances.get(i).containsKey(attr)){
                    noInstances++;
                }
            } else {
                if(classes.get(i).equals(cls) && instances.get(i).containsKey(attr) && instances.get(i).get(attr).equals(value)){
                    noInstances++;
                }
            }
        }
        
        return (((double)noInstances)/((double)classes.size()));
    }
}
