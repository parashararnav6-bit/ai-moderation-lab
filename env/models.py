from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class Observation(BaseModel):
    post: str
    context: str
    user_history: str
    difficulty: str
    item_id: int


class Action(BaseModel):
    decision: str
    reasoning: str
    rewrite: Optional[str] = None


class Reward(BaseModel):
    score: float
    feedback: str
    breakdown: Dict[str, float]


class SessionStats(BaseModel):
    total_cases: int
    completed_cases: int
    average_score: float
    decisions: Dict[str, int]
    recent_scores: List[float]