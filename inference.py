import importlib
import argparse
import sys
from pprint import pprint

from graders.grader import grade

def heuristic_agent(state):
    """
    Very simple heuristic:
    1. If there's a patient waiting with no doctor, and doctors available, assign doctor.
       Prioritize highest severity.
    2. If there's a patient with doctor but no bed, and beds available, assign bed.
       Prioritize highest severity.
    3. Otherwise do nothing (30).
    """
    queue = state['queue']
    num_waiting = state['queue_length']
    
    # We construct a usable list. queue is [ [sev, wait, has_doc, has_bed], ... ]
    patients = []
    for i in range(num_waiting):
        p = queue[i]
        patients.append({
            'id': i,
            'severity': p[0],
            'wait_time': p[1],
            'has_doctor': p[2],
            'has_bed': p[3]
        })
        
    # Sort by severity descending, then wait_time descending
    patients.sort(key=lambda x: (x['severity'], x['wait_time']), reverse=True)
    
    available_doctors = state['available_doctors']
    available_beds = state['available_beds']
    
    # Try logic 1: needs treatment
    for p in patients:
        if p['severity'] == 0: continue
        if p['has_doctor'] == 0 and available_doctors > 0:
            return p['id']  # Assign doctor -> action id 0 to 9
            
        if p['has_doctor'] == 1 and p['has_bed'] == 0 and available_beds > 0:
            return p['id'] + 10 # Assign bed -> action id 10 to 19

    return 30 # Do nothing / Sleep


def run_episode(task_name):
    # Dynamic import
    tasks_module = importlib.import_module("tasks.tasks")
    task_class = getattr(tasks_module, task_name)
    task = task_class()
    env = task.make_env()
    
    state = env.reset()
    done = False
    
    trajectory = []
    
    print(f"--- Running {task_name} ---")
    
    while not done:
        action = heuristic_agent(state)
        next_state, reward, done, _ = env.step(action)
        trajectory.append((state, action, reward, next_state))
        state = next_state
        
    score = grade(trajectory)
    print(f"Task: {task_name} -> Final Score: {score:.4f}")
    return score

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", type=str, default="task_0", choices=["task_0", "task_1", "task_2"])
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    
    if args.all:
        for t in ["task_0", "task_1", "task_2"]:
            run_episode(t)
    else:
        run_episode(args.task)
