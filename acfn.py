"""Toy Adaptive Curvature Flow Network engine.

This module is intentionally small and dependency-free. It models the ACFN idea on a
2D grid where each cell has a symmetric metric tensor and decayed memory tensor.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite


ScalarField = list[list[float]]


@dataclass(frozen=True)
class TensorField:
    """Symmetric 2D tensor field with components xx, xy, yy."""

    xx: ScalarField
    xy: ScalarField
    yy: ScalarField


@dataclass(frozen=True)
class ACFNParameters:
    """Coupling constants for one explicit ACFN update."""

    dt: float = 0.05
    lambda_stress: float = 0.8
    eta_memory: float = 0.25
    memory_decay: float = 0.3
    curvature_diffusion: float = 0.2
    metric_floor: float = 0.05
    metric_ceiling: float = 10.0


def uniform_field(width: int, height: int, value: float) -> ScalarField:
    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive")
    return [[float(value) for _ in range(width)] for _ in range(height)]


def identity_metric(width: int, height: int) -> TensorField:
    return TensorField(
        xx=uniform_field(width, height, 1.0),
        xy=uniform_field(width, height, 0.0),
        yy=uniform_field(width, height, 1.0),
    )


def zero_tensor(width: int, height: int) -> TensorField:
    return TensorField(
        xx=uniform_field(width, height, 0.0),
        xy=uniform_field(width, height, 0.0),
        yy=uniform_field(width, height, 0.0),
    )


def adaptive_stress(conductance: ScalarField) -> TensorField:
    """Build A_ij = grad_i(G) grad_j(G) from a conductance grid."""

    width, height = _shape(conductance)
    stress_xx = uniform_field(width, height, 0.0)
    stress_xy = uniform_field(width, height, 0.0)
    stress_yy = uniform_field(width, height, 0.0)

    for row_index in range(height):
        for column_index in range(width):
            gradient_x, gradient_y = _gradient(conductance, column_index, row_index)
            stress_xx[row_index][column_index] = gradient_x * gradient_x
            stress_xy[row_index][column_index] = gradient_x * gradient_y
            stress_yy[row_index][column_index] = gradient_y * gradient_y

    return TensorField(xx=stress_xx, xy=stress_xy, yy=stress_yy)


def update_memory(memory: TensorField, usage: TensorField, parameters: ACFNParameters) -> TensorField:
    """Apply M_next = exp(-mu dt) M + dt K."""

    _assert_same_tensor_shape(memory, usage)
    decay = exp(-parameters.memory_decay * parameters.dt)
    return _map_tensor_pair(
        memory,
        usage,
        lambda old_value, usage_value: decay * old_value + parameters.dt * usage_value,
    )


def evolve_step(
    metric: TensorField,
    conductance: ScalarField,
    memory: TensorField,
    usage: TensorField,
    parameters: ACFNParameters | None = None,
) -> tuple[TensorField, TensorField]:
    """Advance one explicit ACFN step and return (metric_next, memory_next)."""

    active_parameters = parameters or ACFNParameters()
    _validate_parameters(active_parameters)
    _assert_tensor_matches_field(metric, conductance)
    _assert_same_tensor_shape(metric, memory)
    _assert_same_tensor_shape(metric, usage)

    stress = adaptive_stress(conductance)
    memory_next = update_memory(memory, usage, active_parameters)

    metric_next = TensorField(
        xx=_update_component(metric.xx, stress.xx, memory_next.xx, active_parameters, diagonal=True),
        xy=_update_component(metric.xy, stress.xy, memory_next.xy, active_parameters, diagonal=False),
        yy=_update_component(metric.yy, stress.yy, memory_next.yy, active_parameters, diagonal=True),
    )
    return metric_next, memory_next


def curvature_energy(metric: TensorField) -> float:
    """Return a simple scalar roughness measure for the metric field."""

    total = 0.0
    width, height = _shape(metric.xx)
    for component in (metric.xx, metric.xy, metric.yy):
        laplacian = _laplacian(component)
        for row_index in range(height):
            for column_index in range(width):
                value = laplacian[row_index][column_index]
                total += value * value
    return total / (width * height)


def all_finite(tensor: TensorField) -> bool:
    for component in (tensor.xx, tensor.xy, tensor.yy):
        for row in component:
            for value in row:
                if not isfinite(value):
                    return False
    return True


def _update_component(
    component: ScalarField,
    stress: ScalarField,
    memory: ScalarField,
    parameters: ACFNParameters,
    *,
    diagonal: bool,
) -> ScalarField:
    width, height = _shape(component)
    laplacian = _laplacian(component)
    updated = uniform_field(width, height, 0.0)

    for row_index in range(height):
        for column_index in range(width):
            delta = (
                parameters.curvature_diffusion * laplacian[row_index][column_index]
                + parameters.lambda_stress * stress[row_index][column_index]
                + parameters.eta_memory * memory[row_index][column_index]
            )
            value = component[row_index][column_index] + parameters.dt * delta
            if diagonal:
                value = min(parameters.metric_ceiling, max(parameters.metric_floor, value))
            else:
                value = min(parameters.metric_ceiling, max(-parameters.metric_ceiling, value))
            updated[row_index][column_index] = value

    return updated


def _laplacian(field: ScalarField) -> ScalarField:
    width, height = _shape(field)
    result = uniform_field(width, height, 0.0)
    for row_index in range(height):
        for column_index in range(width):
            center = field[row_index][column_index]
            left = field[row_index][max(0, column_index - 1)]
            right = field[row_index][min(width - 1, column_index + 1)]
            up = field[max(0, row_index - 1)][column_index]
            down = field[min(height - 1, row_index + 1)][column_index]
            result[row_index][column_index] = left + right + up + down - 4.0 * center
    return result


def _gradient(field: ScalarField, column_index: int, row_index: int) -> tuple[float, float]:
    width, height = _shape(field)
    left_column = max(0, column_index - 1)
    right_column = min(width - 1, column_index + 1)
    up_row = max(0, row_index - 1)
    down_row = min(height - 1, row_index + 1)

    horizontal_span = max(1, right_column - left_column)
    vertical_span = max(1, down_row - up_row)
    gradient_x = (field[row_index][right_column] - field[row_index][left_column]) / horizontal_span
    gradient_y = (field[down_row][column_index] - field[up_row][column_index]) / vertical_span
    return gradient_x, gradient_y


def _map_tensor_pair(left: TensorField, right: TensorField, mapper) -> TensorField:
    return TensorField(
        xx=_map_field_pair(left.xx, right.xx, mapper),
        xy=_map_field_pair(left.xy, right.xy, mapper),
        yy=_map_field_pair(left.yy, right.yy, mapper),
    )


def _map_field_pair(left: ScalarField, right: ScalarField, mapper) -> ScalarField:
    width, height = _shape(left)
    _assert_same_field_shape(left, right)
    result = uniform_field(width, height, 0.0)
    for row_index in range(height):
        for column_index in range(width):
            result[row_index][column_index] = mapper(
                left[row_index][column_index], right[row_index][column_index]
            )
    return result


def _shape(field: ScalarField) -> tuple[int, int]:
    if not field or not field[0]:
        raise ValueError("fields must be non-empty rectangular grids")
    width = len(field[0])
    for row in field:
        if len(row) != width:
            raise ValueError("fields must be rectangular")
    return width, len(field)


def _assert_same_field_shape(left: ScalarField, right: ScalarField) -> None:
    if _shape(left) != _shape(right):
        raise ValueError("field shapes must match")


def _assert_same_tensor_shape(left: TensorField, right: TensorField) -> None:
    if _shape(left.xx) != _shape(left.xy) or _shape(left.xx) != _shape(left.yy):
        raise ValueError("left tensor components must have matching shapes")
    if _shape(right.xx) != _shape(right.xy) or _shape(right.xx) != _shape(right.yy):
        raise ValueError("right tensor components must have matching shapes")
    if _shape(left.xx) != _shape(right.xx):
        raise ValueError("tensor shapes must match")


def _assert_tensor_matches_field(tensor: TensorField, field: ScalarField) -> None:
    if _shape(tensor.xx) != _shape(tensor.xy) or _shape(tensor.xx) != _shape(tensor.yy):
        raise ValueError("tensor components must have matching shapes")
    if _shape(tensor.xx) != _shape(field):
        raise ValueError("tensor and field shapes must match")


def _validate_parameters(parameters: ACFNParameters) -> None:
    if parameters.dt <= 0.0:
        raise ValueError("dt must be positive")
    if parameters.memory_decay < 0.0:
        raise ValueError("memory_decay cannot be negative")
    if parameters.metric_floor <= 0.0:
        raise ValueError("metric_floor must be positive")
    if parameters.metric_ceiling <= parameters.metric_floor:
        raise ValueError("metric_ceiling must be greater than metric_floor")
