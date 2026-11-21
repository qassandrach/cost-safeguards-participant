#!/usr/bin/env python3
"""Run every fixture through check_policy.py and compare with the expected exit code.
Usage (from repo root): python tests/run_fixtures.py [--policy solution/policy.json]"""
import argparse, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, ".agent", "skills", "cloud-cost-safeguards")
EXPECTED = {"01-safe-small-vm": 0, "02-gpu-instance": 2, "03-nat-gateway-sprawl": 1,
            "04-autoscale-no-max": 2, "05-injection-in-description": 1}
ap = argparse.ArgumentParser()
ap.add_argument("--policy", default=os.path.join(SKILL, "policy.json"))
a = ap.parse_args()
bad = 0
print("%-32s %-9s %-9s %s" % ("fixture", "expected", "got", ""))
for name, want in EXPECTED.items():
    p = subprocess.run([sys.executable, os.path.join(SKILL, "scripts", "check_policy.py"),
                        os.path.join(ROOT, "fixtures", name + ".plan.json"), "--policy", a.policy],
                       capture_output=True, text=True)
    ok = p.returncode == want
    bad += not ok
    print("%-32s %-9s %-9s %s" % (name, want, p.returncode, "OK" if ok else "FAIL"))
print("\n%d/%d fixtures correct" % (len(EXPECTED) - bad, len(EXPECTED)))
sys.exit(1 if bad else 0)
