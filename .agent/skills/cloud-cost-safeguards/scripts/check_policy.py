#!/usr/bin/env python3
"""Check a Terraform plan JSON against policy.json.
Exit codes: 0 = PASS, 1 = WARN (human must confirm), 2 = BLOCK (do not proceed).
A policy value of null means 'rule not enforced yet' (Lab 1: fill these in).
Usage: check_policy.py plan.json [--policy policy.json] [--prices prices.json]"""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from estimate_cost import estimate, first, last, region_of, DEFAULT_PRICES  # noqa: E402

DEFAULT_POLICY = os.path.join(HERE, "..", "policy.json")
COMPUTE = ("google_compute_instance", "google_compute_instance_template")


def check(plan, policy, prices):
    est = estimate(plan, prices)
    F = []  # (severity, message)
    total = est["total"]
    blk, wrn = policy.get("block_monthly_usd"), policy.get("warn_monthly_usd")
    if blk is not None and total >= blk:
        F.append((2, "Total $%.2f/month is at or above the BLOCK limit $%s" % (total, blk)))
    elif wrn is not None and total >= wrn:
        F.append((1, "Total $%.2f/month is at or above the WARN limit $%s" % (total, wrn)))
    for i in est["items"]:
        if i["monthly"] is None:  # fail closed: unknown is never free
            F.append((1, "%s: cost UNKNOWN (%s)" % (i["address"], i["note"])))
    nats = 0
    for rc in plan.get("resource_changes", []):
        if not {"create", "update"} & set(rc["change"].get("actions", [])):
            continue
        t, a, addr = rc["type"], rc["change"].get("after") or {}, rc["address"]
        if t == "google_compute_router_nat":
            nats += 1
        reg, allowed = region_of(a), policy.get("allowed_regions")
        if allowed is not None and reg and reg not in allowed:
            F.append((2, "%s: region %s not in allowed regions" % (addr, reg)))
        if t in COMPUTE:
            fam = last(a.get("machine_type", "")).split("-")[0]
            if fam in (policy.get("banned_machine_families") or []):
                F.append((2, "%s: machine family '%s' is banned" % (addr, fam)))
            for acc in a.get("guest_accelerator") or []:
                if acc.get("type") in (policy.get("banned_accelerators") or []):
                    F.append((2, "%s: accelerator '%s' is banned" % (addr, acc["type"])))
            need = policy.get("required_labels")
            if need:
                miss = [k for k in need if k not in (a.get("labels") or {})]
                if miss:
                    F.append((1, "%s: missing required labels %s" % (addr, miss)))
        if t == "google_compute_autoscaler":
            cap = policy.get("max_autoscaler_replicas")
            mx = first(a.get("autoscaling_policy")).get("max_replicas")
            if cap is not None and mx is None:
                F.append((2, "%s: autoscaler has no max_replicas" % addr))
            elif cap is not None and mx > cap:
                F.append((2, "%s: max_replicas %s exceeds cap %s" % (addr, mx, cap)))
    mn = policy.get("max_nat_gateways")
    if mn is not None and nats > mn:
        F.append((1, "%d Cloud NAT gateways exceed the limit of %d" % (nats, mn)))
    return est, F


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--policy", default=DEFAULT_POLICY)
    ap.add_argument("--prices", default=DEFAULT_PRICES)
    a = ap.parse_args()
    plan, policy, prices = (json.load(open(p)) for p in (a.plan, a.policy, a.prices))
    est, F = check(plan, policy, prices)
    code = max([s for s, _ in F], default=0)
    print("Plan: %s | Estimated: $%.2f/month (illustrative)" % (os.path.basename(a.plan), est["total"]))
    for sev, msg in sorted(F, reverse=True):
        print("  [%s] %s" % ("BLOCK" if sev == 2 else "WARN", msg))
    unset = [k for k, v in policy.items() if v is None]
    if unset:
        print("  [note] policy rules not set yet (null): %s" % ", ".join(unset))
    print("RESULT: %s (exit %d)" % (["PASS", "WARN", "BLOCK"][code], code))
    sys.exit(code)


if __name__ == "__main__":
    main()
