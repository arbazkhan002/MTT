/**
 * 
 */
package xprolog;

import java.io.StringReader;

import org.apache.log4j.BasicConfigurator;

/**
 * @author bgutmann
 * 
 */
public class MyXprologTest {
    public static void main(String[] args) throws ParseException {
        BasicConfigurator.configure();

        /*
         * Engine eng = new Engine(new StringReader("f1(X):-seq(X,Y),X2 is
         * X+1,seq(X2,Y),X3 is X-1, seq(X3,Y).")); // Engine eng = new Engine(); //
         * eng.db.dump();
         * 
         * eng.setQuery("assert(seq(1,apf2l))");
         * eng.setQuery("assert(seq(2,ap2fel))");
         * eng.setQuery("assert(seq(3,apfel))");
         * eng.setQuery("assert(seq(4,apfel))");
         * eng.setQuery("assert(seq(5,birne))");
         * 
         * eng.setQuery("listing");
         */
        
        
        
        test3(); 
        //test2();
    }
    
    public static void test1() throws ParseException{

        Engine eng = new Engine(new StringReader(
                "small(K) :- K<4.big(K) :- K>1."));

      /*  eng.setQuery("assert(ex(1,1,5))");
        eng.setQuery("assert(ex(1,2,5))");
        eng.setQuery("assert(ex(1,3,5))");
        
        eng.setQuery("assert(ex(2,1,2))");
        eng.setQuery("assert(ex(2,2,3))");
        eng.setQuery("assert(ex(2,3,4))");
        
        eng.setQuery("assert(ex(3,1,4))");
        eng.setQuery("assert(ex(3,2,4))");
        eng.setQuery("assert(ex(3,3,2))");*/
        
        // eng.setQuery("trace");

        // eng.setQuery("assert(b(40))");

        //boolean res = eng.setQuery("member(Nr,[1,2,3]),ex(Nr,Pos,Value),not(small(Value)),big(Value)");
        boolean res = eng.setQuery(" member( Num, [1,2,3,5,7,8,22,17]), Num>4, Num<10.");
        System.out.println(res);
        // eng.solve();
        // System.out.println(eng.answer());

        if (res) {
            do {
                System.out.println();
                System.out.println(">>> Answer: " + eng.answer() + "   ( " + eng.getTime() + " ms.)");
            } while (eng.more());
        }
      
    }

     public static void test3() throws ParseException{

            Engine eng = new Engine(new StringReader("listsucceds([],Test,E):-succeds(Test,E)."+
                                                     "listsucceds([H|T],Test,E):-succeds(H,E),listsucceds(T,Test,E)."+
                                                     "test(sameY)."+
                                                     "test(outYis(Y)) :- member(Y,[class1,class2,class3])."+
                                                     "test(outYOldis(Y)) :- test(outYis(Y))." +
                                                     "succeds(sameY,head(_,Y,Y))."+
                                                     "succeds(outYis(Y),head(_,_,Y))."+
                                                     "succeds(outYOldis(Y),head(_,Y,_))." +
                                                     "positiveExample(TestsSoFar,Test,Nr):-example(Nr,Example),listsucceds(TestsSoFar,Test,Example)."));
            
            
            boolean res = eng.setQuery("trace,listsucceds([sameY,not(outYis(12))],outYis(11),head([],11,11))");
                                
            System.out.println(res);
            if (res) {
                do {
                    System.out.println();
                    System.out.println(">>> Answer: " + eng.answer().term + "   ( " + eng.getTime() + " ms.)");
                } while (eng.more());
            }
          
        }
            
    
    public static void test2() throws ParseException{

        Engine eng = new Engine(new StringReader(
                "intervall(K) :- K!=0,K>0-4,K<4. f(N) :- seq(N,X),seq(N2,X), intervall(N-N2)."));

        eng.setQuery("assert(seq(1,a))");
        eng.setQuery("assert(seq(2,b))");
        eng.setQuery("assert(seq(3,c))");
        eng.setQuery("assert(seq(4,d))");
        eng.setQuery("assert(seq(5,b))");
        // eng.setQuery("trace");

        // eng.setQuery("assert(b(40))");

        boolean res = eng.setQuery("f(X)");
        System.out.println(res);
        // eng.solve();
        // System.out.println(eng.answer());

        if (res) {
            do {
                System.out.println();
                System.out.println(">>> Answer: " + eng.answer() + "   ( " + eng.getTime() + " ms.)");
            } while (eng.more());
        }
      
    }


}
