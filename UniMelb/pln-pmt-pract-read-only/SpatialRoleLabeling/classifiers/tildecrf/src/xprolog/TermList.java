/**
 * 
 */
package xprolog;

/**
 * @author bgutmann
 * 
 */
// /////////////////////////////////////////////////////////////////////
public class TermList
// /////////////////////////////////////////////////////////////////////
{
    public Term term;

    public TermList next = null;

    public Clause nextClause; // serves 2 purposes: either links clauses in database

    // or points to defining clause for goals

    public TermList() {} // for Clause

    public TermList(Term t) {
        term = t;
    }

    public TermList(Term t, TermList n) {
        term = t;
        next = n;
    }

    public String toString() {
        int i = 0;
        String s;
        TermList tl;
        s = new String("[" + term.toString());
        tl = next;
        while (tl != null && ++i < 3) {
            s = s + ", " + tl.term.toString();
            tl = tl.next;
        }
        if (tl != null)
            s += ",....";
        s += "]";

        return s;
    }

    public void resolve(KnowledgeBase db) {
        nextClause = (Clause) db.get(term.getfunctor() + "/" + term.getarity());
    }

    public void lookupIn(KnowledgeBase db) {
        nextClause = (Clause) db.get(term.getfunctor() + "/" + term.getarity());
    }

}