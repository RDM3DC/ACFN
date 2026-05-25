import unittest

from acfn import (
    ACFNParameters,
    TensorField,
    adaptive_stress,
    all_finite,
    curvature_energy,
    evolve_step,
    identity_metric,
    uniform_field,
    zero_tensor,
)


class ACFNTests(unittest.TestCase):
    def test_adaptive_stress_detects_conductance_gradient(self):
        conductance = [
            [0.0, 1.0, 2.0],
            [0.0, 1.0, 2.0],
            [0.0, 1.0, 2.0],
        ]

        stress = adaptive_stress(conductance)

        self.assertGreater(stress.xx[1][1], 0.0)
        self.assertEqual(stress.yy[1][1], 0.0)

    def test_evolve_step_accumulates_memory_and_keeps_metric_finite(self):
        width = 5
        height = 5
        conductance = [[float(column_index) for column_index in range(width)] for _ in range(height)]
        metric = identity_metric(width, height)
        memory = zero_tensor(width, height)
        usage = TensorField(
            xx=uniform_field(width, height, 0.0),
            xy=uniform_field(width, height, 0.0),
            yy=uniform_field(width, height, 0.0),
        )
        usage.yy[2][2] = 4.0
        parameters = ACFNParameters(dt=0.05, eta_memory=0.5)

        metric_next, memory_next = evolve_step(metric, conductance, memory, usage, parameters)

        self.assertTrue(all_finite(metric_next))
        self.assertGreater(memory_next.yy[2][2], 0.0)
        self.assertGreater(metric_next.yy[2][2], metric.yy[2][2])

    def test_curvature_diffusion_reduces_isolated_metric_spike(self):
        width = 5
        height = 5
        metric = identity_metric(width, height)
        metric.xx[2][2] = 4.0
        conductance = uniform_field(width, height, 1.0)
        memory = zero_tensor(width, height)
        usage = zero_tensor(width, height)
        parameters = ACFNParameters(
            dt=0.05,
            lambda_stress=0.0,
            eta_memory=0.0,
            curvature_diffusion=0.5,
        )

        energy_before = curvature_energy(metric)
        metric_next, _ = evolve_step(metric, conductance, memory, usage, parameters)
        energy_after = curvature_energy(metric_next)

        self.assertLess(metric_next.xx[2][2], metric.xx[2][2])
        self.assertLess(energy_after, energy_before)


if __name__ == "__main__":
    unittest.main()
