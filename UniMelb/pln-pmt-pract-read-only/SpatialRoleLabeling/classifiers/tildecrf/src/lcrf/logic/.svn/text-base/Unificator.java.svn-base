package lcrf.logic;

import java.util.HashMap;
import java.util.Hashtable;
import java.util.List;
import java.util.Stack;

/**
 * @author Bernd Gutmann
 */
public class Unificator {
    private static final Hashtable<Term, HashMap<Term, Substitutions>> hashtable = new Hashtable<Term, HashMap<Term, Substitutions>>(
            20000, 0.50f);

    /**
     * 
     * @param atoms
     * @param job
     * @param subst
     * @return
     */
    public static Substitutions findMGU(List<Atom> atoms, UnificationJob job, Substitutions subst) {
        assert atoms != null;
        assert job != null;
        assert job.getPosition() < atoms.size();
        assert subst != null;

        return findMGU(atoms.get(job.getPosition()).getTermRepresentation(), subst.apply(job.getTerm()),
                subst);
    }

    /**
     * 
     * @param atoms
     * @param jobs
     * @param newjob
     * @return
     */

    public static Substitutions findMGU(List<Atom> atoms, List<UnificationJob> jobs, UnificationJob newjob) {
        assert atoms != null;
        assert jobs != null;
        Substitutions mgu = Unificator.findMGU(atoms, jobs);
        if (mgu == null) {
            return null;
        }
        return findMGU(mgu.apply(atoms.get(newjob.getPosition()).getTermRepresentation()), mgu.apply(newjob
                .getTerm()), mgu);
    }

    /**
     * 
     * @param atoms
     * @param jobs
     * @return
     */

    public static Substitutions findMGU(List<Atom> atoms, List<UnificationJob> jobs) {
        assert atoms != null;
        assert jobs != null;
        Substitutions mgu = new Substitutions();

        for (UnificationJob job : jobs) {
            if (job.getPosition() < 0 || job.getPosition() >= atoms.size()) {
                throw new ArrayIndexOutOfBoundsException(job.getPosition());
            }
            mgu = findMGU(mgu.apply(atoms.get(job.getPosition()).getTermRepresentation()), mgu.apply(job
                    .getTerm()), mgu);
            if (mgu == null) {
                return null;
            }
        }
        return mgu;
    }

    /**
     * 
     * @param t1
     * @param t2
     * @return
     */
    public static Substitutions findMGU(Term t1, Term t2) {
        assert t1 != null;
        assert t2 != null;

        return findMGU(t1, t2, new Substitutions());
    }

    /**
     * return a substituition if t1 is more general than t2, null otherwise
     * 
     * @param t1
     * @param t2
     * @return
     */
    public static Substitutions findSpecialisation(Term t1, Term t2, Substitutions substs) {
        assert t1 != null;
        assert t2 != null;
        assert substs != null;

        // terms are equal, there is nothing to do
        if (t1.equals(t2)) {
            return substs;
        }

        // terms are not equal, and cannot be unified
        if (!t1.hasVariables()) {
            return null;
        }

        Stack<Term> stack1 = new Stack<Term>();
        Stack<Term> stack2 = new Stack<Term>();

        stack1.push(t1);
        stack2.push(t2);

        while (!stack1.empty()) {
            Term left = stack1.pop();
            Term right = stack2.pop();

            if (left instanceof Variable) {
                if (left.equals(right)) {
                    // nothing to do
                } else if (right.containsVariable((Variable) left)) {
                    // not unifiable
                    return null;
                } else {
                    // generate substitution
                    Substitution rule = new Substitution((Variable) left, right);
                    for (int i = 0; i < stack1.size(); i++) {
                        stack1.setElementAt(rule.apply((Term) stack1.elementAt(i)), i);
                        stack2.setElementAt(rule.apply((Term) stack2.elementAt(i)), i);
                    }
                    substs.addAndApplyToOldRules(rule);
                }
            } else if (!left.hasSubterms()) {
                if (right.hasSubterms() || !left.equals(right)) {
                    // not unifiable
                    return null;
                }
            } else if ( // left musst be constant
            left instanceof Constant && right instanceof Constant) {
                Constant cleft = (Constant) left;
                Constant cright = (Constant) right;
                if (!cleft.getName().equals(cright.getName())
                        || cleft.getSubterms().size() != cright.getSubterms().size()) {
                    return null;
                }
                stack1.addAll(cleft.getSubterms());
                stack2.addAll(cright.getSubterms());
            } else {
                return null;
            }
        }

        return substs;
    }

    /**
     * 
     * @param t1
     * @param t2
     * @param substs
     * @return
     */
    public static Substitutions findMGU(Term t1, Term t2, Substitutions substs) {
        assert t1 != null;
        assert t2 != null;
        assert substs != null;

        // terms are equal, there is nothing to do
        if (t1.equals(t2)) {
            return substs;
        }

        // terms are not equal, and cannot be unified
        if (!t2.hasVariables() && !t1.hasVariables()) {
            return null;
        }

        // try to find result in the hashtable
        if (Unificator.hashtable.containsKey(t1)) {
            HashMap<Term, Substitutions> hashtable2 = hashtable.get(t1);
            if (hashtable2.containsKey(t2)) {
                Substitutions s2 = hashtable2.get(t2);
                return (s2 == null) ? null : s2.clone();
            }
        } else {
            Unificator.hashtable.put(t1, new HashMap<Term, Substitutions>(50));
        }

        // shit we must run the unification algorithm

        Stack<Term> stack1 = new Stack<Term>();
        Stack<Term> stack2 = new Stack<Term>();

        stack1.push(t1);
        stack2.push(t2);

        while (!stack1.empty()) {
            Term left = stack1.pop();
            Term right = stack2.pop();

            // assure that left term is variable
            if (right instanceof Variable) {
                Term tmp = right;
                right = left;
                left = tmp;
            }

            if (left instanceof Variable) {
                if (left.equals(right)) {
                    // nothing to do
                } else if (right.containsVariable((Variable) left)) {
                    // not unifiable
                    Unificator.hashtable.get(t1).put(t2, null);
                    return null;
                } else {
                    // generate substitution
                    Substitution rule = new Substitution((Variable) left, right);
                    for (int i = 0; i < stack1.size(); i++) {
                        stack1.setElementAt(rule.apply((Term) stack1.elementAt(i)), i);
                        stack2.setElementAt(rule.apply((Term) stack2.elementAt(i)), i);
                    }
                    substs.addAndApplyToOldRules(rule);
                }
            } else if (!left.hasSubterms()) {
                if (right.hasSubterms() || !left.equals(right)) {
                    // not unifiable
                    Unificator.hashtable.get(t1).put(t2, null);
                    return null;
                }
            } else if ( // left musst be constant
            left instanceof Constant && right instanceof Constant) {
                Constant cleft = (Constant) left;
                Constant cright = (Constant) right;
                if (!cleft.getName().equals(cright.getName())
                        || cleft.getSubterms().size() != cright.getSubterms().size()) {
                    Unificator.hashtable.get(t1).put(t2, null);
                    return null;
                }
                stack1.addAll(cleft.getSubterms());
                stack2.addAll(cright.getSubterms());
            } else {
                // not unifiable
                Unificator.hashtable.get(t1).put(t2, null);
                return null;
            }
        }

        Unificator.hashtable.get(t1).put(t2, substs);
        assert Unificator.hashtable.get(t1) != null;
        assert Unificator.hashtable.get(t1).get(t2) != null;

        return substs;
    }

}
