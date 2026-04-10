from pydantic import BaseModel
from typing import Optional

class Observation(BaseModel):
    project_id: int
    title: str
    budget: int
    risk_level: str
    status: str
    completeness: float

class Action(BaseModel):
    decision: str  # approve | reject | request_changes
    comments: Optional[str] = None

class Reward(BaseModel):
    score: float