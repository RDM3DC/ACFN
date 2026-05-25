# ACFN Proof and Solution Package

**Repository:** ACFN  
**Canonical Core Arm:** 06  
**Date:** 2026-05-25  
**Status:** Mathematical working draft

---

## 0. Purpose

Adaptive Curvature Flow Networks (ACFN) extend ARP by allowing geometry to evolve with adaptive flow.

This document proves the first rigorous core of ACFN:

1. conductance positivity,
2. bounded conductance under bounded forcing,
3. curvature decay in the unforced case,
4. curvature smoothing under diffusion-relaxation,
5. constant-input equilibria,
6. stability of a reduced conductance-curvature model,
7. energy dissipation for the scalar curvature equation,
8. graph/network versions of the same results,
9. links to PMT, EPM, and ACST.

---

## 1. Minimal Scalar ACFN System

The scalar ACFN prototype is

```text
dG/dt = α|I| − μG + λ|∇κ|
```

```text
∂κ/∂t = η ∇·(G∇κ) − βκ
```

where:

- `G ≥ 0` is adaptive conductance or transport capacity,
- `I` is flow/current/intensity,
- `κ` is curvature or curvature proxy,
- `α, μ, η, β ≥ 0`,
- `λ ≥ 0` couples curvature gradients back into adaptation.

The central loop is:

```text
flow → conductance → curvature transport → geometry memory → future flow
```

---

## 2. Theorem: Conductance Positivity

### Statement

If

```text
G(0) ≥ 0,
α ≥ 0,
μ > 0,
λ ≥ 0,
```

and `|I|, |∇κ| ≥ 0`, then the solution of

```text
dG/dt = α|I| − μG + λ|∇κ|
```

satisfies

```text
G(t) ≥ 0
```

for all `t ≥ 0`.

### Proof

At the boundary `G=0`,

```text
dG/dt = α|I| + λ|∇κ| ≥ 0.
```

Therefore the vector field points inward or tangent to the nonnegative half-line. A trajectory starting at `G ≥ 0` cannot cross into `G < 0`.

QED.

---

## 3. Theorem: Conductance Boundedness Under Bounded Forcing

### Statement

Let

```text
F(t) = α|I(t)| + λ|∇κ(t)|.
```

If

```text
0 ≤ F(t) ≤ F_max
```

then

```text
G(t) ≤ e^{-μt}G(0) + (F_max/μ)(1 − e^{-μt}).
```

In particular,

```text
limsup_{t→∞} G(t) ≤ F_max/μ.
```

### Proof

The equation is

```text
dG/dt + μG = F(t).
```

Using the integrating factor `e^{μt}`:

```text
G(t) = e^{-μt}G(0) + ∫0^t e^{-μ(t-s)}F(s)ds.
```

Since `F(s) ≤ F_max`,

```text
G(t) ≤ e^{-μt}G(0) + F_max∫0^t e^{-μ(t-s)}ds.
```

The integral is `(1 − e^{-μt})/μ`, so

```text
G(t) ≤ e^{-μt}G(0) + (F_max/μ)(1 − e^{-μt}).
```

QED.

---

## 4. Constant-Forcing Conductance Solution

If `I=I0` and `|∇κ|=K0` are constant, then

```text
F0 = α|I0| + λK0.
```

The exact solution is

```text
G(t) = G* + (G(0) − G*)e^{-μt}
```

where

```text
G* = F0/μ = (α|I0| + λK0)/μ.
```

This is the ACFN extension of the classic ARP equilibrium.

---

## 5. Curvature Energy Dissipation for Fixed Conductance

Assume `G(x)` is fixed and bounded below:

```text
G(x) ≥ G_min > 0.
```

Consider

```text
∂κ/∂t = η ∇·(G∇κ) − βκ
```

on a domain with periodic or no-flux boundary conditions.

Define curvature energy

```text
Eκ(t) = 1/2 ∫ κ² dx.
```

### Theorem

```text
dEκ/dt = −η∫ G|∇κ|² dx − β∫κ² dx ≤ 0.
```

### Proof

Differentiate:

```text
dEκ/dt = ∫κ ∂κ/∂t dx.
```

Substitute the PDE:

```text
dEκ/dt = η∫κ ∇·(G∇κ) dx − β∫κ² dx.
```

Integrate by parts. Boundary terms vanish under periodic or no-flux conditions:

```text
∫κ ∇·(G∇κ) dx = −∫ G|∇κ|² dx.
```

Therefore

```text
dEκ/dt = −η∫ G|∇κ|² dx − β∫κ² dx ≤ 0.
```

QED.

### Interpretation

In fixed-conductance ACFN, curvature roughness and curvature magnitude decay unless driven by adaptive forcing.

---

## 6. Maximum-Principle Bound for Curvature Relaxation

If `G` is constant, the curvature equation becomes

```text
∂κ/∂t = ηG Δκ − βκ.
```

For periodic or no-flux boundaries,

```text
||κ(t)||∞ ≤ e^{-βt} ||κ(0)||∞.
```

### Proof Sketch

At a positive spatial maximum, `Δκ ≤ 0`, so

```text
∂κ/∂t ≤ −βκ.
```

At a negative spatial minimum, apply the same argument to `−κ`.

Thus the maximum magnitude decays at least as fast as `e^{-βt}`.

QED.

---

## 7. Reduced 0D Conductance-Curvature Model

A minimal finite-dimensional model is

```text
dG/dt = αI0 − μG + λK
```

```text
dK/dt = qG − βK
```

where `K ≥ 0` is a scalar curvature-activity proxy.

### Equilibrium

Set derivatives to zero:

```text
0 = αI0 − μG* + λK*
```

```text
0 = qG* − βK*.
```

From the second equation:

```text
K* = qG*/β.
```

Substitute into the first:

```text
0 = αI0 − μG* + λqG*/β.
```

Therefore

```text
G* = αI0 / (μ − λq/β)
```

```text
K* = qG*/β.
```

### Existence Condition

A positive finite equilibrium exists when

```text
I0 > 0
```

and

```text
μβ > λq.
```

### Stability

The system matrix for perturbations is

```text
A = [[−μ,  λ ],
     [ q, −β ]].
```

Trace:

```text
tr(A)=−(μ+β)<0.
```

Determinant:

```text
det(A)=μβ−λq.
```

Thus the equilibrium is linearly stable when

```text
μβ > λq.
```

QED.

### Interpretation

Stable ACFN feedback requires relaxation to dominate curvature-amplified conductance feedback.

The solved stability condition is:

```text
μβ > λq.
```

---

## 8. Graph ACFN Model

On a graph with node curvature `κ_v` and edge conductance `G_uv`, use

```text
dκ_v/dt = η Σ_{u~v} G_uv(κ_u − κ_v) − βκ_v.
```

This can be written

```text
dκ/dt = −η L_G κ − βκ
```

where `L_G` is the weighted graph Laplacian.

### Theorem: Graph Curvature Energy Decays

Define

```text
Eκ = 1/2 Σ_v κ_v².
```

If `G_uv ≥ 0`, then

```text
dEκ/dt = −η/2 Σ_{u~v} G_uv(κ_u − κ_v)² − βΣ_v κ_v² ≤ 0.
```

### Proof

Using `dκ/dt = −ηL_Gκ − βκ`,

```text
dEκ/dt = κ^T dκ/dt
       = −η κ^T L_G κ − β κ^Tκ.
```

For a weighted graph Laplacian,

```text
κ^T L_G κ = 1/2 Σ_{u~v} G_uv(κ_u − κ_v)² ≥ 0.
```

Therefore energy decays.

QED.

---

## 9. Adaptive Geodesic Cost

ACFN path cost can be modeled as

```text
C[path] = ∫ [1 + a|κ| − bG − cM] ds.
```

A learned route becomes favorable when

```text
bG + cM > a|κ|.
```

This is the first solved route-preference inequality.

Interpretation:

- `a|κ|` penalizes curvature/stress,
- `bG` rewards conductance/adaptation,
- `cM` rewards memory reinforcement.

---

## 10. ACST Accounting for ACFN Conductance Mass

Define total conductance mass:

```text
Q_G = ∫ G dx.
```

From

```text
dG/dt = α|I| − μG + λ|∇κ|,
```

we get

```text
dQ_G/dt = α∫|I|dx − μQ_G + λ∫|∇κ|dx.
```

This is an ACST law:

```text
adaptive quantity = input + curvature source − decay.
```

If memory is included:

```text
dG/dt = α|I| − μG + λ|∇κ| + σM,
```

then

```text
dQ_G/dt = α∫|I|dx − μQ_G + λ∫|∇κ|dx + σ∫Mdx.
```

---

## 11. Coupling to PMT

PMT introduces phase transport:

```text
∂θ_R/∂t = ω − γ∇·(G∇θ_R).
```

Thus ACFN supplies the adaptive geometry/conductance field `G` through which PMT transports resolved phase.

ACFN + PMT loop:

```text
phase → memory → conductance → curvature → future phase
```

---

## 12. Coupling to EPM

EPM uses curvature and memory in an effective potential:

```text
r(x,t) = V0 + uκ − vM.
```

ACFN supplies `κ` and can therefore create, move, or relax the geometric traps in which EPM structures form.

EPM structure condition:

```text
vM > V0 + uκ.
```

ACFN affects this threshold through `κ`.

---

## 13. What Is Solved So Far

### Proven

- conductance positivity,
- conductance boundedness under bounded forcing,
- exact constant-forcing solution,
- curvature energy dissipation,
- maximum-principle curvature decay for constant conductance,
- reduced conductance-curvature equilibrium,
- reduced stability condition,
- graph curvature energy decay,
- adaptive geodesic route-preference inequality,
- ACST accounting law for total conductance.

### Solved conditions

Conductance equilibrium:

```text
G* = (α|I0| + λK0)/μ.
```

Reduced ACFN equilibrium:

```text
G* = αI0/(μ − λq/β)
```

```text
K* = qG*/β.
```

Reduced stability:

```text
μβ > λq.
```

Route preference:

```text
bG + cM > a|κ|.
```

Curvature energy decay:

```text
dEκ/dt ≤ 0.
```

---

## 14. What Is Still Open

1. Full Ricci-style tensor version of ACFN.
2. Global existence for fully coupled `G,κ,M,θ,Φ` fields.
3. Graph curvature choice: Forman-Ricci vs Ollivier-Ricci vs Laplacian proxy.
4. Topology-change thresholds.
5. Numerical stability limits for explicit 2D solvers.
6. Rigorous adaptive geodesic convergence.

---

## 15. Summary

The first solved mathematical core of ACFN is:

```text
adaptive conductance remains positive and bounded under bounded forcing;
curvature diffusion-relaxation dissipates energy;
stable conductance-curvature feedback requires relaxation to dominate reinforcement.
```

The flagship ACFN stability condition is:

```text
μβ > λq.
```

The flagship field system is:

```text
dG/dt = α|I| − μG + λ|∇κ|
```

```text
∂κ/∂t = η∇·(G∇κ) − βκ.
```

This gives ACFN a rigorous first foundation as the dynamic-geometry arm of Canonical Core.
