# Universal Tame Semistability of Goldbach–Frey Jacobians

**Paper #13 in the Titan Project series**

A proof that f_r = 2 at all odd primes for the Goldbach–Frey curve.

## Key Result

**Theorem.** For the Goldbach–Frey curve C: y² = x(x² − p²)(x² − q²) with p ≠ q distinct odd primes, p + q = 2N, the conductor exponent at every bad odd prime r equals exactly 2:

```
f_r(Jac(C)) = 2
```

The proof classifies bad odd primes into four mutually exclusive cases:

| Case | Condition | Reduced curve | Singularity | (a,t,u) | f_r |
|------|-----------|---------------|-------------|---------|-----|
| I    | r = p     | y² = x³(x²−q̄²) | 1 cusp (A₂) | (1,0,1) | 2 |
| II   | r = q     | y² = x³(x²−p̄²) | 1 cusp (A₂) | (1,0,1) | 2 |
| III  | r \| N    | y² = x(x−ā)²(x+ā)² | 2 nodes (A₁) | (0,2,0) | 2 |
| IV   | r \| (p−q) | y² = x(x−ā)²(x+ā)² | 2 nodes (A₁) | (0,2,0) | 2 |

Two geometrically distinct mechanisms conspire to produce the same identity 2a + t = 2.

**Corollary.** Cond_odd(Jac(C)) = [rad_odd(p · q · N · (p−q))]²

## Repository Structure

```
├── paper/
│   ├── Universal_Tame_Semistability.tex
│   └── Universal_Tame_Semistability.pdf   (6 pages)
├── figures/
│   ├── fig_classification.pdf
│   ├── fig_proof_diagram.pdf
│   └── (PNG versions)
├── scripts/
│   ├── fig_proof.py                       Figure generation
│   └── proof_fr2_scheme.py                Computational proof verification
├── README.md
└── LICENSE
```

## Series Context

| # | Paper | DOI |
|---|-------|-----|
| 10 | Dynamic Stability (BSL) | [10.5281/zenodo.18724884](https://zenodo.org/records/18724884) |
| 11 | Ternary Conductor Boundary | [10.5281/zenodo.18727994](https://zenodo.org/records/18727994) |
| 12 | True Conductor Validation | [10.5281/zenodo.18749731](https://zenodo.org/records/18749731) |
| **13** | **Universal Tame Semistability** | *this paper* |

## License

MIT
