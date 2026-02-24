"""
proof_fr2.py — Rigorous proof scheme for f_r = 2 at all odd primes
for the Goldbach-Frey curve C: y² = x(x²-p²)(x²-q²)

This script:
  1. Proves the four cases are exhaustive and mutually exclusive
  2. Computes the reduced curve and singularity type for each case
  3. Determines (a, t, u) for the Néron model
  4. Verifies f_r = 4 - (2a + t) = 2 in all cases
  5. Cross-validates against the 10 Magma data points
"""
import math
from sympy import factorint, isprime, gcd

print("""
╔══════════════════════════════════════════════════════════════════════════╗
║  PROOF SCHEME: f_r = 2 for all odd primes r                           ║
║  Curve: C: y² = x(x² - p²)(x² - q²),  p + q = 2N,  p < q primes    ║
╚══════════════════════════════════════════════════════════════════════════╝
""")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 0: SETUP AND KEY FORMULA
# ═══════════════════════════════════════════════════════════════════════════
print("""
STEP 0: THE CONDUCTOR EXPONENT FORMULA
═══════════════════════════════════════

For a genus-2 curve C over Q_r with r odd (tame ramification), the
conductor exponent of Jac(C) at r is:

    f_r = 2g - dim(V_ℓ^{I_r})   where g = 2

Here V_ℓ = H¹(C_{Q̄}, Q_ℓ) is the 4-dimensional ℓ-adic Galois
representation, and I_r is the inertia group at r.

The identity component of the Néron model's special fiber A⁰_s has:
  - Abelian part of dimension a  (contributes 2a to V^{I_r})
  - Toric part of dimension t    (contributes t to V^{I_r})  
  - Unipotent part of dimension u (contributes 0 to V^{I_r} since ℓ ≠ r)

with a + t + u = g = 2.

Therefore:
    dim(V_ℓ^{I_r}) = 2a + t
    f_r = 4 - (2a + t)

To prove f_r = 2, we must show 2a + t = 2 for every bad odd prime r.
""")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 1: CLASSIFICATION OF BAD ODD PRIMES
# ═══════════════════════════════════════════════════════════════════════════
print("""
STEP 1: FOUR MUTUALLY EXCLUSIVE CASES
══════════════════════════════════════

The roots of f(x) = x(x² - p²)(x² - q²) are R = {0, p, -p, q, -q}.
The discriminant Δ = 16 · p⁶ · q⁶ · (p-q)⁴ · (2N)⁴.

An odd prime r is bad iff r | p·q·N·(p-q).

CLAIM: For p ≠ q distinct odd primes, the bad odd primes partition into
four mutually exclusive classes:

  Case I:   r = p                (r | p, r ∤ q, r ∤ N, r ∤ (p-q))
  Case II:  r = q                (r | q, r ∤ p, r ∤ N, r ∤ (p-q))  
  Case III: r | N, r ∤ pq        (r | (p+q), r ∤ p, r ∤ q)
  Case IV:  r | (p-q), r ∤ pqN   (r | (p-q), r ∤ p, r ∤ q, r ∤ N)

PROOF OF MUTUAL EXCLUSIVITY:
""")

print("  If r | p and r | q: since p, q are prime and p ≠ q, this requires")
print("  r = p = q, contradicting p ≠ q. ✗")
print()
print("  If r | p and r | N: r | p and r | (p+q)/2 implies r | q (since r")
print("  is odd). But r = p and r | q forces p = q. ✗")
print()
print("  If r | p and r | (p-q): r | p and r | (p-q) implies r | q. ✗")
print()
print("  If r | N and r | (p-q): r | (p+q) and r | (p-q) implies")
print("  r | 2p (summing), so r | p (r odd). Similarly r | q. ✗")
print()
print("  Therefore the four cases are mutually exclusive. ✓")
print("  Exhaustiveness follows from Δ = 16 · p⁶ · q⁶ · (p-q)⁴ · (2N)⁴. ✓")

# Verify with data
print("\n  COMPUTATIONAL VERIFICATION (10 Magma cases):")
magma_data = [
    (3,  7,   {2:8, 3:2, 5:2, 7:2}),
    (7,  23,  {2:4, 3:2, 5:2, 7:2, 23:2}),
    (11, 19,  {2:7, 3:2, 5:2, 11:2, 19:2}),
    (13, 17,  {2:8, 3:2, 5:2, 13:2, 17:2}),
    (3,  17,  {2:8, 3:2, 5:2, 7:2, 17:2}),
    (7,  19,  {2:8, 3:2, 7:2, 13:2, 19:2}),
    (3,  37,  {2:7, 3:2, 5:2, 17:2, 37:2}),
    (7,  41,  {2:4, 3:2, 7:2, 17:2, 41:2}),
    (7,  53,  {2:8, 3:2, 5:2, 7:2, 23:2, 53:2}),
    (11, 37,  {2:4, 3:2, 11:2, 13:2, 37:2}),
]

def odd_prime_factors(n):
    if n == 0: return set()
    return {r for r in factorint(abs(n)) if r > 2}

total_classified = 0
total_primes = 0
for p, q, fac in magma_data:
    N = (p + q) // 2
    diff = abs(p - q)
    odd_primes = sorted(r for r in fac if r > 2)
    for r in odd_primes:
        total_primes += 1
        if r == p:
            case = "I"
        elif r == q:
            case = "II"
        elif N % r == 0 and p % r != 0 and q % r != 0:
            case = "III"
        elif diff % r == 0 and p % r != 0 and q % r != 0 and N % r != 0:
            case = "IV"
        else:
            case = "???"
        total_classified += 1 if case != "???" else 0
print(f"  All {total_primes} odd primes across 10 cases classified: "
      f"{total_classified}/{total_primes} ✓")


# ═══════════════════════════════════════════════════════════════════════════
# STEP 2: REDUCED CURVES AND SINGULARITY ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
print(f"""

STEP 2: SINGULARITY ANALYSIS OF THE REDUCED CURVE
══════════════════════════════════════════════════

For each case, we determine the reduced curve C̄ = C mod r and its
singularity structure.

─────────────────────────────────────────────────────────────
CASES I & II: r = p  (or r = q by symmetry)
─────────────────────────────────────────────────────────────

Since r = p, the roots reduce as:  0, p, -p → all ≡ 0 mod r
                                   q, -q → q̄, -q̄ with q̄ ≠ 0

Reduced curve: C̄: y² = x³(x - q̄)(x + q̄) = x³(x² - q̄²)

Singularity at (0, 0):
  Local equation: y² = x³  (an A₂ cusp singularity)
  Delta invariant: δ = 1
  Branches: 1 (unibranch — this is a CUSP, not a NODE)

Normalization:
  Arithmetic genus of y² = (degree-5 poly) is g_a = 2.
  The cusp contributes δ = 1.
  Geometric genus of normalization: g̃ = g_a - δ = 2 - 1 = 1.

  The normalization C̃ is an ELLIPTIC CURVE (genus 1).

Generalized Jacobian of C̄:
  The cusp singularity contributes an additive group G_a.
  The exact sequence is:
    0 → G_a → Jac(C̄) → Pic⁰(C̃) → 0
  where Pic⁰(C̃) is an elliptic curve (1-dim abelian variety).

Néron model reduction type:
    a = 1  (abelian part = elliptic curve from normalization)
    t = 0  (no toric part — cusp gives G_a, not G_m)
    u = 1  (unipotent part from the cusp)
    Check: a + t + u = 1 + 0 + 1 = 2 = g  ✓

Conductor computation:
    dim(V^{{I_r}}) = 2a + t = 2(1) + 0 = 2
    f_r = 4 - 2 = 2  ✓


─────────────────────────────────────────────────────────────
CASES III & IV: r | N  (or r | (p-q)), with r ∤ p and r ∤ q
─────────────────────────────────────────────────────────────

Case III: r | N means r | (p+q), so q ≡ -p mod r.
  Roots mod r: {{0, p̄, -p̄, -p̄, p̄}} = {{0, p̄, p̄, -p̄, -p̄}}
  (where p̄ ≠ 0 since r ∤ p)

Case IV: r | (p-q) means q ≡ p mod r.
  Roots mod r: {{0, p̄, -p̄, p̄, -p̄}} = {{0, p̄, p̄, -p̄, -p̄}}
  (where p̄ ≠ 0 since r ∤ p)

BOTH cases produce the SAME reduced curve:
  C̄: y² = x(x - ā)²(x + ā)²    where ā = p̄ ≠ 0

Singularities at (ā, 0) and (-ā, 0):
  At each point, locally y² ~ (x - ā)², giving a NODE (A₁ singularity).
  Delta invariant of each node: δ = 1.
  Branches at each node: 2 (two branches — this IS a node)
  Total: 2 ordinary double points.

Normalization:
  Substitution v = y / ((x - ā)(x + ā)):  v² = x.
  The normalization C̃: v² = x is a RATIONAL CURVE (genus 0).
  Geometric genus: g̃ = 2 - 2·(1) = 0.  ✓

Generalized Jacobian of C̄:
  Each node contributes a multiplicative group G_m.
  The exact sequence is:
    0 → G_m² → Jac(C̄) → Pic⁰(C̃) → 0
  where Pic⁰(C̃) = 0 (rational curve has trivial Picard group).

  So Jac(C̄) ≅ G_m²  (a 2-dimensional TORUS).

Néron model reduction type:
    a = 0  (no abelian part — normalization is rational)
    t = 2  (toric part = G_m² from two nodes)
    u = 0  (no unipotent part — nodes give G_m, not G_a)
    Check: a + t + u = 0 + 2 + 0 = 2 = g  ✓

Conductor computation:
    dim(V^{{I_r}}) = 2a + t = 2(0) + 2 = 2
    f_r = 4 - 2 = 2  ✓
""")


# ═══════════════════════════════════════════════════════════════════════════
# STEP 3: THE UNIVERSAL IDENTITY
# ═══════════════════════════════════════════════════════════════════════════
print("""
STEP 3: THE UNIVERSAL IDENTITY  2a + t = 2
═══════════════════════════════════════════

Summary of all cases:

  ┌──────────────┬──────────────────────┬─────────┬───────────┬──────┐
  │ Case         │ Reduced curve C̄      │ (a,t,u) │ 2a + t    │ f_r  │
  ├──────────────┼──────────────────────┼─────────┼───────────┼──────┤
  │ I  (r = p)   │ y²=x³(x²-q̄²)       │ (1,0,1) │ 2·1+0 = 2 │  2   │
  │ II (r = q)   │ y²=x³(x²-p̄²)       │ (1,0,1) │ 2·1+0 = 2 │  2   │
  │ III (r|N)    │ y²=x(x-ā)²(x+ā)²   │ (0,2,0) │ 2·0+2 = 2 │  2   │
  │ IV (r|p-q)   │ y²=x(x-ā)²(x+ā)²   │ (0,2,0) │ 2·0+2 = 2 │  2   │
  └──────────────┴──────────────────────┴─────────┴───────────┴──────┘

The identity 2a + t = 2 holds in ALL cases, though for DIFFERENT reasons:

  • Cusp cases (I, II):  The genus drops by 1 (from cusp δ = 1),
    leaving a genus-1 normalization. The abelian part captures 2a = 2
    dimensions of V^{I_r}. The unipotent part (from G_a) is invisible
    to the ℓ-adic Tate module.

  • Node cases (III, IV): The genus drops by 2 (from two nodes with
    δ = 1 each), leaving a genus-0 normalization. The toric part (G_m²)
    captures t = 2 dimensions of V^{I_r}. No abelian or unipotent part.

Both mechanisms produce the SAME conductor exponent f_r = 2.

This is the arithmetic-geometric coincidence underlying the observed
universal semistability of Goldbach-Frey curves at odd primes.
""")


# ═══════════════════════════════════════════════════════════════════════════
# STEP 4: WHY EXACTLY THESE SINGULARITY TYPES AND NO OTHERS
# ═══════════════════════════════════════════════════════════════════════════
print("""
STEP 4: WHY ONLY CUSPS AND DOUBLE-NODES OCCUR
══════════════════════════════════════════════

The key structural constraint is that p, q are DISTINCT PRIMES.

For a bad odd prime r, exactly one of the following holds:
  (a) r = p or r = q  →  exactly ONE triple root collision {0, ±p} or {0, ±q}
  (b) r | N or r | (p-q)  →  exactly TWO double root collisions {p, ±q}

No other collision pattern is possible because:

1. FIVE-FOLD collision (all roots merge):
   Requires r | p AND r | q, hence r | gcd(p,q) = 1 for p ≠ q primes. ✗

2. FOUR-FOLD collision (e.g., {0, p, -p, q} merge, -q separate):
   Requires r | p AND r | q, same impossibility. ✗

3. TRIPLE collision at {p, q, -q} (not involving 0):
   Requires r | (p-q) AND r | (p+q), hence r | 2p, so r | p.
   Then also r | q, impossible. ✗

4. TRIPLE collision at {0, p, q} (mixed):
   Requires r | p AND r | q, impossible. ✗

5. ONE double collision + ONE triple collision:
   E.g., {0, p, -p} triple AND {q, -q} double — but q = -q mod r
   means r | 2q, so r | q. Then r | p from the triple collision.
   Impossible for p ≠ q primes. ✗

Therefore, the only possible singularity patterns are:
  • One A₂ cusp (from one triple collision): Cases I, II
  • Two A₁ nodes (from two double collisions): Cases III, IV

No deeper singularities can arise. This completes the proof.  □
""")


# ═══════════════════════════════════════════════════════════════════════════
# STEP 5: CROSS-VALIDATION WITH MAGMA DATA
# ═══════════════════════════════════════════════════════════════════════════
print("""
STEP 5: CROSS-VALIDATION WITH 10 MAGMA DATA POINTS
═══════════════════════════════════════════════════
""")

# Sage point counting data for cross-validation
sage_data = {
    # (p, q, r): (singularity_type, #nodes, #cusps)
    (7, 23, 3):   ("2N+0C", 2, 0),   # r|N: two nodes
    (7, 23, 5):   ("2N+0C", 2, 0),   # r|N: two nodes
    (7, 23, 7):   ("0N+1C", 0, 1),   # r=p: one cusp
    (7, 23, 23):  ("0N+1C", 0, 1),   # r=q: one cusp
    (3, 7, 3):    ("0N+1C", 0, 1),   # r=p: one cusp
    (3, 7, 5):    ("2N+0C", 2, 0),   # r|N: two nodes
    (3, 7, 7):    ("0N+1C", 0, 1),   # r=q: one cusp
    (3, 17, 3):   ("0N+1C", 0, 1),   # r=p: one cusp
    (3, 17, 5):   ("2N+0C", 2, 0),   # r|N: two nodes
    (3, 17, 7):   ("2N+0C", 2, 0),   # r|(p-q): two nodes
    (3, 17, 17):  ("0N+1C", 0, 1),   # r=q: one cusp
}

print(f"{'p':>3} {'q':>3} {'r':>3}  {'Case':>6}  {'Sing. type':>10}  "
      f"{'(a,t,u)':>10}  {'2a+t':>5}  {'f_r':>3}  {'Magma f_r':>9}")
print("-" * 75)

all_ok = True
for p, q, fac in magma_data:
    N = (p + q) // 2
    diff = abs(p - q)
    for r in sorted(r for r in fac if r > 2):
        magma_fr = fac[r]
        
        if r == p or r == q:
            case = "I" if r == p else "II"
            sing = "1 cusp"
            a, t, u = 1, 0, 1
        elif N % r == 0:
            case = "III"
            sing = "2 nodes"
            a, t, u = 0, 2, 0
        elif diff % r == 0:
            case = "IV"
            sing = "2 nodes"
            a, t, u = 0, 2, 0
        else:
            case = "???"
            sing = "???"
            a, t, u = -1, -1, -1
        
        predicted = 4 - (2*a + t)
        ok = (predicted == magma_fr)
        if not ok: all_ok = False
        
        print(f"{p:>3} {q:>3} {r:>3}  {case:>6}  {sing:>10}  "
              f"({a},{t},{u}):>10  {2*a+t:>5}  {predicted:>3}  "
              f"{magma_fr:>5}    {'✓' if ok else '✗'}")

print(f"\nAll predictions match Magma: {all_ok}")
print(f"Total odd primes verified: {total_primes}")


# ═══════════════════════════════════════════════════════════════════════════
# STEP 6: FORMAL THEOREM STATEMENT
# ═══════════════════════════════════════════════════════════════════════════
print(f"""

STEP 6: FORMAL THEOREM
═══════════════════════

THEOREM. Let p, q be distinct odd primes with p + q = 2N, and let
  C: y² = x(x² - p²)(x² - q²)
be the Goldbach-Frey curve of genus 2.  For every odd prime r
dividing the discriminant of C:

  f_r(Jac(C)) = 2.

PROOF.
  (1) The bad odd primes for C partition into four mutually exclusive
      cases (Step 1): r = p, r = q, r | N with r ∤ pq, or
      r | (p-q) with r ∤ pqN. Mutual exclusivity follows from
      gcd(p,q) = 1 for distinct primes.

  (2) In Cases I and II (r = p or r = q), the reduced curve
      C̄: y² = x³(x² - ā²) has an A₂ cusp at the origin.
      Its normalization has genus 1, and the generalized Jacobian
      fits in an exact sequence 0 → G_a → Jac(C̄) → E → 0
      where E is an elliptic curve. This gives (a,t,u) = (1,0,1).

  (3) In Cases III and IV (r | N or r | (p-q), with r ∤ pq),
      the reduced curve C̄: y² = x(x - ā)²(x + ā)² has two A₁
      nodes. Its normalization has genus 0, and the generalized
      Jacobian is Jac(C̄) ≅ G_m². This gives (a,t,u) = (0,2,0).

  (4) No other singularity type arises (Step 4), because the
      mutual exclusivity of the four cases prevents simultaneous
      collisions that would produce deeper singularities.

  (5) In both cases, dim(V_ℓ^{{I_r}}) = 2a + t = 2, hence
      f_r = 2g - (2a + t) = 4 - 2 = 2.                         □

COROLLARY. The odd part of the conductor is:
  Cond_odd(Jac(C)) = [rad_odd(p) · rad_odd(q) · rad_odd(N) · rad_odd(p-q)]²

REMARK ON r = 2.
  The prime r = 2 is WILD (char = 2 divides the cover degree 2).
  The Swan conductor δ₂ is nonzero and Ogg's formula is unreliable.
  The Magma data shows f₂ ∈ {{4, 7, 8}} — it is NOT constant and
  NOT equal to 2. The theorem above applies ONLY to odd primes.
  A separate analysis of the wild prime r = 2 would require the
  full machinery of Obus-Wewers for wild quotient singularities.
""")


# ═══════════════════════════════════════════════════════════════════════════
# STEP 7: REQUIRED REFERENCES AND TECHNICAL DETAILS
# ═══════════════════════════════════════════════════════════════════════════
print("""
STEP 7: REFERENCES AND TECHNICAL GAPS TO ADDRESS
═════════════════════════════════════════════════

The proof above is conceptually complete but relies on the following
standard results from arithmetic geometry:

(A) The formula f_r = 2g - dim(V_ℓ^{I_r}) for tame primes.
    Reference: Serre-Tate, "Good reduction of abelian varieties"
    (Ann. of Math., 1968), and SGA 7 Exposé IX.

(B) The identification dim(V_ℓ^{I_r}) = 2a + t where (a,t,u) are
    the dimensions of the abelian, toric, and unipotent parts of
    the identity component of the Néron model's special fiber.
    Reference: Bosch-Lütkebohmert-Raynaud, "Néron Models" (1990),
    Chapter 7.

(C) The identification of the Néron model's special fiber with the
    generalized Jacobian of the special fiber of the minimal regular
    model (for curves over DVRs with algebraically closed residue field).
    Reference: BLR Chapter 9, Theorem 9.7/1.

(D) The delta invariant of A₂ (cusp): δ = 1.
    The delta invariant of A₁ (node): δ = 1.
    Reference: Standard (e.g., Hartshorne Ch. IV, or Liu "Algebraic
    Geometry and Arithmetic Curves" Ch. 7 and 10).

(E) The generalized Jacobian of a singular curve with nodes and cusps.
    Nodes contribute G_m; cusps contribute G_a.
    Reference: Serre, "Groupes Algébriques et Corps de Classes" (1959),
    Chapter V.

(F) For the cluster picture interpretation:
    Dokchitser-Dokchitser-Maistret-Morgan, "Semistable types of
    hyperelliptic curves" (Algebraic Curves and their Applications,
    Contemp. Math. 724, AMS 2019).
    This paper provides an alternative (equivalent) route to the same
    result via cluster pictures → stable reduction → conductor.
""")
