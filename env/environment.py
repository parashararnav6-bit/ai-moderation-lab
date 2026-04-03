from .models import Observation, Action, Reward, SessionStats
from .tasks import load_task
from .graders import grade_action
from .supervisor import supervisor_review


class ModerationEnv:
    def __init__(self, level="easy"):
        self.level = level
        self.task = load_task(level)
        self.reset()

    def set_level(self, level: str):
        self.level = level
        self.task = load_task(level)
        return self.reset()

    def reset(self):
        self.index = 0
        self.history = []
        self.recent_scores = []
        self.decision_counts = {
            "allow": 0,
            "flag": 0,
            "remove": 0,
            "escalate": 0,
        }
        return self._get_obs()

    def _get_obs(self):
        if self.index >= len(self.task):
            return None

        item = self.task[self.index]
        return Observation(
            post=item["post"],
            context=item["context"],
            user_history=item["user_history"],
            difficulty=self.level,
            item_id=self.index,
        )

    def step(self, action: Action):
        if self.index >= len(self.task):
            reward = Reward(
                score=0.0,
                feedback="Episode already finished.",
                breakdown={"final_score": 0.0},
            )
            return None, reward, True, {"state": self.state()}

        expected = self.task[self.index]

        base_score, feedback, breakdown = grade_action(action, expected)
        supervisor_penalty, supervisor_notes = supervisor_review(action, expected)

        final_score = max(0.0, min(base_score + supervisor_penalty, 1.0))
        breakdown["supervisor_penalty"] = round(supervisor_penalty, 3)
        breakdown["final_score"] = round(final_score, 3)

        decision = action.decision.strip().lower()
        if decision in self.decision_counts:
            self.decision_counts[decision] += 1

        self.recent_scores.append(final_score)
        self.history.append(
            {
                "item_id": self.index,
                "post": expected["post"],
                "decision": decision,
                "score": round(final_score, 3),
                "notes": supervisor_notes,
            }
        )

        self.index += 1
        done = self.index >= len(self.task)

        reward = Reward(
            score=final_score,
            feedback=feedback,
            breakdown=breakdown,
        )

        info = {
            "supervisor_notes": supervisor_notes,
            "state": self.state(),
        }

        next_obs = None if done else self._get_obs()
        return next_obs, reward, done, info

    def state(self):
        completed = len(self.recent_scores)
        avg_score = sum(self.recent_scores) / completed if completed else 0.0

        stats = SessionStats(
            total_cases=len(self.task),
            completed_cases=completed,
            average_score=round(avg_score, 3),
            decisions=self.decision_counts,
            recent_scores=[round(x, 3) for x in self.recent_scores[-10:]],
        )

        return {
            "level": self.level,
            "current_index": self.index,
            "history": self.history,
            "stats": stats.model_dump(),
        }