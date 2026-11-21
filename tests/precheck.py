#!/usr/bin/env python3
"""Pre-workshop check. Run from the repo root:  python tests/precheck.py   (or python3 / py)
It only reads files and runs the sample checker. It changes nothing and needs no internet."""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, ".agent", "skills", "cloud-cost-safeguards")
ok_all = True


def line(ok, msg, fix=""):
    global ok_all
    ok_all = ok_all and ok
    print("[%s] %s" % ("OK" if ok else "FAIL", msg))
    if not ok and fix:
        print("       -> " + fix)


v = sys.version_info
line(v >= (3, 8), "Python %d.%d.%d (need 3.8 or newer)" % v[:3], "Install a newer Python (see SETUP.md)")
need = [os.path.join(SKILL, "SKILL.md"), os.path.join(SKILL, "policy.json"),
        os.path.join(SKILL, "scripts", "estimate_cost.py"), os.path.join(SKILL, "scripts", "check_policy.py"),
        os.path.join(SKILL, "references", "prices.json")]
need += [os.path.join(ROOT, "fixtures", f) for f in sorted(os.listdir(os.path.join(ROOT, "fixtures")))] if os.path.isdir(os.path.join(ROOT, "fixtures")) else []
missing = [os.path.relpath(p, ROOT) for p in need if not os.path.exists(p)]
line(not missing and len(need) >= 10, "Skill folder and 5 fixtures found" if not missing else "Missing files: %s" % missing,
     "Open the folder that CONTAINS .agent, fixtures and tests, not its parent")
try:
    json.load(open(os.path.join(SKILL, "policy.json")))
    line(True, "policy.json is valid JSON")
except Exception as e:
    line(False, "policy.json is not valid JSON: %s" % e, "Re-extract the zip")
fx = os.path.join(ROOT, "fixtures", "01-safe-small-vm.plan.json")
try:
    p = subprocess.run([sys.executable, os.path.join(SKILL, "scripts", "check_policy.py"), fx],
                       capture_output=True, text=True, timeout=30)
    line(p.returncode == 0 and "RESULT: PASS" in p.stdout, "Sample check ran (RESULT: PASS expected for fixture 01)",
         "Output was: %s %s" % (p.stdout.strip()[-200:], p.stderr.strip()[-200:]))
except Exception as e:
    line(False, "Could not run the checker: %s" % e)
print("\nNext: run  python tests/run_fixtures.py  (expect '1/5 fixtures correct' before Lab 1).")
print("Then ask the agent: what skills do you have?  (expect cloud-cost-safeguards)")
print("\nALL GOOD" if ok_all else "\nSOMETHING NEEDS FIXING (see FAIL lines above)")
sys.exit(0 if ok_all else 1)
