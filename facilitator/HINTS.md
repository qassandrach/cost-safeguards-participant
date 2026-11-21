# Lab 1 hints (reveal gradually)
1. Fixture 02 has a GPU. Which `banned_accelerators` and `banned_machine_families` stop it?
2. Fixture 03 costs about $384. Choose `warn_monthly_usd` below that and `block_monthly_usd` above it. Also try `max_nat_gateways`.
3. Fixture 04 has no scaling cap. Set `max_autoscaler_replicas`.
4. Fixture 05 should WARN on cost, not PASS. Is your warn threshold low enough?
5. Also fill `required_labels` (owner, ttl) and `allowed_regions` (try us-central1, asia-southeast2).
Answer: solution/policy.json
