package xprolog;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.Enumeration;
import java.util.HashSet;
import java.util.Hashtable;
import java.util.Stack;

///////////////////////////////////////////////////////////////////////
public class KnowledgeBase
// /////////////////////////////////////////////////////////////////////
{
    Hashtable ht;

    HashSet primitives;

    String oldIndex;

    public KnowledgeBase() {
        reset();
    }

    public Object get(Object key) {
        return ht.get(key);
    }

    public void put(Object key, Object value) {
        ht.put(key, value);
    }

    public String toString() {
        return ht.toString();
    }

    public Enumeration elements() {
        return ht.elements();
    }

    public void reset() {
        ht = new Hashtable();
        primitives = new HashSet();
        oldIndex = "";
    }

    public void consult(String fName) throws ParseException, FileNotFoundException {
        oldIndex = "";
        new Parser(new FileReader(fName)).Program(this);
    }

    // ==========================================================
    public void addPrimitive(Clause clause)
    // ----------------------------------------------------------
    {
        Term term = clause.term;

        String index = term.getfunctor() + "/" + term.getarity();
        Clause c = (Clause) ht.get(index);
        if (c != null) {
            while (c.nextClause != null)
                c = c.nextClause;
            c.nextClause = clause;
        } else {
            primitives.add(index);
            ht.put(index, clause);
        }
    }

    public void addClause(Clause clause)
    // -----------------------------------------------------------
    {
        Term term = clause.term;

        String index = term.getfunctor() + "/" + term.getarity();
        if (primitives.contains(index)) {
            System.out.println("Trying to modify primitive predicate: " + index);
            return;
        }

        if (!oldIndex.equals(index)) {
            ht.remove(index);
            ht.put(index, clause);
            oldIndex = index;
        } else {

            Clause c = (Clause) ht.get(index);
            while (c.nextClause != null)
                c = c.nextClause;
            c.nextClause = clause;
        }
    }

    // ==========================================================
    public void assertTerm(Term term)
    // -----------------------------------------------------------------------
    {
        term = term.cleanUp();
        Clause newC = new Clause(term.deref(), null);

        String index = term.getfunctor() + "/" + term.getarity();
        if (primitives.contains(index)) {
            IO.error("Assert", "Trying to insert a primitive: " + index);
            return;
        }

        Clause c = (Clause) ht.get(index);
        if (c != null) {
            while (c.nextClause != null)
                c = c.nextClause;
            c.nextClause = newC;
        } else {
            ht.put(index, newC);
        }
    }

    // ==========================================================
    public void asserta(Term term)
    // -----------------------------------------------------------------------
    {
        String index = term.getfunctor() + "/" + term.getarity();
        if (primitives.contains(index)) {
            IO.error("Assert", "Trying to insert a primitive: " + index);
            return;
        }

        term = term.cleanUp();
        Clause newC = new Clause(term.deref(), null);
        Clause c = (Clause) ht.get(index);
        newC.nextClause = c;
        ht.put(index, newC);
    }

    // ==========================================================
    public boolean retract(Term term, Stack stack)
    // -----------------------------------------------------------------------
    {
        Clause newC = new Clause(term, null);
        String index = term.getfunctor() + "/" + term.getarity();
        if (primitives.contains(index)) {
            IO.error("Retract", "Trying to retract a primitive: " + index);
            return false;
        }
        Clause cc = null, c = (Clause) ht.get(index);

        while (c != null) {
            Term vars[] = new Term[Parser.maxVarnum];
            Term xxx = c.term.refresh(vars);
            int top = stack.size();
            if (xxx.unify(term, stack)) {
                if (cc != null)
                    cc.nextClause = c.nextClause;
                else if (c.nextClause == null)
                    ht.remove(index);
                else
                    ht.put(index, c.nextClause);
                return true;
            }
            for (int i = stack.size() - top; i > 0; i--) {
                Term t = (Term) stack.pop();
                t.unbind();
            }
            cc = c;
            c = c.nextClause;
        }
        return false;
    }

    // ==========================================================
    public boolean retractall(Term term, Term arity)
    // ----------------------------------------------------------
    {
        String key = term.getfunctor() + "/" + arity.getfunctor();
        if (primitives.contains(key)) {
            IO.error("Retractall", "Trying to retract a primitive: " + key);
            return false;
        }
        ht.remove(key);
        return true;
    }

    // ==========================================================
    public Term get(Term key)
    // ----------------------------------------------------------
    {
        return (Term) ht.get(key.toString());
    }

    // ==========================================================
    public void set(Term key, Term value)
    // ----------------------------------------------------------
    {
        ht.put(key.toString(), value.cleanUp());
    }

    // =======================================================

    public void dump() {
        dump(false);
    }

    public void dump(boolean full) {
        System.out.println();
        int i = 1;
        Enumeration e = ht.keys();
        while (e.hasMoreElements()) {
            Object key = e.nextElement();
            if (!full && primitives.contains(key))
                continue;
            Object val = ht.get(key);
            if (val instanceof Clause) {
                System.out.println(i++ + ". " + key + ": ");
                Clause head = (Clause) ht.get(key);
                do {
                    System.out.print("    " + head.term);
                    if (head.next != null)
                        System.out.print(" :- " + head.next);
                    System.out.println(".");
                    head = head.nextClause;
                } while (head != null);
            } else
                // get/set pair
                System.out.println(i++ + ". " + key + " = " + val);
        }
        System.out.println();
    }

    public void list(Term term, Term arity) {
        String key = term.getfunctor() + "/" + arity.getfunctor();
        System.out.println();
        System.out.println(key + ": ");
        Clause head = (Clause) ht.get(key);
        while (head != null) {
            System.out.print("    " + head.term);
            if (head.next != null)
                System.out.print(" :- " + head.next);
            System.out.println(".");
            head = head.nextClause;
        }
    }
}
