"""
Reduced Adaptive Curvature Flow Networks (ACFN) solver.

This solves the finite-dimensional conductance-curvature feedback model:

    dG/dt = alpha*I0 - mu*G + lambda_coupling*K
    dK/dt = q*G - beta*K

The equilibrium is:

    G* = alpha*I0 / (mu - lambda_coupling*q/beta)
    K* = q*G*/beta

The stability condition is:

    mu*beta > lambda_coupling*q

Run:
    python examples/reduced_acfn_solver.py
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReducedACFNParameters:
    alpha: float = 1.0
    input_current: float = 0.4
    mu: float = 0.8
    lambda_coupling: float = 0.15
    q: float = 0.4
    beta: float = 0.7
    dt: float = 0.002
    steps: int = 12000
    initial_g: float = 0.05
    initial_k: float = 0.0


def equilibrium(p: ReducedACFNParameters) -> dict[str, float | bool]:
    denominator = p.mu - (p.lambda_coupling * p.q / p.beta)
    exists = p.input_current > 0.0 and denominator > 0.0
    if not exists:
        return {"exists": False, "G_star": 0.0, "K_star": 0.0}

    g_star = p.alpha * p.input_current / denominator
    k_star = p.q * g_star / p.beta
    return {"exists": True, "G_star": g_star, "K_star": k_star}


def stability_condition(p: ReducedACFNParameters) -> dict[str, float | bool]:
    trace = -(p.mu + p.beta)
    determinant = p.mu * p.beta - p.lambda_coupling * p.q
    return {
        "trace": trace,
        "determinant": determinant,
        "stable": trace < 0.0 and determinant > 0.0,
        "stability_margin_mu_beta_minus_lambda_q": determinant,
    }


def run_solver(params: ReducedACFNParameters | None = None) -> dict[str, float | bool]:
    p = params or ReducedACFNParameters()

    g = max(0.0, p.initial_g)
    k = max(0.0, p.initial_k)

    max_g = g
    max_k = k

    for _ in range(p.steps):
        dg = p.alpha * p.input_current - p.mu * g + p.lambda_coupling * k
        dk = p.q * g - p.beta * k

        g = max(0.0, g + p.dt * dg)
        k = max(0.0, k + p.dt * dk)

        max_g = max(max_g, g)
        max_k = max(max_k, k)

    eq = equilibrium(p)
    stable = stability_condition(p)

    g_star = float(eq["G_star"])
    k_star = float(eq["K_star"])
    distance_to_equilibrium = ((g - g_star) ** 2 + (k - k_star) ** 2) ** 0.5

    return {
        **eq,
        **stable,
        "final_G": g,
        "final_K": k,
        "max_G": max_g,
        "max_K": max_k,
        "distance_to_equilibrium": distance_to_equilibrium,
    }


if __name__ == "__main__":
    result = run_solver()
    print("Reduced ACFN solver complete")
    for key, value in result.items():
        if isinstance(value, bool):
            print(f"{key}: {value}")
        else:
            print(f"{key}: {value:.8f}")
