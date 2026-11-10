# Prefilter bearing-pickup recovery — offline proof of concept

## Purpose

This small Python prototype explores how a robotic assembly process might respond when bearing pickup is successful or cannot be confirmed. It was developed as a follow-up investigation after reviewing the Prefilter module videos from a robotics hackathon.

**This is a synthetic demonstration, not a production control or safety system.** It is not connected to a KUKA robot, PLC, physical sensor, or factory event logs. It never commands robot motion.

## Project files

- `app.py` — Tkinter technician-facing interface with scenario selection, a decision report, illustrative event history and simulated signal details.
- `recovery.py` — synthetic signal definitions, four example scenarios, and rule-based decision logic.
- `test_recovery.py` — six unit tests covering the four example scenarios, an incorrect tool, and missing operator approval.

## How to run

Requires Python 3 with Tkinter available. No third-party Python packages are used.

From this folder:

```bash
python app.py
```

Choose an example from the dropdown. To view simulated inputs, click **Show sensor and PLC details**.

Run the automated checks with:

```bash
python -m unittest -v test_recovery.py
```

## Four illustrative scenarios

| Scenario | Assumed condition | Simulated decision |
| --- | --- | --- |
| Successful pickup | Correct tool/cylinder state and bearing presence confirmed | `CONTINUE_TO_PRESS` |
| Failed pickup — approved retry | Bearing not held, known pickup location, gripper/cell clear, operator approval, retry limit not reached | `SIMULATED_RETRY_ELIGIBLE` |
| Failed pickup — unsafe/unknown | Bearing not held and required recovery conditions cannot be confirmed | `BLOCK_AND_INSPECT` |
| Failed pickup — retry limit reached | Bearing not held and configured example retry limit reached | `BLOCK_AND_INSPECT` |

The demonstration sets `MAX_RETRIES = 1` as an illustrative design choice, **not** a verified setting from the actual equipment. `CONTINUE_TO_PRESS` is a software decision label; it does not initiate pressing. A retry-eligible result does not execute a retry.

## Detection concept and assumptions

The example includes a `bearing_held` Boolean representing a **proposed** bearing-presence check. An inductive proximity sensor is one possible candidate because the bearing is metallic, but it has not been selected, mounted or tested. Nearby metallic gripper components and fixtures may interfere with detection. Optical or camera-based methods, and existing machine sensors, should also be evaluated.

Other simulated conditions — including bearing location, gripper/cell clearance and operator approval — are assumed inputs. The prototype does not establish how these would be measured or verified in the actual cell.

## Current validation and limitations

The included unit tests check six expected decisions of the rule-based function. They do not validate physical sensing accuracy, real PLC/robot behavior, safe robot recovery, industrial fault coverage, or production performance. The event history in the interface is illustrative and is **not** sourced from real PLC events.

Potential next steps, subject to review by the automation team:

1. Review existing PLC, gripper and sensor signals and current recovery behavior.
2. Determine whether an additional bearing-presence check is necessary and feasible.
3. Evaluate false positives/negatives and sensing at relevant robot positions.
4. Define and validate any recovery sequence with appropriate robot/PLC safety interlocks and approved procedures.
5. Expand test coverage using representative machine states and, if available, real logged data.
