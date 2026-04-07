import json
from env.medalloc_env import MedAllocEnv

class Task:
    def __init__(self, **kwargs):
        # Setup specific task configuration
        self.config = {
            "max_queue_size": 10,
            "num_doctors": 5,
            "num_beds": 5,
            "max_steps": 50,
            "patient_inflow_rate": kwargs.get("patient_inflow_rate", 0.5),
            "emergency_spikes": kwargs.get("emergency_spikes", False)
        }
        
    def make_env(self):
        return MedAllocEnv(self.config)

class task_0(Task):
    """Easy: Low inflow, no spikes"""
    def __init__(self):
        super().__init__(patient_inflow_rate=0.3, emergency_spikes=False)

class task_1(Task):
    """Medium: Moderate inflow"""
    def __init__(self):
        super().__init__(patient_inflow_rate=0.6, emergency_spikes=False)

class task_2(Task):
    """Hard: High inflow + emergency spikes"""
    def __init__(self):
        super().__init__(patient_inflow_rate=0.8, emergency_spikes=True)
