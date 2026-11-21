#!/usr/bin/env python3
"""Estimate the monthly cost of a Terraform plan JSON (GCP) from a LOCAL, ILLUSTRATIVE price table.
Usage: estimate_cost.py plan.json [--prices prices.json] [--json]
Unknown prices are reported as unknown (None), never as free."""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PRICES = os.path.join(HERE, "..", "references", "prices.json")


def first(x):
    if isinstance(x, list):
        return x[0] if x else {}
    return x or {}


def last(s):
    return str(s).rsplit("/", 1)[-1]


def region_of(after):
    if after.get("region"):
        return last(after["region"])
    if after.get("zone"):
        return last(after["zone"]).rsplit("-", 1)[0]
    return None


def machine_cost(after, prices):
    mt = last(after.get("machine_type", ""))
    if mt not in prices["machine_types"]:
        return None, "machine type '%s' not in price table" % mt
    cost = prices["machine_types"][mt]
    if first(after.get("scheduling")).get("preemptible"):
        cost *= 1 - prices.get("preemptible_discount", 0)
    for acc in after.get("guest_accelerator") or []:
        if acc.get("type") not in prices["accelerators"]:
            return None, "accelerator '%s' not in price table" % acc.get("type")
        cost += prices["accelerators"][acc["type"]] * int(acc.get("count", 1))
    return cost, mt


def estimate(plan, prices):
    rcs = [rc for rc in plan.get("resource_changes", [])
           if {"create", "update"} & set(rc.get("change", {}).get("actions", []))]
    template_costs = []
    for rc in rcs:
        if rc["type"] == "google_compute_instance_template":
            c, _ = machine_cost(rc["change"].get("after") or {}, prices)
            if c is not None:
                template_costs.append(c)
    items = []
    for rc in rcs:
        t, after = rc["type"], rc["change"].get("after") or {}
        item = {"address": rc["address"], "type": t, "monthly": None, "note": ""}
        if t == "google_compute_instance":
            item["monthly"], item["note"] = machine_cost(after, prices)
        elif t == "google_compute_instance_template":
            c, n = machine_cost(after, prices)
            item["monthly"] = 0.0 if c is not None else None
            item["note"] = "billed through the autoscaler" if c is not None else n
        elif t == "google_compute_autoscaler":
            mx = first(after.get("autoscaling_policy")).get("max_replicas")
            if mx is None:
                item["note"] = "NO max_replicas: cost is unbounded"
            elif not template_costs:
                item["note"] = "no instance template in plan to price replicas"
            else:
                item["monthly"] = float(mx) * max(template_costs)
                item["note"] = "%s replicas x most expensive template (worst case)" % mx
        elif t == "google_compute_router_nat":
            u = prices["usage_assumptions"]
            item["monthly"] = prices["fixed_monthly"][t] + u["nat_gb_per_month"] * u["nat_usd_per_gb"]
            item["note"] = "fixed + assumed %s GB egress" % u["nat_gb_per_month"]
        elif t in prices["fixed_monthly"]:
            item["monthly"] = float(prices["fixed_monthly"][t])
        else:
            item["note"] = "no price entry for resource type"
        items.append(item)
    total = sum(i["monthly"] for i in items if i["monthly"] is not None)
    return {"total": round(total, 2), "items": items,
            "unknown": [i["address"] for i in items if i["monthly"] is None]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--prices", default=DEFAULT_PRICES)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    with open(a.plan) as f:
        plan = json.load(f)
    with open(a.prices) as f:
        prices = json.load(f)
    est = estimate(plan, prices)
    if a.json:
        print(json.dumps(est, indent=2))
        return
    print("Estimated monthly cost (ILLUSTRATIVE prices)\n")
    for i in est["items"]:
        m = "UNKNOWN" if i["monthly"] is None else "$%.2f" % i["monthly"]
        print("  %-48s %10s  %s" % (i["address"], m, i["note"]))
    print("\n  TOTAL (known items): $%.2f" % est["total"])
    if est["unknown"]:
        print("  UNKNOWN cost items: %s" % ", ".join(est["unknown"]))


if __name__ == "__main__":
    main()
