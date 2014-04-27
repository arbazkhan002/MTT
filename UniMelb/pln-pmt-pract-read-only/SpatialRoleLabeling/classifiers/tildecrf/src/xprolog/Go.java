package xprolog;

// A simple program which interfaces to the XProlog engine.
// Author: J. Vaucher
// Author: Michael Winikoff (winikoff@cs.mu.oz.au)
// Date: 6/3/97
//
// Usage: java Go util.pro
// 
// 

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.InputStreamReader;
import java.io.PrintStream;

public class Go {
    static public void main(String args[]) {
        BufferedReader F;
        PrintStream out = System.out;
        String program;
        String query;

        try {
            F = new BufferedReader(new InputStreamReader(System.in));

            Engine eng;

            if (args.length == 0)
                eng = new Engine();
            else
                eng = new Engine(new FileReader(args[0]));

            System.out.println("\n" + XProlog.VERSION);

            while (!eng.fini)
                try {
                    System.out.println();
                    System.out.print("?- ");
                    System.out.flush();
                    query = F.readLine();

                    boolean res = eng.setQuery(query);
                    while (!eng.fini) {
                        if (!res) {
                            System.out.println("> No. ");
                            break;
                        }
                        System.out.println();
                        System.out.println(">>> Answer: " + eng.answer() + "   ( " + eng.getTime() + " ms.)");
                        out.print("More (y/n)? ");
                        out.flush();
                        String ans = F.readLine().trim();
                        if (ans.equals("y") | ans.equals(";")) {
                            res = eng.more();
                        } else
                            break;
                    }
                } catch (ParseException x) {
                    System.out.println("Parsing Problem");
                    x.printStackTrace();
                } catch (TokenMgrError x) {
                    System.out.println("Token Manager Problem");
                    x.printStackTrace();
                }

        } catch (FileNotFoundException x) {
            System.out.println("Can't find: " + args[0]);
        } catch (Exception f) {
            f.printStackTrace();
        }
    }

}
