/**
 * 
 */
package xprolog;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;
import java.io.StringReader;
import java.util.LinkedList;
import java.util.Stack;

/**
 * An engine is what executes prolog queries.
 * 
 * @author Michael Winikoff
 */

final public class Engine extends Thread {
    public boolean fini = false;

    Parser parser;

    LinkedList inq = new LinkedList();

    /**
     * The stack holds choicepoints and a list of variables which need to be
     * un-bound upon backtracking.
     */
    private Stack stack;

    int agent_id = 0;

    /** We use a KnowledgeBase to store the program */

    private KnowledgeBase db;

    private TermList goal_list;

    private TermList call;

    /** This governs whether tracing is done */
    public boolean trace = false;

    public boolean stepFlag = false;

    /** Used to time how long queries take */
    private long time;

    /**
     * Variables to handle backtrackable "retract" without growing the stack
     */

    private Clause retractClause;

    private ChoicePoint cp;

    // ------------------------ Enquiry Methods -------------------

    public TermList answer() {
        return call;
    }

    public long getTime() {
        return System.currentTimeMillis() - time;
    }

    // ------------------------------------------------------------
    public Engine() throws ParseException
    // ------------------------------------------------------------
    {
        agent_id = PostOffice.register(inq);
        db = new KnowledgeBase();

        parser = new Parser(new StringReader(

        "    !      := 1. " + "call(X)    := 2 ." + "fail       := 3 ." + "consult(X) := 4 ."
                + "assert(X)  := 5 ." + "asserta(X) := 6 ." + "retract(X) := 7 . retract(X) :- retract(X)."
                // + "retractall(X/Y) := 29 ."

                + "listing    := 8 ." + "listing(X/Y) := 9 ." + "listing([])."
                + "listing([A|Tail]):- listing(A), listing(Tail)." + "print(X)   := 10 ."
                + "println(X) := 11." + "nl       := 12." + "trace    := 13." + "notrace  := 13."
                + "step     := 14." + "nostep   := 14." + "X is Y   := 15." + "X > Y    := 16."
                + "X < Y    := 17." + "X == Y   := 18." + "X >= Y   := 19." + "X <= Y   := 20."
                + "X != Y   := 21." + "quit     := 22." + "var(C)   := 23." + "self(S)  := 24."
                + "send(D,M)    := 25." + "shout(M)     := 26." + "broadcast(M) := 26."
                + "receive(S,M) := 27." + "dumpQ        := 28."

                + "retractall(X/Y) := 29 ." + "seq(X)        := 30 ."

                + "set(X,Y)      := 31 ." + "get(X,Y)      := 32 ." + "gensym(X)     := 33 ."

                + "X=X.  eq(X,X). true." + "not(X) :- X, !, fail.  not(X). "
                + "if(X, Yes, _ ) :- seq(X), !, seq(Yes)." + "if(X, _  , No) :- seq(No)."
                + "if(X, Yes) :- seq(X), !, seq(Yes)." + "if(X, _  )."
                + "or(X,Y) :- seq(X). or(X,Y) :- seq(Y)." + "once(X) :- X , !."
                
                //added to get some more comfort
                + "append([],L,L). append([A|B],L,[A|Tail]) :- append(B,L,Tail)."
                + "member(X,[X|_]). member(X,[_|Y]) :- member(X,Y)."
                + "length([],0). length([_|Rest],L2):- length(Rest,L), L2 is L+1."
                + "add(X) :- X,!. add(X) :- assert(X)."
                + "nth0(_,[],_) :- !,fail. nth0(0,[H|_],H) :- !. nth0(N,[_|T],H) :- N2 is N-1,nth0(N2,T,H)."
                + "nth(_,[],_) :- !,fail. nth(1,[H|_],H) :- !. nth(N,[_|T],H) :- N2 is N-1,nth0(N2,T,H)." ));

        parser.primitives(db);

        stack = new Stack();
        retractClause = (Clause) db.get("retract/1");

        setPriority(2);

    }

    public Engine(String pgm) throws ParseException {
        this();
        // Parser.ReInit( new StringReader( pgm ));
        // Parser.Program( db );
        new Parser(new StringReader(pgm)).Program(db);
    }

    public Engine(Reader file) throws ParseException {
        this();
        // Parser.ReInit( file );
        // Parser.Program( db );
        new Parser(file).Program(db);
    }

    public void consult(String fName) throws ParseException {
        try {
            new Parser(new FileReader(fName)).Program(db);
        } catch (FileNotFoundException e) {
            IO.fatalerror("consult", fName + " NOT Found!");
        }
        // db.dump();
    }

    public boolean setQuery(String query) throws ParseException {
        // goal_list = Parser.getList( query );
        goal_list = parser.getList(query);
        call = goal_list;
        goal_list.resolve(db);
        stack.clear();
        return solve();
    }

    final public void run() {
        solve();
    }

    // int stackTop = 0;

    /** run does the actual work. */
    final public boolean solve() {
        Stack stack2 = new Stack();
        int stackTop = 0;

        String func;
        int arity;
        TermList clause = null, nextclause;
        Term vars[] = null;

        time = System.currentTimeMillis();

        while (true) {
            stackTop = stack.size();

            if (goal_list instanceof Step) {
                goal_list = goal_list.next;
                if (goal_list != null)
                    goal_list.lookupIn(db);
                stepFlag = trace = true;
            }
            if (trace) {
                // System.out.println("\nSTACK: " + stack);
                dumpGoal();
            }
            if (stepFlag)
                step();

            if (goal_list == null) {
                return true;
            }

            if (goal_list.term == null) {
                IO.fatalerror("Engine.run", "goal.term is null!");
            }

            func = goal_list.term.getfunctor();
            arity = goal_list.term.getarity(); // is this needed?

            if (goal_list.nextClause == null) {
                if (trace)
                    IO.diagnostic(goal_list.term.getfunctor() + "/" + goal_list.term.getarity()
                            + " undefined!");
                if (!backtrack())
                    return false;
                else
                    continue;
            }

            clause = goal_list.nextClause;
            if (clause.nextClause != null)
                stack.push(cp = new ChoicePoint(goal_list, clause.nextClause));

            vars = new Term[Parser.maxVarnum];
            Term xxx = clause.term.refresh(vars);

            if (xxx.unify(goal_list.term, stack)) {
                clause = clause.next;

                if (clause instanceof Primitive) {
                    if (!doPrimitive(goal_list.term, clause) && !backtrack())
                        return false;
                } else if (clause == null) // matching against fact ...
                {
                    goal_list = goal_list.next;
                    if (goal_list != null)
                        goal_list.lookupIn(db);
                }

                else // replace goal by clause body
                {
                    TermList p, p1 = null, ptail = null;

                    for (int i = 1; clause != null; i++) {
                        if (clause.term == Term.CUT)
                            p = new TermList(new Cut(stackTop));
                        else
                            p = new TermList(clause.term.refresh(vars));
                        if (i == 1)
                            p1 = ptail = p;
                        else {
                            ptail.next = p;
                            ptail = p;
                        }
                        clause = clause.next;
                    }
                    // System.out.println("Refreshed clause: " + p1);
                    ptail.next = goal_list.next;
                    goal_list = p1;
                    goal_list.lookupIn(db);
                }
            }

            else { // unify failed - backtrack ...

                if (!backtrack()) {
                    return false;
                }
            }

        } // while
    } // run

    boolean backtrack() // returns TRUE if choice point was found
    {
        Object o;
        ChoicePoint cp;
        Term t;
        boolean found = false;

        if (trace)
            System.out.println(" <<== Backtrack: ");
        while (!stack.empty()) {
            o = stack.pop(); // System.out.println(" Pop: " + o);

            if (o instanceof Term) {
                t = (Term) o;
                t.unbind();
            } else if (o instanceof ChoicePoint) {
                cp = (ChoicePoint) o;
                goal_list = cp.goal;
                goal_list.nextClause = cp.clause;
                found = true;
                // System.out.println(" CP: " + cp);
                break;
            }
        }
        return found;
    }

    /*
     * --------------------------------------------------------------------
     * Primitives: 1: cut 2: call 3: fail 4: consult 5: assert 6: asserta 7:
     * retract 8: listing 9: listing(full) or listing( <functor>/<arity> ) 10:
     * print 11: println etc...
     */

    static int gensymInt = 0;

    boolean doPrimitive(Term term, TermList c) // returns false if FAIL
    {
        // Primitive p = (Primitive) c;
        Term t2;

        switch (((Primitive) c).ID) {
        case 1: // CUT
            removeChoices(term.varid);
            break;

        case 2: // call
            goal_list = new TermList(term.getarg(0), goal_list.next);
            goal_list.resolve(db);
            return true;

        case 3: // fail
            return false;

        case 4: // consult
            String fName = term.getarg(0).getfunctor();
            try {
                db.consult(fName);
                break;
            } catch (FileNotFoundException e) {
                IO.fatalerror("consult", fName + " NOT Found!");
                return false;
            } catch (ParseException e) {
                IO.error("Consult", "parseException");
                return false;
            }

        case 5: // assert
            db.assertTerm(term.getarg(0));
            break;

        case 6: // asserta
            db.asserta(term.getarg(0));
            break;

        case 7: // retract
            boolean r = db.retract(term.getarg(0), stack);
            if (!r) {
                backtrack();
                return false;
            } else
                cp.clause = retractClause;
            break;

        case 29: // retractall
            t2 = term.getarg(0);
            if (t2.getfunctor().equals("/") && t2.getarity() == 2) {
                db.retractall(t2.getarg(0), t2.getarg(1));
            } else
                return false;
            break;

        case 8: // listing
            db.dump(false);
            break;

        case 9: // listing(Term)
            t2 = term.getarg(0);
            if (t2.getfunctor().equals("/") && t2.getarity() == 2) {
                db.list(t2.getarg(0), t2.getarg(1));
            } else
                db.dump(true);
            break;

        case 10: // print
            IO.prologprint(term.getarg(0).toString());
            break;

        case 11: // println
            IO.prologprint(term.getarg(0).toString() + "\n");
            break;

        case 12: // nl
            IO.prologprint("\n");
            break;

        case 13: // trace
            trace = term.getfunctor().equals("trace");
            ;
            System.out.println("Trace " + (trace ? "ON" : "OFF"));
            break;

        case 14: // step
            stepFlag = term.getfunctor().equals("step");
            trace = stepFlag;
            System.out.println(" => Step: " + (stepFlag ? "ON" : "OFF"));
            break;

        case 15: // is
            Term rhs = term.getarg(0).deref();
            int lhs = term.getarg(1).value();
            if (rhs.isBound())
                return false;
            rhs.bind(new Number(lhs));
            stack.push(rhs);
            break;

        case 16: // >
            if (term.getarg(0).value() > term.getarg(1).value())
                break;
            return false;

        case 17: // <
            if (term.getarg(0).value() < term.getarg(1).value())
                break;
            return false;

        case 18: // ==
            if (term.getarg(0).value() == term.getarg(1).value())
                break;
            return false;

        case 19: // >=
            if (term.getarg(0).value() >= term.getarg(1).value())
                break;
            return false;

        case 20: // <=
            if (term.getarg(0).value() <= term.getarg(1).value())
                break;
            return false;

        case 21: // !=
            if (term.getarg(0).value() != term.getarg(1).value())
                break;
            return false;

        case 22: // quit
            fini = true;
            break;

        case 23: // var
            // System.out.println( "Term: " + term.getarg(0));
            if (term.getarg(0).bound())
                return false;
            break;

        case 24: // self
            lhs = agent_id;
            rhs = term.getarg(0);
            if (rhs.isBound())
                return false;
            rhs.bind(new Number(lhs));
            stack.push(rhs);
            break;

        case 25: // send(D,M)
            Term a1 = term.getarg(0).deref();
            Term a2 = term.getarg(1);

            if (!(a1 instanceof Number))
                return false;
            PostOffice.send(agent_id, a1.value(), a2.cleanUp());
            break;

        case 26: // broadcast( Msg )
            PostOffice.broadcast(agent_id, term.getarg(0).cleanUp());
            break;

        case 27: // receive( Src, Msg)
            if (inq.size() < 1)
                return false; // Empty queue -> fail
            Message m = (Message) inq.removeFirst();
            a1 = term.getarg(0);
            a2 = term.getarg(1);

            if (a1.unify(new Number(m.source), stack) && a2.unify(m.content, stack))
                break;
            return false;

        case 28: // dumpq

            System.out.println("INQ:" + inq + " ");
            break;

        case 30: // seq( <list> )

            splice_goal_list(term);
            return true;

        case 31: // set(X,Y)
            db.set(term.getarg(0), term.getarg(1));
            break;

        case 32: // get(X)

            t2 = (Term) db.get(term.getarg(0));

            if (t2 == null)
                return false;

            Term xxx = t2.refresh(new Term[Parser.maxVarnum]);

            if (xxx.unify(term.getarg(1), stack))
                break;
            return false;

        case 33: // gensym(X)

            t2 = new Term("v" + gensymInt++, 0);

            if (t2.unify(term.getarg(0), stack))
                break;
            else
                return false;

        default:
            IO.diagnostic("Unknown builtin: " + term);
            return false;
        }
        goal_list = goal_list.next;
        if (goal_list != null)
            goal_list.lookupIn(db);
        return true;
    }

    void removeChoices(int n) {
        Object o;
        Stack stack2 = new Stack();
        int i = stack.size();
        while (i > n) {
            o = stack.pop();
            if (!(o instanceof ChoicePoint))
                stack2.push(o);
            i--;
        }
        while (!(stack2.empty()))
            stack.push(stack2.pop());
    }

    // --------------------------------------------------
    void splice_goal_list(Term term)
    // --------------------------------------------------
    {
        Term t2;
        TermList p, p1 = null, ptail = null;
        // Term vars[] = new Term[ Parser.maxVarnum ];
        int i = 0;

        term = term.getarg(0);
        while (term.getfunctor() != "null") {
            t2 = term.getarg(0);
            if (t2 == Term.CUT)
                p = new TermList(new Cut(stack.size()));
            else
                // p = new TermList( t2.refresh(vars));
                p = new TermList(t2);
            if (i++ == 0)
                p1 = ptail = p;
            else {
                ptail.next = p;
                ptail = p;
            }
            term = term.getarg(1);
        }

        ptail.next = goal_list.next;
        goal_list = p1;
        goal_list.lookupIn(db);
    }

    void dumpGoal() {
        System.out.println();
        System.out.println("= Goals: " + goal_list);
        if (goal_list != null) {
            System.out.println("==> Try:  " + goal_list.nextClause);
        }
    }

    /**
     * Used from the GUI when the user hits <em>more</em>. All it does is add
     * <tt>fail</tt> to the goal and lets the engine do the rest.
     */

    final public boolean more() {
        time = System.currentTimeMillis();
        if (!backtrack())
            return false;
        return solve();
    }

    BufferedReader MoreF = null;

    void step() {
        System.out.print("More:");
        System.out.flush();
        BufferedReader F;
        try {
            if (MoreF == null)
                MoreF = new BufferedReader(new InputStreamReader(System.in));
            String s = MoreF.readLine().trim();
            if (s.equals(""))
                return;
            else if (s.equals("q"))
                stepFlag = false;
            else if (s.trim().equals("s")) {
                stepFlag = false;
                trace = false;
                new Step(goal_list);
            } else if (s.trim().equals("a")) {
                goal_list = null;
                stepFlag = trace = false;
            } else {
                System.out.println("   <CR>, 'q': Quit, 's': Skip, 'a': Abort");
                step();
            }
        } catch (IOException e) {
        }
    }
    
    
    /**
     * Retract all atom from the database that unify with <pre>atom</pre>.
     * @param atom an atom in Prolog notation
     */
    public void retractAll(String atom) {
        try{
            if (setQuery("retract("+atom+")")) {
                do {                
                } while (more());
            }
        }catch(ParseException e) {
                throw new RuntimeException(e);
        }
    }

} // //////////////////////// Engine //////////////////////////////
