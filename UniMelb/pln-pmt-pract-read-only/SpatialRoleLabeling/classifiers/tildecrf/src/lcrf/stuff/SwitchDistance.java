/**
 * 
 */
package lcrf.stuff;

import java.util.List;
import java.util.Vector;

import lcrf.logic.Atom;
import lcrf.logic.Constant;
import lcrf.logic.NumberConstant;
import lcrf.logic.Term;

/**
 * @author Bernd Gutmann
 * 
 */
public class SwitchDistance {

    public static int switchDistance(List<Atom> p, List<Atom> q) {
        assert p != null;
        assert q != null;
        assert p.size() == q.size();

        Vector<Term> p1 = new Vector<Term>(p.size());
        Vector<Term> p2 = new Vector<Term>(p.size());
        Vector<Term> q1 = new Vector<Term>(q.size());
        Vector<Term> q2 = new Vector<Term>(q.size());

        for (Atom a : p) {
            assert a != null;
            assert a.getTermRepresentation() instanceof Constant;

            Constant c = (Constant) a.getTermRepresentation();

            assert c.getName().equals("o");
            assert c.hasSubterms();
            assert c.getSubterms().size() == 2;
            assert c.getSubterms().get(0) instanceof NumberConstant;
            assert c.getSubterms().get(1) instanceof NumberConstant;

            p1.add(c.getSubterms().get(0));
            p2.add(c.getSubterms().get(1));
        }

        for (Atom a : q) {
            assert a != null;
            assert a.getTermRepresentation() instanceof Constant;

            Constant c = (Constant) a.getTermRepresentation();

            assert c.getName().equals("o");
            assert c.hasSubterms();
            assert c.getSubterms().size() == 2;
            assert c.getSubterms().get(0) instanceof NumberConstant;
            assert c.getSubterms().get(1) instanceof NumberConstant;

            q1.add(c.getSubterms().get(0));
            q2.add(c.getSubterms().get(1));
        }

        return switchDistance(p1, p2, q1, q2);
    }

    private static int switchDistance(List<Term> p1, List<Term> p2, List<Term> q1, List<Term> q2) {
        assert p1.size() == p2.size();
        assert q1.size() == q2.size();
        assert p1.size() == q1.size();

        if (p1.size() == 0) {
            return 0;
        } else {
            if (p1.get(0).equals(q1.get(0)) && (p2.get(0).equals(q2.get(0)))) {
                // match, look at rest
                return switchDistance(p1.subList(1, p1.size()), p2.subList(1, p2.size()), q1.subList(1, q1
                        .size()), q2.subList(1, q2.size()));
            } else {
                // mismatch, switch rest and count error
                return switchDistance(p2.subList(1, p2.size()), p1.subList(1, p1.size()), q1.subList(1, q1
                        .size()), q2.subList(1, q2.size())) + 1;
            }
        }
    }

}
