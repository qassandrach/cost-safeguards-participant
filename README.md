# Facilitator kit (do NOT put this folder inside the participants' workspace)

Contents: `solution/` (reference SKILL.md and policy.json), `facilitator/` (run of show, hints, red-team handout).
Why separate: the agent can read every file in the workspace, so answers placed next to participants leak.

Quick dry run:
1. Unzip the participant kit in a clean folder, keep this kit elsewhere.
2. `python tests/run_fixtures.py` -> 1/5.
3. Copy solution/policy.json over the skill's policy.json -> 5/5.
4. Copy solution/SKILL.md over the skill's SKILL.md, then run the red-team attacks.
