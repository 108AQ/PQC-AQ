#!/usr/bin/env python3
"""
triangle_to_cnf.py -- bounded proof search for the triangle angle-sum theorem, as CNF.

Statement to prove:  m<BAC + m<ABC + m<ACB = 180  (atom `goal`).

The geometry is grounded: a finite pool of statements (atoms) and a finite pool of
ground axiom/lemma instances (rules), taken from the 27-line proof.  Each rule is
`premises |- conclusion`, tagged with the axiom it instantiates.  The CNF searches for
an assignment of statements and justifications to k proof lines.

    build(k)  ->  CNF satisfiable  iff  `goal` has a k-line proof inside this pool

Variables
    line[i,s]   line i asserts statement s
    by[i,r]     line i is justified by rule instance r

Clauses
    (a) exactly one statement per line
    (b) exactly one justification per line
    (c) the justification's conclusion is the line's statement
    (d) every premise of the justifying rule appears on an earlier line
    (e) the last line is the goal

A satisfying assignment decodes to a genuine proof.  UNSAT means only that no proof of
that length exists inside this pool -- not that none exists at all.

Usage:
    python3 triangle_to_cnf.py 27              build, solve, decode, verify
    python3 triangle_to_cnf.py 27 out.cnf      ... and write DIMACS
"""
import itertools
import sys
from collections import Counter

# statement pool: name -> reading  (S-numbers refer to the 27-line proof)
ATOMS = {
    'tri':        'A, B, C are not collinear (S1)',
    'angRange':   '0 < m<ABC < 180 and 0 < m<ACB < 180 (S2)',
    'Dpt':        'D chosen opposite C across AB with m<BAD = m<ABC (S3)',
    'ADparBC':    'line AD is parallel to line BC (S4)',
    'Ept':        'E chosen opposite B across AC with m<CAE = m<ACB (S5)',
    'AEparBC':    'line AE is parallel to line BC (S6)',
    'ell':        'line AD = line AE = ell (S7)',
    'ellMisses':  'ell misses BC; B, C off ell; ell is neither AB nor AC (S8)',
    'meetA':      'ell meets AB only at A, and AC only at A (S9)',
    'BCsameSide': 'B and C are on the same side of ell (S10)',
    'DEonEll':    'D, E on ell, distinct from A, off AB and AC (S11)',
    'c12':        'not-beta implies A is not on segment DE (S12)',
    'c13':        'not-beta implies segment DE misses AC (S13)',
    'c14':        'not-beta implies D is opposite B across AC (S14)',
    'Fpt':        'F chosen with F-A-D (S15)',
    'Fsides':     'F on ell, opposite D across AB and across AC (S16)',
    'FsameC':     'F is on the same side of AB as C (S17)',
    'c18':        'not-beta implies F is on the same side of AC as B (S18)',
    'c19':        'not-beta implies F is interior to angle BAC (S19)',
    'c20':        'not-beta implies ell meets BC (S20)',
    'beta':       'A is between D and E (S21)',
    'linPair':    'm<BAD + m<BAE = 180 (S22)',
    'EsameC':     'E is on the same side of AB as C (S23)',
    'Cinterior':  'C is interior to angle BAE (S24)',
    'addC':       'm<BAC + m<CAE = m<BAE (S25)',
    'sum3':       'm<BAD + m<BAC + m<CAE = 180 (S26)',
    'goal':       'm<BAC + m<ABC + m<ACB = 180 (S27)',
    # decoys: derivable but useless, plus one statement nothing can produce
    'Gpt':        'G chosen with G-A-E (unused)',
    'Gsides':     'G on ell, opposite E across AB and AC (unused)',
    'linPairF':   'm<BAF + m<BAD = 180 (unused)',
    'ABneAC':     'line AB is not line AC (unused)',
    'noParallel': 'the parallel postulate fails (no rule produces this)',
    'bogus':      'm<BAC + m<ABC + m<ACB < 180 (hyperbolic; underivable here)',
}

# ground rule instances: (name, premises, conclusion)
RULES = [
    ('hyp|-tri',           [],                                  'tri'),
    ('Ax4a|-angRange',     ['tri'],                             'angRange'),
    ('Ax4b|-Dpt',          ['tri', 'angRange'],                 'Dpt'),
    ('T1|-ADparBC',        ['Dpt'],                             'ADparBC'),
    ('Ax4b|-Ept',          ['tri', 'angRange'],                 'Ept'),
    ('T1|-AEparBC',        ['Ept'],                             'AEparBC'),
    ('Ax7|-ell',           ['tri', 'ADparBC', 'AEparBC'],       'ell'),
    ('def|-ellMisses',     ['ADparBC', 'ell'],                  'ellMisses'),
    ('Ax1|-meetA',         ['ellMisses'],                       'meetA'),
    ('Ax3|-BCsameSide',    ['ellMisses'],                       'BCsameSide'),
    ('def|-DEonEll',       ['Dpt', 'Ept', 'ell', 'meetA'],      'DEonEll'),
    ('def|-c12',           ['DEonEll'],                         'c12'),
    ('Ax1|-c13',           ['c12', 'meetA'],                    'c13'),
    ('Ax3|-c14',           ['c13', 'DEonEll', 'Ept'],           'c14'),
    ('Ax2|-Fpt',           [],                                  'Fpt'),
    ('Ax3|-Fsides',        ['Fpt', 'meetA', 'DEonEll'],         'Fsides'),
    ('Ax3|-FsameC',        ['Fsides', 'Dpt'],                   'FsameC'),
    ('Ax3|-c18',           ['Fsides', 'c14'],                   'c18'),
    ('def|-c19',           ['FsameC', 'c18'],                   'c19'),
    ('T2|-c20',            ['c19'],                             'c20'),
    ('MT|-beta',           ['c20', 'ellMisses'],                'beta'),
    ('Ax6|-linPair',       ['beta', 'ellMisses'],               'linPair'),
    ('Ax3|-EsameC',        ['beta', 'DEonEll', 'Dpt'],          'EsameC'),
    ('def|-Cinterior',     ['EsameC', 'BCsameSide'],            'Cinterior'),
    ('Ax5|-addC',          ['Cinterior'],                       'addC'),
    ('sub|-sum3',          ['linPair', 'addC'],                 'sum3'),
    ('sub|-goal',          ['sum3', 'Dpt', 'Ept'],              'goal'),
    ('Ax2|-Gpt',           [],                                  'Gpt'),
    ('Ax3|-Gsides',        ['Gpt', 'meetA', 'DEonEll'],         'Gsides'),
    ('Ax6|-linPairF',      ['Fpt', 'ellMisses'],                'linPairF'),
    ('Ax1|-ABneAC',        ['tri'],                             'ABneAC'),
    ('hyperbolic|-bogus',  ['noParallel'],                      'bogus'),
]
GOAL = 'goal'


class CNF:
    def __init__(self):
        self.ids, self.names, self.clauses = {}, {}, []

    def var(self, name):
        if name not in self.ids:
            self.ids[name] = len(self.ids) + 1
            self.names[self.ids[name]] = name
        return self.ids[name]

    def add(self, group, *lits):
        self.clauses.append((group, list(lits)))

    def show(self, lits):
        return '(' + ' v '.join(('-' if l < 0 else '') + self.names[abs(l)] for l in lits) + ')'


def build(k):
    """The reduction: budget of k proof lines -> CNF."""
    F = CNF()
    atoms = sorted(ATOMS)
    rules = sorted(RULES)                       # name order, not proof order
    line = lambda i, s: F.var(f'line[{i},{s}]')
    by = lambda i, r: F.var(f'by[{i},{r}]')

    for i in range(1, k + 1):
        # (a) exactly one statement per line
        F.add('one statement per line', *[line(i, s) for s in atoms])
        for s, t in itertools.combinations(atoms, 2):
            F.add('one statement per line', -line(i, s), -line(i, t))

        # (b) exactly one justification per line
        F.add('one justification per line', *[by(i, r[0]) for r in rules])
        for r, q in itertools.combinations(rules, 2):
            F.add('one justification per line', -by(i, r[0]), -by(i, q[0]))

        for name, prem, concl in rules:
            # (c) the rule's conclusion is what the line asserts
            F.add('conclusion matches rule', -by(i, name), line(i, concl))
            # (d) each premise appears on an earlier line
            for p in prem:
                F.add('premises appear earlier',
                      -by(i, name), *[line(j, p) for j in range(1, i)])

    # (e) the last line is the theorem
    F.add('last line is the goal', line(k, GOAL))

    # (f) no statement is repeated -- duplicate lines can always be deleted
    for s in atoms:
        for i, j in itertools.combinations(range(1, k + 1), 2):
            F.add('no repeated statement', -line(i, s), -line(j, s))

    # (g) every line before the last is used later -- dead lines can be deleted
    users = {s: [n for n, p, _ in rules if s in p] for s in atoms}
    for i in range(1, k):
        for s in atoms:
            F.add('no unused line', -line(i, s),
                  *[by(j, r) for j in range(i + 1, k + 1) for r in users[s]])
    return F


def solve(clauses, nvars, order):
    """DPLL: unit propagation over occurrence lists, branching in the given order."""
    key = lambda lit: 2 * abs(lit) + (lit < 0)
    occ = [[] for _ in range(2 * nvars + 2)]
    for idx, c in enumerate(clauses):
        for l in c:
            occ[key(-l)].append(idx)
    stats = Counter()

    def propagate(assign, queue):
        while queue:
            for idx in occ[key(queue.pop())]:
                free, last = 0, 0
                for l in clauses[idx]:
                    val = assign.get(abs(l))
                    if val is None:
                        free, last = free + 1, l
                    elif val == (l > 0):
                        break
                else:
                    if free == 0:
                        stats['conflicts'] += 1
                        return False
                    if free == 1:
                        assign[abs(last)] = last > 0
                        queue.append(last)
        return True

    def dpll(assign, queue):
        if not propagate(assign, queue):
            return None
        v = next((v for v in order if v not in assign), None)
        if v is None:
            return assign
        for val in (True, False):
            stats['decisions'] += 1
            model = dpll({**assign, v: val}, [v if val else -v])
            if model is not None:
                return model
        return None

    assign, queue = {}, []
    for c in clauses:
        if len(c) == 1:
            l = c[0]
            if assign.get(abs(l)) == (l < 0):
                return None, stats
            assign[abs(l)] = l > 0
            queue.append(l)
    return dpll(assign, queue), stats


def solve_instance(F):
    order = [v for n, v in F.ids.items() if n.startswith('by[')]
    order += [v for v in range(1, len(F.ids) + 1) if v not in set(order)]
    return solve([c for _, c in F.clauses], len(F.ids), order)


def decode(F, model, k):
    out = []
    for i in range(1, k + 1):
        s = next(n[len(f'line[{i},'):-1] for n, v in F.ids.items()
                 if n.startswith(f'line[{i},') and model.get(v))
        r = next(n[len(f'by[{i},'):-1] for n, v in F.ids.items()
                 if n.startswith(f'by[{i},') and model.get(v))
        out.append((s, r))
    return out


def verify(proof):
    """Independent checker: is this a genuine proof of the goal in this system?"""
    rules = {n: (p, c) for n, p, c in RULES}
    seen = set()
    for s, r in proof:
        prem, concl = rules[r]
        if concl != s or any(p not in seen for p in prem):
            return False
        seen.add(s)
    return proof[-1][0] == GOAL


def write_dimacs(F, path, k):
    with open(path, 'w') as f:
        f.write(f'c triangle angle-sum theorem, budget of {k} proof lines, reduced to CNF\n')
        f.write('c satisfiable iff the goal has a k-line proof in this grounded system\n')
        for v in range(1, len(F.ids) + 1):
            f.write(f'c var {v} = {F.names[v]}\n')
        f.write(f'p cnf {len(F.ids)} {len(F.clauses)}\n')
        for _, c in F.clauses:
            f.write(' '.join(map(str, c)) + ' 0\n')


def main(k, dimacs=None):
    F = build(k)
    print(f'Budget: {k} lines')
    print(f'CNF: {len(F.ids)} variables, {len(F.clauses)} clauses')
    for g, n in Counter(g for g, _ in F.clauses).items():
        print(f'   {g:<26}{n:>7}')
    if dimacs:
        write_dimacs(F, dimacs, k)
        print(f'DIMACS written to {dimacs}')
    model, stats = solve_instance(F)
    print(f'decisions: {stats["decisions"]}, conflicts: {stats["conflicts"]}')
    if model is None:
        print('UNSAT -> no proof of this length exists in this pool')
        return
    proof = decode(F, model, k)
    print('SAT -> decoded proof:')
    for i, (s, r) in enumerate(proof, 1):
        print(f'  {i:>3}. {s:<12} by {r:<20} {ATOMS[s]}')
    print(f'checker accepts the decoded proof: {verify(proof)}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(int(sys.argv[1]), sys.argv[2] if len(sys.argv) > 2 else None)
