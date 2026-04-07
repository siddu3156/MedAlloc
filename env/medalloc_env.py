import copy
import logging

class MedAllocEnv:
    def __init__(self, config=None):
        """
        config dict with:
        - max_queue_size: int (default 10)
        - num_doctors: int (default 5)
        - num_beds: int (default 10)
        - max_steps: int (default 50)
        - patient_inflow_rate: float (default 0.5)
        - emergency_spikes: bool (default False)
        """
        if config is None:
            config = {}
        self.max_queue_size = config.get("max_queue_size", 10)
        self.total_doctors = config.get("num_doctors", 5)
        self.total_beds = config.get("num_beds", 10)
        self.max_steps = config.get("max_steps", 50)
        self.patient_inflow_rate = config.get("patient_inflow_rate", 0.5)
        self.emergency_spikes = config.get("emergency_spikes", False)
        
        self.reset()
        
    def reset(self):
        self.timestep = 0
        self.available_doctors = self.total_doctors
        self.available_beds = self.total_beds
        self.queue = [] # List of dicts
        self._seed_rng()
        self._spawn_patients()
        return self.state()

    def _seed_rng(self):
        # We need pseudo-random but deterministic generation based on timestep and config.
        # We'll use a simple deterministic sequence instead of random to strictly guarantee determinism
        self.random_counter = 0

    def _pseudo_random(self):
        # Deterministic pseudo-random number generator
        val = (self.random_counter * 1103515245 + 12345) % 2147483648
        self.random_counter += 1
        return val / 2147483648

    def _spawn_patients(self):
        # Spawn logic deterministic
        prob = self._pseudo_random()
        num_to_spawn = 0
        if prob < self.patient_inflow_rate:
            num_to_spawn = 1
        if self._pseudo_random() < (self.patient_inflow_rate / 2):
            num_to_spawn += 1
            
        if self.emergency_spikes and self.timestep % 10 == 0 and self.timestep > 0:
            num_to_spawn += 3
            
        for _ in range(num_to_spawn):
            if len(self.queue) < self.max_queue_size:
                severity = int(self._pseudo_random() * 5) + 1 # 1 to 5
                new_patient = {
                    "id": self.random_counter,
                    "severity": severity,
                    "wait_time": 0,
                    "has_doctor": 0,
                    "has_bed": 0
                }
                self.queue.append(new_patient)

    def state(self):
        padded_queue = []
        for p in self.queue:
            padded_queue.append([p['severity'], p['wait_time'], p['has_doctor'], p['has_bed']])
        
        # Pad with zeros
        while len(padded_queue) < self.max_queue_size:
            padded_queue.append([0, 0, 0, 0])
            
        return {
            "queue": padded_queue,
            "available_doctors": self.available_doctors,
            "available_beds": self.available_beds,
            "timestep": self.timestep,
            "queue_length": len(self.queue)
        }

    def step(self, action):
        """
        Actions:
        0 to 9: Assign doctor to patient i
        10 to 19: Assign bed to patient i
        20 to 29: Delay/reprioritize patient i
        30: Do nothing (wait step)
        """
        reward = 0.0
        done = False
        info = {}
        
        # Parse action
        action_type = -1
        patient_idx = -1
        if action == 30:
            action_type = 3
        elif 0 <= action < 10:
            action_type = 0
            patient_idx = action
        elif 10 <= action < 20:
            action_type = 1
            patient_idx = action - 10
        elif 20 <= action < 30:
            action_type = 2
            patient_idx = action - 20
        else:
            # Invalid action mapping entirely
            reward -= 0.5
            action_type = -1

        # Process valid patient-targeted actions
        if action_type in [0, 1, 2]:
            if patient_idx >= len(self.queue):
                reward -= 0.5 # Penalty for invalid patient index
            else:
                patient = self.queue[patient_idx]
                
                # Check incorrect prioritization
                # If there is a patient with severity 5 waiting no resources, and we target a severity < 5
                max_severity_waiting = max([p['severity'] for p in self.queue if p['has_doctor']==0 or p['has_bed']==0], default=0)
                if patient['severity'] < max_severity_waiting and action_type in [0,1]:
                    reward -= 1.0 # incorrect prioritization
                
                if action_type == 0: # Assign Doctor
                    if patient['has_doctor'] == 1:
                        reward -= 0.1 # already has doctor
                    elif self.available_doctors <= 0:
                        reward -= 0.1 # no doctors
                    else:
                        patient['has_doctor'] = 1
                        self.available_doctors -= 1
                        if patient['severity'] >= 4:
                            reward += 0.5
                        else:
                            reward += 0.25
                            
                elif action_type == 1: # Assign Bed
                    if patient['has_bed'] == 1:
                        reward -= 0.1
                    elif self.available_beds <= 0:
                        reward -= 0.1
                    else:
                        patient['has_bed'] = 1
                        self.available_beds -= 1
                        if patient['severity'] >= 4:
                            reward += 0.5
                        else:
                            reward += 0.25

                elif action_type == 2: # Delay/reprioritize
                    # Delays patient explicitly (increases wait time but maybe frees them from queue if taking too long)
                    patient['wait_time'] += 1
                    reward -= 0.2
                    
                # If patient is fully treated
                if patient['has_doctor'] == 1 and patient['has_bed'] == 1:
                    if patient['severity'] >= 4:
                        reward += 1.0 # +1.0 for correct high-priority full treatment
                    else:
                        reward += 0.5 # +0.5 for efficient allocation of lower severity
                    
                    # Patient leaves
                    self.available_doctors += 1
                    self.available_beds += 1
                    self.queue.pop(patient_idx)

        # Environment dynamics
        for p in self.queue:
            p['wait_time'] += 1
            if p['wait_time'] > 5:
                # Severe penalty if wait time exceeds 5
                reward -= 0.5
                
        self.timestep += 1
        self._spawn_patients()
        
        if self.timestep >= self.max_steps:
            done = True
            
        return self.state(), reward, done, info
