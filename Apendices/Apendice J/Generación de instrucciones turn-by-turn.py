from typing import List, Tuple
import math

Point = Tuple[float, float]

def _wrap_pi(a: float) -> float:
    while a <= -math.pi:
        a += 2.0 * math.pi
    while a > math.pi:
        a -= 2.0 * math.pi
    return a

def _heading(a: Point, b: Point) -> float:
    return math.atan2(b[1] - a[1], b[0] - a[0])

def generate_instructions(points: List[Point],
                          cell_size_m: float,
                          tau_straight_deg: float = 15.0,
                          tau_turn_deg: float = 45.0,
                          tau_uturn_deg: float = 150.0) -> List[str]:
    if len(points) < 2:
        return []

    tau_straight = math.radians(tau_straight_deg)
    tau_turn = math.radians(tau_turn_deg)
    tau_uturn = math.radians(tau_uturn_deg)

    instr: List[str] = []
    prev_theta = _heading(points[0], points[1])
    acc = 0.0

    for k in range(1, len(points) - 1):
        theta = _heading(points[k], points[k+1])
        dtheta = _wrap_pi(theta - prev_theta)

        seg = math.hypot(points[k][0] - points[k-1][0],
                         points[k][1] - points[k-1][1]) * cell_size_m
        acc += seg

        if abs(dtheta) < tau_straight:
            prev_theta = theta
            continue

        instr.append(f"Avance aproximadamente {acc:.1f} m.")
        acc = 0.0

        if abs(dtheta) >= tau_uturn:
            instr.append("De la vuelta en U.")
        else:
            if dtheta > 0:
                instr.append("Gire a la izquierda." if abs(dtheta) >= tau_turn
                             else "Gire ligeramente a la izquierda.")
            else:
                instr.append("Gire a la derecha." if abs(dtheta) >= tau_turn
                             else "Gire ligeramente a la derecha.")

        prev_theta = theta

    last = math.hypot(points[-1][0] - points[-2][0],
                      points[-1][1] - points[-2][1]) * cell_size_m
    acc += last
    instr.append(f"Avance aproximadamente {acc:.1f} m hasta su destino.")
    return instr