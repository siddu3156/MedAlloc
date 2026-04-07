# MedAlloc: Hospital Emergency Resource Allocation RL Environment

MedAlloc is a complex, deterministic Reinforcement Learning environment where an agent acts as a hospital emergency resource allocator. It manages doctors and beds, assigning them to incoming patients of varying severities.

## Problem Statement

The environment simulates a hospital ward:
- Patients arrive dynamically with a severity `1-5` and wait in a queue.
- The hospital has limited resources (beds and doctors).
- The agent must allocate resources carefully to optimize treatment while minimizing wait times.

## State Space
The `state()` method returns a dictionary:
- `queue`: Matrix of 10 rows (patients). Each row has `[severity, wait_time, has_doctor, has_bed]`.
- `queue_length`: integer (0-10)
- `available_doctors`: integer
- `available_beds`: integer
- `timestep`: integer

## Action Space
A discrete action space `[0, 30]`:
- `0-9`: Assign a doctor to patient at index `i`.
- `10-19`: Assign a bed to patient at index `i`.
- `20-29`: Delay patient at index `i` (leaves them in queue for later, wait time increases).
- `30`: Wait (do nothing).

## Reward Function
Rewards are calculated deterministically:
- `+1.0`: Correct, complete treatment of high-priority patient.
- `+0.5`: Complete treatment of low-priority patient.
- `-1.0`: Incorrect prioritization (e.g. treating severity 1 while severity 5 waits).
- `-0.5`: Increased waiting time > 5.
- `-0.1`: Invalid assignment actions.

## Determinism
To satisfy OpenEnv guidelines, both patient generation and environment progression are 100% deterministic pseudo-random sequences (without using `random` to avoid seed leakages).

## Quick Start
Run the baseline heuristic agent across all tasks:
```bash
python inference.py --all
```

## Structure
`env/` - The environment logic.
`tasks/` - Three difficulty levels: Easy, Medium, Hard.
`graders/` - Deterministic grader scoring from `[0.0, 1.0]`.
`models/` - Baseline reference location.
