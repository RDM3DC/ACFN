# 6th Arm - Adaptive Curvature Flow Networks

Adaptive Curvature Flow (ACF) and Adaptive Curvature Flow Networks (ACFN) are the same branch of the framework. ACF is the equation-level idea; ACFN is the practical network form and the canonical name for the 6th arm.

> ARP does not just adapt flow.  
> ARP adapts the geometry that flow moves through.

This makes the 6th arm the dynamic-geometry layer of Canonical Core: a system where flow, memory, phase structure, and curvature co-evolve instead of living on a fixed background.

## Canonical Lineage

This local prototype is aligned with the public `RDM3DC/canonical-core` framing:

1. **ARP/AIN** supplies adaptive conductance, impedance, and reinforcement/decay dynamics.
2. **Adaptive-pi Geometry** supplies the idea that phase-period geometry can be a field.
3. **Curve Memory** supplies historical path dependence.
4. **Phase-Lift / PROs** supplies branch-aware phase continuity.
5. **QPS-GR Mapping** supplies the engineering bridge to spacetime-style interpretation.
6. **ACFN** adds dynamic curvature as an active state variable.

Later Canonical Core arms then build on ACFN: **PMT** transports phase-memory through adaptive geometry, **EPM** studies stable emergent structures, and **ACST** tracks quasi-conserved quantities across the adaptive stack.

## Core Evolution Law

The conceptual update extends Ricci flow:

```math
\frac{\partial g_{ij}}{\partial t} = -2R_{ij} + \lambda A_{ij} + \eta M_{ij}
```

Where:

- `g_ij` is the local metric tensor.
- `R_ij` is a curvature tensor or discrete curvature proxy.
- `A_ij` is adaptive stress.
- `M_ij` is geometric memory.
- `lambda` controls stress coupling.
- `eta` controls memory coupling.

The first stress tensor can be defined from ARP conductance `G`:

```math
A_{ij} = \nabla_i G \nabla_j G
```

The memory tensor is a decayed accumulation of historical curvature usage:

```math
M_{ij}(t) = \int_0^t K_{ij}(\tau)e^{-\mu(t-\tau)}d\tau
```

In a discrete engine this becomes:

```math
M_{ij}^{t+1} = e^{-\mu\Delta t}M_{ij}^{t} + \Delta tK_{ij}^{t}
```

## ACFN Interpretation

ACFN treats a manifold as a computational network whose nodes carry local geometry. Flow through the network changes the local metric, and the changed metric alters future routing.

In the scalar canonical form, the recurring state variables are:

- `G`: adaptive conductance or generalized transport capacity;
- `I`: flow, intensity, current, traffic, or signal load;
- `kappa`: curvature field;
- `M`: accumulated memory field;
- `theta`: phase field when coupled to Phase-Memory Transport Theory.

One compact grid recipe is:

```text
for each time step:
    I = solve_flow(G, sources, sinks)
    G += dt*(alpha*abs(I) - mu*G + lambda*abs(grad(kappa)))
    kappa += dt*(eta*div(G*grad(kappa)) - beta*kappa)
```

This repo's first executable prototype uses a symmetric 2D metric tensor instead of a scalar `kappa` field. That keeps the original ACF equation visible while remaining compatible with the canonical network interpretation.

This gives the branch a practical computational form:

- frequently used geodesics deepen;
- unstable routes flatten;
- resonance corridors can form;
- curvature can stabilize around repeated traffic;
- routing becomes hysteretic because geometry remembers.

## Minimal Computational State

A first ACFN cell can carry:

- `G`: ARP conductance field;
- `g_xx`, `g_xy`, `g_yy`: local symmetric 2D metric tensor;
- `A_xx`, `A_xy`, `A_yy`: adaptive stress from conductance gradients;
- `M_xx`, `M_xy`, `M_yy`: decayed memory tensor;
- `K_xx`, `K_xy`, `K_yy`: current usage or curvature-history input.

The prototype in [acfn.py](acfn.py) implements this toy update on a 2D grid:

```text
metric_next = metric
            + dt * curvature_diffusion * laplacian(metric)
            + dt * lambda_stress * adaptive_stress(conductance)
            + dt * eta_memory * memory_next
```

The curvature term is intentionally a discrete smoothing proxy, not a full Ricci tensor. The goal is to create a stable first engine that can later be replaced by richer differential geometry or graph curvature operators.

## Framework Role

ACFN unifies the earlier arms at the geometry-feedback layer:

| Existing idea | ACFN role |
| --- | --- |
| ARP/AIN | adaptive conductance, impedance, and stress source |
| Adaptive-pi | local phase-period geometry |
| Curve Memory | geometric memory tensor |
| QPS | adaptive phase routing through learned geometry |
| RealignR | optimization inside an evolving metric |
| CAD/manifold work | evolving surfaces and strain-sensitive topology |

The central loop becomes:

```text
flow -> conductance -> curvature -> memory -> effective geometry -> future flow
```

When coupled to PMT, the loop extends to:

```text
phase -> memory -> adaptation -> geometry -> future phase
```

## Immediate Research Directions

1. Replace the grid curvature proxy with Ollivier-Ricci, Forman-Ricci, or Laplace-Beltrami operators on graphs.
2. Couple `K_ij` to actual path usage from ARP/QPS simulations.
3. Add phase tension as a separate tensor term `P_ij`.
4. Track topology events when strain crosses thresholds.
5. Compare routing before and after memory accumulation to measure geometric learning.
