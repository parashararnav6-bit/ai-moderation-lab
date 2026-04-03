# AI Moderation Lab

AI Moderation Lab is a real-world OpenEnv-style environment for trust and safety research.

It simulates the type of moderation decisions that large platforms make every day:
- allow
- flag
- remove
- escalate

The environment is not a simple classifier. It evaluates:
- decision correctness
- reasoning quality
- policy alignment
- optional safe rewrites
- supervisor review penalties

## Why this project is strong

This project mirrors real production workflows in content moderation and safety systems. It includes:
- context-aware observations
- multi-step reward shaping
- multi-difficulty task sets
- analytics dashboard
- baseline model script
- containerized deployment

## Project structure

- `env/` core environment logic
- `data/` evaluation tasks
- `templates/` dashboard UI
- `static/` frontend logic
- `scripts/` baseline evaluation

## Action space

Each action includes:
- `decision`: allow / flag / remove / escalate
- `reasoning`: explanation for the moderation choice
- `rewrite`: optional safe rewrite

## Observation space

Each observation contains:
- `post`
- `context`
- `user_history`
- `difficulty`
- `item_id`

## Difficulty levels

- Easy: clear cases
- Medium: borderline or implicit harm
- Hard: contextual and safety-critical cases

## Run locally

```bash
pip install -r requirements.txt
python3 -m uvicorn app:app --reload