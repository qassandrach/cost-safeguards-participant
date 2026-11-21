# Playbook: what to do on WARN or BLOCK (GCP)

Cheaper alternatives to propose:
- Smaller machine type (e2-small / e2-medium) for demos and dev.
- Spot / preemptible VMs for fault-tolerant work (large discount, can be interrupted).
- Set a hard `max_replicas` / `max_node_count` on every autoscaler (start small, e.g. 3-10).
- Cloud Run with `max-instances` instead of always-on VMs for bursty demos.
- Share ONE Cloud NAT per region/network instead of one per subnet.
- Add `owner` and `ttl` labels, plus a scheduled shutdown for sandbox resources.
- GPUs: ask for an approved project, use the smallest accelerator, or use a hosted model API.

On BLOCK: never loosen the policy yourself. Tell the user who can approve an exception (project owner / FinOps) and offer a cheaper redesign.
