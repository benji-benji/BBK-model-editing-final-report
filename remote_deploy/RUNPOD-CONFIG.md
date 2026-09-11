# RunPod configuration

Standing config for this project. Update when anything changes — this is the reference for
"what do I click" at the start of a session, and the source for the report's deployment
appendix.

---

## The decision that saves the most time: **network volume**

RunPod has three kinds of storage. Getting this right is the difference between a 2-minute
session start and a 40-minute one.

| | Survives pod stop? | Survives pod *termination*? | Use for |
|---|---|---|---|
| **Container disk** | no | no | scratch only |
| **Volume disk** | yes | **no** — dies with the pod | scratch only |
| **Network volume** | yes | **yes** — independent of any pod | everything that matters |

**Put the project on a network volume.** Then a new pod attaches it and the models,
benchmark data, covariance caches and venv are already there.

What that avoids re-doing every session:

| | size | rebuild cost |
|---|---|---|
| GPT-2-XL weights | 6.4 GB | ~5 min download |
| CodeGemma-2B | 5.2 GB | ~5 min |
| LLaMA-3-8B | 16.7 GB | ~15 min + gated HF token |
| benchmark data | ~50 MB | ~1 min |
| **covariance caches** | 0.8 GB (GPT-2) / ~4 GB (LLaMA) | **expensive to recompute** |
| `.venv` (torch CUDA) | ~5 GB | ~3–5 min |

⚠️ **Network volumes are region-locked.** A volume in one region can only attach to pods in
that region. **Pick a region once and always deploy there**, or you will find your GPU of
choice unavailable in the region holding your data. Record it below.

**Size:** ~100 GB covers all three models plus caches and venv. Storage is billed per GB per
month even with no pod running, so don't over-provision. Start at 60–80 GB if only using
GPT-2-XL and CodeGemma; raise before LLaMA.

---

## GPU choice — pick by VRAM tier, not by model name

Availability varies constantly, so don't depend on one specific card. Work out which **tier**
the job needs and take whatever is available and cheapest in that tier.

### What the job actually needs

| workload | VRAM | where it goes |
|---|---|---|
| GPT-2-XL (1.5B) edits + eval | **~10–12 GB** | 6.4 GB fp32 weights + 0.8 GB covariance (5 × 164 MB) + activations |
| CodeGemma-2B | **~12–16 GB** | 5.2 GB weights + similar overhead |
| **LLaMA-3-8B** | **24 GB min · 48 GB comfortable** | 16.7 GB weights + **~4 GB** covariance (d_mlp 14336 → 822 MB *per layer*, all 5 held at once) + activations |

### Tiers — take any card in the tier

| tier | VRAM | covers | examples (check availability/price) |
|---|---|---|---|
| **A — small** | 16 GB | GPT-2-XL, CodeGemma | **RTX 2000 Ada**, RTX 4000 Ada, L4, RTX A4000 |
| **B — mid** | 24 GB | + LLaMA-3 (tight, fp16) | RTX 3090, RTX 4090, L40, A5000 |
| **C — large** | 48 GB | + LLaMA-3 comfortably | **RTX A6000**, **A40**, L40S, RTX 6000 Ada |
| ✗ avoid | 80 GB+ | — | H100 / H200 / B200 — overkill, 5–10× the cost for no benefit |

**RTX 2000 Ada (16 GB) is fine for today.** GPT-2-XL and CodeGemma both fit with room to
spare, and it's cheap. It will **not** do LLaMA-3 — plan to move to tier B/C for M9.


⚠️ **Check GPU availability in your chosen region BEFORE committing the network volume
there.** The volume is region-locked, so if tier B/C cards are chronically unavailable in
that region you will be stuck when LLaMA comes round.

## Pod settings

| setting | value | why |
|---|---|---|
| Type | **On-Demand** | Spot is cheaper but can be interrupted mid-run. Revisit once runs are checkpointed. |
| **SSH terminal access** | **ON** | `gpu.py` provisions over SSH; without this nothing works |
| Start Jupyter notebook | OFF | not used, wastes resources |
| Encrypt volume | optional | no sensitive data here |
| Container disk | 20 GB default is fine | scratch only |
| Volume disk | small | superseded by the network volume |
| Network volume | **attach it** | see above |
| Template | PyTorch CUDA image | avoids installing CUDA/torch from scratch |

**Save a template** once configured — it stores image, disk sizes and ports, so redeploying
is a couple of clicks rather than re-entering everything.

---

## First-time setup (once only)

1. Create the **network volume** in your chosen region (record the region below).
2. Deploy a pod with the volume attached, SSH access on, Jupyter off.
3. Provision: `uv run python "remote deployment/gpu.py"`.
4. On the pod, populate the volume — this is the part you never repeat:
   ```bash
   cd /workspace/bbk-model-editing-final-report
   uv sync                                              # ~5 GB CUDA torch
   uv run python util_download_model.py                 # GPT-2-XL, ~6.4 GB
   uv run python -m benchmarks.download                 # CounterFact + ZsRE
   uv run python util_compute_covariances.py --device cuda -n 20000
   ```
5. **Save a RunPod template** so image/disks/ports are one click next time.

---

## Per-session routine

Setup is *not* repeated. Only steps 1, 2 and 7 are genuinely per-session.

1. **Deploy pod** — pick any GPU in the right tier → attach network volume → select
   template *(~2 min)*
2. **Copy the pod's IP and SSH port into `.env`** (`GPU_IP_ADDRESS`, `GPU_PUBLIC_PORT`)
3. **Provision** from your laptop:
   ```bash
   uv run python "remote deployment/gpu.py"
   ```
4. **SSH in and start tmux** — anything long-running MUST be inside tmux or it dies with the
   connection:
   ```bash
   ssh -p $GPU_PUBLIC_PORT root@$GPU_IP_ADDRESS
   tmux new -s work          # or: tmux attach -t work
   ```
   Detach with `Ctrl-b` then `d`. Reattach with `tmux attach -t work`. List: `tmux ls`.
5. **Sync the repo** (the volume keeps models/data/covariances — only code changes):
   ```bash
   cd /workspace/bbk-model-editing-final-report
   git pull && uv sync
   nvidia-smi                # confirm the GPU is visible and idle
   ```
6. **Verify the device before trusting numbers** — the MPS bug is why this is a standing
   rule, and CUDA deserves the same check once:
   ```bash
   uv run python -m eval.harness --method none -n 3 --device cuda
   ```
   Expect pre == post on every record and `max restore drift 0.00e+00`. Then confirm a real
   MEMIT run matches the CPU baseline (efficacy `p_first` 0.018 → 0.987 on CounterFact n=3).
7. **Terminate the pod when finished.** Billing is per-second while it runs; the network
   volume retains everything. *Stopping* is not terminating — check the bill.

---

## Cost control

The proposal budgeted **£50**. 

### Hard rules

1. **TERMINATE, never just stop.** A stopped pod may still bill for its disk. Check the
   billing page at the end of every session, not from memory.
2. **Develop on CPU locally. Use the GPU only for runs that need it.** Debugging on a live
   pod is paying rental to read tracebacks. The harness runs fine on CPU.
3. **Right-size the network volume.** It bills per GB per month *whether or not a pod is
   running* — at roughly $0.05–0.07/GB/month, 100 GB is ~$5–7/month, ~$14 over the project.
   That is a real slice of an £18 budget. Start at 60 GB; raise only when LLaMA needs it.
4. **Use tier A for everything except LLaMA.** GPT-2-XL and CodeGemma are the bulk of the
   work and don't need an expensive card.
5. **Estimate before launching.** A CounterFact n=100 MEMIT run took ~42s/fact on CPU;
   expect roughly 5–10× faster on GPU, so ~10 min. Cheap. The costly items are LLaMA work
   and high-sample covariance computation — plan those, don't drift into them.


