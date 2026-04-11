import random
from tasks.easy import get_easy_task
from tasks.medium import get_medium_task
from tasks.hard import get_hard_task
from models import Observation, Reward

class ProjectApprovalEnv:
    def __init__(self):
        self.project = {}
        self.correct_decision = None
        self.step_count = 0
        self.max_steps = 3
        self.changes_requested = 0

    def reset(self, difficulty="easy"):
        if difficulty == "easy":
            task = get_easy_task()
        elif difficulty == "medium":
            task = get_medium_task()
        else:
            task = get_hard_task()
        self.project = {k: v for k, v in task.items() if k not in ("correct_decision", "grader", "name")}
        self.correct_decision = task["correct_decision"]
        self.step_count = 0
        self.changes_requested = 0
        return Observation(**self.project)

    def step(self, action):
        self.step_count += 1
        reward = self.calculate_reward(action)

        # If agent requests changes, improve the project slightly
        if action.decision == "request_changes":
            self.changes_requested += 1
            # Project improves after changes requested
            self.project["completeness"] = min(
                1.0, self.project["completeness"] + random.uniform(0.05, 0.15)
            )
            self.project["status"] = "under_review"
            # Not done yet - agent gets another chance
            done = self.step_count >= self.max_steps
        else:
            # Final decision made
            done = True
            self.project["status"] = action.decision

        return Observation(**self.project), reward, done, {
            "step": self.step_count,
            "changes_requested": self.changes_requested
        }

    def state(self):
        if not self.project:
            return {"status": "no project loaded"}
        return Observation(**self.project).dict()

    def calculate_reward(self, action):
        completeness = self.project.get("completeness", 0.5)
        risk = self.project.get("risk_level", "medium")

        if action.decision == "request_changes":
            # Reward for requesting changes on incomplete projects
            if completeness < 0.7:
                return Reward(score=0.65)
            else:
                return Reward(score=0.35)  # Penalize unnecessary change requests

        elif action.decision == action.decision == self.correct_decision:
            # Correct final decision - higher reward if reached quickly
            base = 0.85
            penalty = self.changes_requested * 0.05
            return Reward(score=max(0.50, base - penalty))

        else:
            # Wrong final decision
            return Reward(score=0.10)