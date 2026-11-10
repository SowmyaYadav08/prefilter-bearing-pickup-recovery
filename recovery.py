"""Offline, synthetic Prefilter bearing-pickup recovery logic. No robot control."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Signals:
    tool_ok: bool
    cylinder_in_pick_position: bool
    bearing_held: bool  # Proposed additional presence sensor, NOT an existing confirmed signal
    bearing_at_known_pick_location: bool
    gripper_clear: bool
    cell_clear: bool
    operator_approved: bool
    retry_count: int = 0

MAX_RETRIES = 1

def evaluate(s: Signals) -> tuple[str, str]:
    """Returns decision and reason; never commands motion."""
    if not s.tool_ok or not s.cylinder_in_pick_position:
        return 'BLOCK_AND_INSPECT', 'Tool or cylinder state is not confirmed.'
    if s.bearing_held:
        return 'CONTINUE_TO_PRESS', 'Bearing presence is confirmed at the gripper.'
    if s.retry_count >= MAX_RETRIES:
        return 'BLOCK_AND_INSPECT', 'Retry limit reached.'
    if not all((s.bearing_at_known_pick_location, s.gripper_clear, s.cell_clear, s.operator_approved)):
        return 'BLOCK_AND_INSPECT', 'At least one retry prerequisite is missing.'
    return 'SIMULATED_RETRY_ELIGIBLE', 'All illustrative retry prerequisites are confirmed.'

SCENARIOS = {
    'Successful pickup': Signals(True, True, True, False, True, True, False),
    'Failed pickup — approved retry': Signals(True, True, False, True, True, True, True),
    'Failed pickup — unsafe/unknown': Signals(True, True, False, False, True, False, False),
    'Failed pickup — retry limit reached': Signals(True, True, False, True, True, True, True, 1),
}

if __name__ == '__main__':
    for name, signals in SCENARIOS.items():
        decision, reason = evaluate(signals)
        print(f'{name}: {decision} — {reason}')
