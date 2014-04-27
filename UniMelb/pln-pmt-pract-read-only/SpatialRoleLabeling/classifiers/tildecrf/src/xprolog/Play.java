package xprolog;

//  Play.java  :  Testbench to have two Prolog agents interacting
//  ================
//  Author: J. Vaucher (vaucher@iro.umontreal.ca)
//  Date: 2002/5/10
//  URL:  www.iro.umontreal.ca/~vaucher/~XProlog
//  ----------------------------------------------------------------------
//  Usage: java Play <KB for env> <KB for agent1> 
// 
//   The system first executes the query "init" in context of ENV
//   then queries user for AGENT queries
//   After doing each AGENT query, the system automatically executes
//    a "doTurn" on ENV

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintStream;

public class Play {
    static BufferedReader F = null;

    static public void main(String args[]) {
        PrintStream out = System.out;
        String query;
        long time = System.currentTimeMillis();

        System.out.println("\nXProlog v.1.2, May 2002");
        if (args.length < 2) {
            System.out.println("Usage: java Play robot_env.pro robot.pro ");
            System.exit(1);
        }
        try {
            F = new BufferedReader(new InputStreamReader(System.in));

            Engine env, ag1;
            env = new Engine(new FileReader(args[0]));
            ag1 = new Engine(new FileReader(args[1]));
            Term.trace = true;
            getAnswer(env, "init.");

            int i = 0;
            while (!ag1.fini && ++i < 65) {
                submit(ag1, "go.");
                submit(env, "go.");
            }
            getAnswer(ag1, "listing( [visited/2, contains/3]).");
        } catch (FileNotFoundException x) {
            System.out.println("Can't find: " + args[0]);
        } catch (Exception f) {
            f.printStackTrace();
        }
        System.out.println("Time: " + (System.currentTimeMillis() - time) + " ms.");
    }

    static String getQuery() {
        System.out.println();
        System.out.print("Agent ?- ");
        System.out.flush();
        try {
            return F.readLine();
        } catch (IOException e) {
            e.printStackTrace();
            return ".";
        }

    }

    static void getAnswer(Engine e, String query) {
        boolean res = false;
        try {
            res = e.setQuery(query);
        } catch (ParseException x) {
            System.out.println("Parsing Problem");
            x.printStackTrace();
        }
        if (res)
            System.out.println(">>> Answer: " + e.answer());
        else
            System.out.println("> No. ");
    }

    static boolean submit(Engine e, String query) {
        boolean res = false;
        try {
            res = e.setQuery(query);
        } catch (ParseException x) {
            System.out.println("Parsing Problem");
            x.printStackTrace();
        }
        return res;
    }
}
