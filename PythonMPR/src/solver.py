from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class Constraint:
    a: float
    b: float
    c: float
    typ: int  # 1 for <=, -1 for >=


class LppProblem:
    """Object representation of a linear programming problem in two variables."""

    def __init__(self,
                 constraints: Optional[List[Constraint]] = None,
                 objective: Tuple[float, float] = (0.0, 0.0),
                 maximize: bool = True):
        self.constraints = constraints or []
        self.objective = objective
        self.maximize = maximize

    def add_constraint(self, a: float, b: float, c: float, typ: int):
        self.constraints.append(Constraint(a, b, c, typ))

    def is_point_feasible(self, x: float, y: float) -> bool:
        for constraint in self.constraints:
            lhs = constraint.a * x + constraint.b * y
            if constraint.typ == 1 and lhs > constraint.c + 1e-9:
                return False
            if constraint.typ == -1 and lhs < constraint.c - 1e-9:
                return False
        return True

    def all_candidate_points(self) -> List[Tuple[float, float]]:
        points: List[Tuple[float, float]] = []

        # Origin
        if self.is_point_feasible(0.0, 0.0):
            points.append((0.0, 0.0))

        # Axis intersections
        for constraint in self.constraints:
            if abs(constraint.a) > 1e-12:
                x = constraint.c / constraint.a
                if x >= -1e-9 and self.is_point_feasible(x, 0.0):
                    points.append((x, 0.0))

            if abs(constraint.b) > 1e-12:
                y = constraint.c / constraint.b
                if y >= -1e-9 and self.is_point_feasible(0.0, y):
                    points.append((0.0, y))

        # Pairwise intersections
        n = len(self.constraints)
        for i in range(n):
            c1 = self.constraints[i]
            for j in range(i + 1, n):
                c2 = self.constraints[j]
                det = c1.a * c2.b - c2.a * c1.b
                if abs(det) < 1e-12:
                    continue

                x = (c1.c * c2.b - c2.c * c1.b) / det
                y = (c1.a * c2.c - c2.a * c1.c) / det

                if x >= -1e-9 and y >= -1e-9 and self.is_point_feasible(x, y):
                    points.append((x, y))

        # Deduplicate
        unique_points = []
        seen = set()
        for x, y in points:
            rounded = (round(x, 9), round(y, 9))
            if rounded not in seen:
                seen.add(rounded)
                unique_points.append((x, y))

        return unique_points

    def solve(self) -> Tuple[Optional[Tuple[float, float]], Optional[float]]:
        candidates = self.all_candidate_points()
        if not candidates:
            return None, None

        best_point = None
        best_val = None

        for x, y in candidates:
            val = self.objective[0] * x + self.objective[1] * y
            if best_val is None:
                best_val = val
                best_point = (x, y)
            elif self.maximize and val > best_val:
                best_val = val
                best_point = (x, y)
            elif not self.maximize and val < best_val:
                best_val = val
                best_point = (x, y)

        # Check simplified unbounded scenario
        if best_point is None:
            return None, None

        return best_point, best_val


def solve_lpp(constraints: List[Tuple[float, float, float, int]],
              objective: Tuple[float, float],
              maximize: bool = True) -> Tuple[Optional[Tuple[float, float]], Optional[float]]:
    problem = LppProblem(
        constraints=[Constraint(a, b, c, typ) for (a, b, c, typ) in constraints],
        objective=objective,
        maximize=maximize
    )
    return problem.solve()
