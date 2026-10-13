#!/usr/bin/env python3
"""
verify_nomograms.py
Systematic accuracy assessment of the PyNomo/Nomogen nomograms.

For every nomogram script the PyNomo geometry (final paper coordinates, in cm,
after all projective transformations) is recovered from the Nomographer object.
Two error components are evaluated separately, on random samples of input
values drawn uniformly over the scale ranges:

 1. Construction error: the isopleth construction is reproduced numerically
    (straight lines, intersections with reference lines, root-finding of the
    output value on its scale) with no reading noise. It measures how exactly
    the drawn scales implement the target equation.
 2. Reading error: each point the user sets or reads (input marks, pivot points
    on reference lines and the output reading) is displaced along its scale by
    a Gaussian error of standard deviation sigma (mm, on the printed nomogram
    at its native size). sigma = 0.25 mm and 0.5 mm are used.

Usage:  python verify_nomograms.py <dir_with_scripts> <nomogen_dir> <out_dir> [N]
        e.g. python verify_nomograms.py . ../pynomo/nomogen results 2000
"""
import os, sys, json, math, shutil, runpy, tempfile, contextlib, io, zlib
import numpy as np
from scipy.optimize import brentq

SCRIPTS, NOMOGEN_DIR, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
NSAMP = int(sys.argv[4]) if len(sys.argv) > 4 else 2000
SIGMAS_MM = [0.25, 0.5]
rng = np.random.default_rng(20261012)
sys.path.insert(0, NOMOGEN_DIR)

import pynomo.nomographer as pn
_captured = []
_Orig = pn.Nomographer
class _Capture(_Orig):
    def __init__(self, params):
        super().__init__(params)
        _captured.append(self)
pn.Nomographer = _Capture


def build(script):
    """Run a nomogram script in a scratch dir and return its Nomographer."""
    _captured.clear()
    work = tempfile.mkdtemp()
    shutil.copy(os.path.join(SCRIPTS, script), work)
    cwd = os.getcwd(); os.chdir(work)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            runpy.run_path(os.path.join(work, script), run_name="__main__")
    finally:
        os.chdir(cwd)
    return _captured[-1]


# ---------------------------------------------------------------- geometry
def P(atom, u):
    return np.array([atom.give_x(u), atom.give_y(u)])

def tang(atom, u):
    h = 1e-6 * max(1.0, abs(u))
    d = (P(atom, u + h) - P(atom, u - h)) / (2 * h)
    return d  # cm per unit of u

def unit(v):
    return v / np.linalg.norm(v)

def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]

def intersect(a1, a2, b1, b2):
    da, db = a2 - a1, b2 - b1
    t = cross(b1 - a1, db) / cross(da, db)
    return a1 + t * da

def solve_on(atom, A, B, lo, hi):
    f = lambda u: cross(B - A, P(atom, u) - A)
    us = np.linspace(lo, hi, 60)
    fs = [f(u) for u in us]
    for i in range(len(us) - 1):
        if fs[i] == 0:
            return us[i]
        if fs[i] * fs[i + 1] < 0:
            return brentq(f, us[i], us[i + 1], xtol=1e-14, rtol=1e-14, maxiter=200)
    return np.nan

def mark(atom, u, s):
    """point of value u displaced along its scale by s (cm)."""
    return P(atom, u) + s * unit(tang(atom, u))

def read_noise(atom, u, s):
    """value read when the true intersection is displaced by s (cm)."""
    return u + s / np.linalg.norm(tang(atom, u))


# ------------------------------------------------- generic 3-scale solver
def three_scale(atoms, vals, unknown, lo, hi, s=None):
    """atoms: 3 atoms; vals: values (None for unknown); s: noise (cm) or None."""
    s = s if s is not None else np.zeros(3)
    pts = [None if i == unknown else mark(atoms[i], vals[i], s[i]) for i in range(3)]
    k = [i for i in range(3) if i != unknown]
    u = solve_on(atoms[unknown], pts[k[0]], pts[k[1]], lo, hi)
    return read_noise(atoms[unknown], u, s[unknown]) if not np.isnan(u) else np.nan


# ------------------------------------------------- type 3 chain solver
def type3(block, vals, unknown, lo, hi, s=None):
    """F1+...+FN=0 with N-3 reference lines (PyNomo type 3)."""
    N = len(vals)
    F = block.atom_stack[:N]
    R = block.atom_stack[N:N + N - 3]
    s = s if s is not None else np.zeros(2 * N)
    sF, sR = s[:N], s[N:]
    Rl = [(P(r, 0.0), P(r, 1.0)) for r in R]

    def chain(u):
        v = list(vals); v[unknown] = u
        pts = [mark(F[i], v[i], sF[i] if i != unknown else 0.0) for i in range(N)]
        piv = intersect(pts[0], pts[1], *Rl[0])
        piv = piv + sR[0] * unit(Rl[0][1] - Rl[0][0])
        for j in range(1, N - 3):
            piv = intersect(piv, pts[j + 1], *Rl[j])
            piv = piv + sR[j] * unit(Rl[j][1] - Rl[j][0])
        return cross(pts[N - 2] - piv, pts[N - 1] - piv)

    us = np.linspace(lo, hi, 80)
    fs = [chain(u) for u in us]
    for i in range(len(us) - 1):
        if fs[i] * fs[i + 1] < 0:
            u = brentq(chain, us[i], us[i + 1], xtol=1e-14, rtol=1e-14, maxiter=200)
            return read_noise(F[unknown], u, sF[unknown])
    return np.nan


# ---------------------------------------------------------- definitions
def U(a, b, n):
    return rng.uniform(a, b, n)

def LU(a, b, n):
    return np.exp(rng.uniform(np.log(a), np.log(b), n))

cases = []

# 1. Bond's law (blocks 1+2, short-ton scales)
def bond_setup(nomo):
    b1, b2 = nomo.wrapper.block_stack[0], nomo.wrapper.block_stack[1]
    F80a, P80a, A1 = b1.atom_stack[:3]
    Ea, Wia, A2 = b2.atom_stack[:3]
    Aline = (P(A1, A1.params['u_min']), P(A1, A1.params['u_max']))
    def solve(x, s):
        F80, P80, Wi = x
        p1 = mark(F80a, F80, s[0]); p2 = mark(P80a, P80, s[1])
        piv = intersect(p1, p2, *Aline) + s[2] * unit(Aline[1] - Aline[0])
        p3 = mark(Wia, Wi, s[3])
        E = solve_on(Ea, piv, p3, 5, 20)
        return read_noise(Ea, E, s[4]) if not np.isnan(E) else np.nan
    return solve, 5
def bond_sample(n):
    out = []
    while len(out) < n:
        F80, P80, Wi = LU(1000, 120000, 1)[0], LU(50, 500, 1)[0], U(8, 25, 1)[0]
        E = 10 * Wi * (P80 ** -0.5 - F80 ** -0.5)
        if 5 <= E <= 20:
            out.append(((F80, P80, Wi), E))
    return out
cases.append(dict(name="Bond's law (Fig. 3)", script="Law_of_Bond_Nomogram.py",
                  setup=bond_setup, sample=bond_sample,
                  center=lambda x: [(x[0], 1000, 120000, 'log'), (x[1], 50, 500, 'log'), (x[2], 8, 25, 'lin')]))

# 2. Modified Hogg & Fuerstenau (type 3, N=7; unknown Pnet, index 3)
def hf_exact(Nc, D, LD, rho, a, J, k=0.267, c=1.0):
    return k * D ** 3.5 * LD * Nc * rho * (J - c * J * J) * math.sin(math.radians(a))
def hf_setup(nomo):
    blk = nomo.wrapper.block_stack[0]
    def solve(x, s):
        Nc, D, LD, rho, a, J = x
        return type3(blk, [Nc, D, LD, None, rho, a, J], 3, 1000, 30000, s)
    return solve, 11
def hf_sample_factory(k, c, Jmin, Jmax, LDmin, LDmax, rmin, rmax, amin, amax):
    def f(n):
        out = []
        while len(out) < n:
            x = (U(0.65, 0.80, 1)[0], LU(10, 40, 1)[0], U(LDmin, LDmax, 1)[0],
                 U(rmin, rmax, 1)[0], U(amin, amax, 1)[0], U(Jmin, Jmax, 1)[0])
            Pn = hf_exact(*x, k=k, c=c)
            if 1000 <= Pn <= 30000:
                out.append((x, Pn))
        return out
    return f
cases.append(dict(name="Modified Hogg & Fuerstenau (Figs. 5, 11)", script="Modified_Hogg_Fuerstenau_Nomogram.py",
                  setup=hf_setup, sample=hf_sample_factory(0.267, 1.0, 0.20, 0.40, 0.5, 2.0, 2.0, 6.0, 25, 45),
                  center=lambda x: [(x[0], .65, .8, 'lin'), (x[1], 10, 40, 'log'), (x[2], .5, 2, 'lin'),
                                    (x[3], 2, 6, 'lin'), (x[4], 25, 45, 'lin'), (x[5], .2, .4, 'lin')]))

# 3. Azzaroni (type 3, N=6; unknown dB, index 1)
def az_exact(F80, rho, Wi, N, D):
    return 6.06 * F80 ** 0.263 * (rho * Wi) ** 0.4 / (N * D) ** 0.25
def az_setup(nomo):
    blk = nomo.wrapper.block_stack[0]
    def solve(x, s):
        F80, rho, Wi, N, D = x
        return type3(blk, [F80, None, rho, Wi, N, D], 1, 25, 100, s)
    return solve, 9
def az_sample(n):
    out = []
    while len(out) < n:
        x = (LU(1000, 10000, 1)[0], U(2, 4, 1)[0], U(8, 25, 1)[0], U(11, 17, 1)[0], LU(10, 30, 1)[0])
        d = az_exact(*x)
        if 25 <= d <= 100:
            out.append((x, d))
    return out
cases.append(dict(name="Azzaroni make-up ball size (Fig. 7)", script="Azzaroni_Nomogram.py",
                  setup=az_setup, sample=az_sample,
                  center=lambda x: [(x[0], 1000, 10000, 'log'), (x[1], 2, 4, 'lin'), (x[2], 8, 25, 'lin'),
                                    (x[3], 11, 17, 'lin'), (x[4], 10, 30, 'log')]))

# 4. Circulating load (type 9 with grid S2-S3)
def cl_exact(S1, S2, S3):
    return (100 / S2 - 100 / S1) / (100 / S1 - 100 / S3)
def cl_setup(nomo):
    blk = nomo.wrapper.block_stack[0]
    G, CL, S1a = blk.atom_stack[:3]
    def solve(x, s):
        S1, S2, S3 = x
        g = np.array([G.give_x_grid(S2, S3), G.give_y_grid(S2, S3)]) + s[0:2]
        p = mark(S1a, S1, s[2])
        u = solve_on(CL, g, p, 0.1, 10.0)
        return read_noise(CL, u, s[3]) if not np.isnan(u) else np.nan
    return solve, 4
def cl_sample(n):
    out = []
    while len(out) < n:
        S2, S3 = U(10, 50, 1)[0], U(66, 85, 1)[0]
        S1 = U(max(10, S2 + 0.5), 65, 1)[0]
        c = cl_exact(S1, S2, S3)
        if 0.1 <= c <= 10:
            out.append(((S1, S2, S3), c))
    return out
cases.append(dict(name="Circulating load (Fig. 6)", script="Circulating_Load_Nomogram.py",
                  setup=cl_setup, sample=cl_sample, grid_noise=True,
                  center=lambda x: [(x[0], 10, 65, 'lin'), (x[1], 10, 50, 'lin'), (x[2], 66, 85, 'lin')]))

# 5. Valuable recovery (Nomogen, type 9)
def rec_exact(t, c):
    return 100 * c * (1 - t) / (c - t)
def three_setup(lo, hi):
    def setup(nomo):
        atoms = nomo.wrapper.block_stack[0].atom_stack[:3]
        def solve(x, s):
            return three_scale(atoms, [x[0], None, x[1]], 1, lo, hi, s)
        return solve, 3
    return setup
def two_in_sample(f, a, b, c, d, lo, hi):
    def g(n):
        out = []
        while len(out) < n:
            x = (U(a, b, 1)[0], U(c, d, 1)[0]); y = f(*x)
            if lo <= y <= hi:
                out.append((x, y))
        return out
    return g
Rlo = min(rec_exact(t, c) for t in (0.05, 0.2) for c in (5, 30)); Rhi = max(rec_exact(t, c) for t in (0.05, 0.2) for c in (5, 30))
cases.append(dict(name="Valuable recovery (Fig. 8, Nomogen)", script="Valuable_Recovery_Nomogram.py",
                  setup=three_setup(Rlo, Rhi), sample=two_in_sample(rec_exact, 0.05, 0.20, 5, 30, Rlo, Rhi),
                  center=lambda x: [(x[0], .05, .2, 'lin'), (x[1], 5, 30, 'lin')]))

# 6. Apparent charge density (type 10): unknown rho_ap (atom 0)
def cd_exact(Jbc, rm):
    return 4.65 * Jbc + 0.6 * rm * (1 - Jbc) + 0.4 * ((rm - 1) * 0.5 + 1)
def cd_setup(nomo):
    atoms = nomo.wrapper.block_stack[0].atom_stack[:3]
    def solve(x, s):
        return three_scale(atoms, [None, x[0], x[1]], 0, 2.0, 7.0, s)
    return solve, 3
cases.append(dict(name="Apparent charge density (Fig. A.2)", script="Apparent_Mill_Charge_Density_Nomogram.py",
                  setup=cd_setup, sample=two_in_sample(cd_exact, 0.0, 1.0, 2.0, 7.0, 2.0, 7.0),
                  center=lambda x: [(x[0], 0, 1, 'lin'), (x[1], 2, 7, 'lin')]))

# 7. Mill speed (type 2): unknown Nc (atom 0)
def ms_exact(N, D):
    return N * math.sqrt(D) / 76.6
def ms_setup(nomo):
    atoms = nomo.wrapper.block_stack[0].atom_stack[:3]
    def solve(x, s):
        return three_scale(atoms, [None, x[0], x[1]], 0, 0.1, 1.0, s)
    return solve, 3
cases.append(dict(name="Mill speed (Fig. A.1)", script="Mill_Speed_Nomogram.py",
                  setup=ms_setup, sample=two_in_sample(ms_exact, 10, 20, 10, 30, 0.1, 1.0),
                  center=lambda x: [(x[0], 10, 20, 'lin'), (x[1], 10, 30, 'lin')]))

# 8-10. Slurry nomograms (Nomogen, type 9): left f_sw, middle unknown, right rho_m
def rp(f, r): return 100 / ((f / r) + (100 - f))
def fsv(f, r): return 100 * (f / r) / ((f / r) + (100.0 - f))
def gl(f, r): return 1000 / ((1 / r) + ((100 - f) / f))
for nm, sc, fn in [("Slurry density, weight % solids (Fig. A.3)", "Mill_Weight_Percentage_of_Solids_Nomogram.py", rp),
                   ("Volume % solids (Fig. A.4)", "Mill_Volume_Percentage_of_Solids_Nomogram.py", fsv),
                   ("Weight of solids per litre (Fig. A.5)", "Mill_Weight_of_Solids_in_a_Litre_Nomogram.py", gl)]:
    vals = [fn(f, r) for f in (20, 80) for r in (2.5, 4.0)]
    lo, hi = min(vals), max(vals)
    cases.append(dict(name=nm, script=sc, setup=three_setup(lo, hi),
                      sample=two_in_sample(fn, 20, 80, 2.5, 4.0, lo, hi),
                      center=lambda x: [(x[0], 20, 80, 'lin'), (x[1], 2.5, 4.0, 'lin')]))


def is_central(spec):
    """True if every input lies in the central 60 % of its scale."""
    for v, a, b, kind in spec:
        if kind == 'log':
            v, a, b = math.log(v), math.log(a), math.log(b)
        f = (v - a) / (b - a)
        if f < 0.20 or f > 0.80:
            return False
    return True


# --------------------------------------------------------------- run
results = []
for cs in cases:
    # per-case seed: results do not depend on the order or number of cases
    rng = np.random.default_rng(20261012 + zlib.crc32(cs['script'].encode()))
    try:
        nomo = build(cs['script'])
    except Exception as e:
        results.append(dict(name=cs['name'], error=repr(e))); print(cs['name'], "FAILED", e); continue
    solve, nnoise = cs['setup'](nomo)
    samples = cs['sample'](NSAMP)
    cons = []
    for x, y in samples:
        yn = solve(x, np.zeros(nnoise))
        cons.append((yn - y) / y)
    cons = np.array(cons); ok = ~np.isnan(cons)
    res = dict(name=cs['name'], script=cs['script'], n=int(ok.sum()),
               paper_cm=[nomo.wrapper.paper_width, nomo.wrapper.paper_height] if hasattr(nomo.wrapper, 'paper_width') else None,
               construction_max_abs_pct=float(np.nanmax(np.abs(cons)) * 100),
               construction_mean_pct=float(np.nanmean(cons) * 100))
    if not cs.get('construction_only'):
        for sig in SIGMAS_MM:
            errs, cen = [], []
            for x, y in samples:
                s = rng.normal(0, sig / 10.0, nnoise)  # mm -> cm
                yn = solve(x, s)
                if not np.isnan(yn):
                    errs.append(abs(yn - y) / y * 100)
                    cen.append(is_central(cs['center'](x)))
            errs, cen = np.array(errs), np.array(cen, bool)
            res[f'read_{sig}mm'] = dict(
                median=float(np.median(errs)), p95=float(np.percentile(errs, 95)), max=float(errs.max()),
                within_1pct=float(np.mean(errs <= 1) * 100), within_3pct=float(np.mean(errs <= 3) * 100),
                central_n=int(cen.sum()),
                central_median=float(np.median(errs[cen])) if cen.any() else None,
                central_p95=float(np.percentile(errs[cen], 95)) if cen.any() else None,
                outer_median=float(np.median(errs[~cen])) if (~cen).any() else None,
                outer_p95=float(np.percentile(errs[~cen], 95)) if (~cen).any() else None)
    results.append(res)
    print(json.dumps(res))

os.makedirs(OUT, exist_ok=True)
json.dump(results, open(os.path.join(OUT, 'verification_results.json'), 'w'), indent=2)
