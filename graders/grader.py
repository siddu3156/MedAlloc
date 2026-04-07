import math

def grade(trajectory):
    """
    Given a list of (state, action, reward, next_state) tuples,
    return a score between 0.0 and 1.0
    """
    total_reward = sum(r for _, _, r, _ in trajectory)
    
    # We define theoretical min and max bounds to normalize between 0.0 and 1.0.
    # Max steps = 50. Plausible max reward per step could be ~3.0 if treatment succeeds.
    # Theoretical max: ~150. Min: -100.
    MAX_POSSIBLE = 100.0
    MIN_POSSIBLE = -100.0
    
    score = (total_reward - MIN_POSSIBLE) / (MAX_POSSIBLE - MIN_POSSIBLE)
    
    # Clip between 0 and 1
    score = max(0.0, min(1.0, score))
    
    return score
