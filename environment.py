from tasks.easy import get_easy_task
from tasks.medium import get_medium_task
from tasks.hard import get_hard_task
from models import Observation, Reward

class ProjectApprovalEnv:
    def __init__(self):
        self.project = {}
        self.correct_decision = None
    
    def reset(self, difficulty="easy"):
        """Initialize environment with a task"""
        if difficulty == "easy":
            task = get_easy_task()
        elif difficulty == "medium":
            task = get_medium_task()
        else:
            task = get_hard_task()

        self.project = {k: v for k, v in task.items() if k != "correct_decision"}
        self.correct_decision = task["correct_decision"]

        return Observation(**self.project)
    
    def step(self, action):
        """Execute action and return result"""
        reward = self.calculate_reward(action)
        done = True
        
        return Observation(**self.project), reward, done, {}
    
    def state(self):
        """Return current state (REQUIRED by OpenEnv spec)"""
        if not self.project:
            return None
        return Observation(**self.project)
    
    def calculate_reward(self, action):
        """Calculate reward based on decision correctness"""
        if action.decision == self.correct_decision:
            return Reward(score=0.9)  # Correct decision = 0.9 (must be < 1.0)
        elif action.decision == "request_changes":
            return Reward(score=0.5)  # Request changes = partial reward
        else:
            return Reward(score=0.1)  # Wrong decision = 0.1 (must be > 0.0) 