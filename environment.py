from tasks.easy import get_easy_task
from tasks.medium import get_medium_task
from tasks.hard import get_hard_task
from models import Observation, Reward

class ProjectApprovalEnv:
    def __init__(self):
        self.project = {}
        self.correct_decision = None

    def reset(self, difficulty="easy"):
        if difficulty == "easy":
            task = get_easy_task()
        elif difficulty == "medium":
            task = get_medium_task()
        else:
            task = get_hard_task()
        self.project = {k: v for k, v in task.items() if k not in ("correct_decision", "grader", "name")}
        self.correct_decision = task["correct_decision"]
        return Observation(**self.project)

    def step(self, action):
        reward = self.calculate_reward(action)
        done = True
        return Observation(**self.project), reward, done, {}

    def state(self):
        if not self.project:
            return {"status": "no project loaded"}
        return Observation(**self.project).dict()

    def calculate_reward(self, action):
        if action.decision == self.correct_decision:
            return Reward(score=0.9)
        elif action.decision == "request_changes":
            return Reward(score=0.5)
        else:
            return Reward(score=0.1)