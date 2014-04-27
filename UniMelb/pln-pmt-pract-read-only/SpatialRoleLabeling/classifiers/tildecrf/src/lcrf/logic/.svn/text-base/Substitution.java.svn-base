package lcrf.logic;

import java.util.List;
import java.util.Vector;

/**
 * @author Bernd Gutmann
 * 
 */
public class Substitution {
    public Variable head;

    public Term body;

    public Substitution(Variable head, Term body) {
        if (head == null || body == null)
            throw new IllegalArgumentException();

        this.head = head;
        this.body = body;
    }

    public Term apply(Term t2) {
        assert t2 != null;

        if (!t2.containsVariable(head)) {
            return t2;
        }

        if (t2 instanceof Variable) {
            return (t2.equals(head)) ? body : t2;
        }

        assert t2 instanceof Constant;

        Constant c2 = (Constant) t2;
        List<Term> c2_subterms = c2.getSubterms();
        Vector<Term> subterms = new Vector<Term>(c2.getSubterms().size());
        for (int i = 0; i < c2.getSubterms().size(); i++) {
            subterms.add(i, apply(c2_subterms.get(i)));
        }
        Constant c3 = new Constant(c2.getName(), subterms);

        return c3;
    }

    public boolean equals(Object anObject) {
        if (anObject == this) {
            return true;
        }

        if (anObject instanceof Substitution) {
            Substitution s2 = (Substitution) anObject;
            return this.head.equals(s2.head) && this.body.equals(s2.body);
        }

        return false;
    }

    public int hashCode() {
        return head.hashCode() * 1024 + body.hashCode();
    }

    public String toString() {
        return head + "<-" + body;
    }

}
