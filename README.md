# Cloud Cost Safeguards as an Agent Skill (participant kit)

90-minute, $0 workshop. No cloud account. Needs only Antigravity + Python 3 (standard library only).
All GCP resources are **simulated** with Terraform plan JSON fixtures. Prices are **illustrative, not real**.

## Setup
Follow **SETUP.md** (Windows and macOS) before the workshop. It takes about 15 minutes and ends with a 2-minute pre-check.

## Layout
- `.agent/skills/cloud-cost-safeguards/` : the skill you will build
- `fixtures/` : 5 simulated GCP plans
- `tests/precheck.py` : run once before the workshop
- `tests/run_fixtures.py` : your scoreboard (goal: 5/5)

## Labs
- **Lab 1:** fill in `policy.json` until the scoreboard shows 5/5.
- **Lab 2:** write `SKILL.md`, then ask the agent to deploy the fixtures and watch what it does.
- **Lab 3:** red team. Work in pairs, open a NEW chat for every attempt, restore changed files afterwards.

Note: verify in Antigravity's docs that workspace skills load from `.agent/skills/` (rename the folder if your version differs).
