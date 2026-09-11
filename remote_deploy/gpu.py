"""Provision a RunPod GPU instance for this project.

Adapted from a reference script. Written by Claude Code.

The pod is provisioned over SSH: clone, install, fetch data, verify. Docker is
deferred — it costs a multi-GB image build before anything can be tested, and the report's
reproducibility claim is served by the pinned uv.lock plus the checksummed data MANIFEST.

This script PROVISIONS ONLY. It never runs the harness and never touches
harness_config.json. Runs are started by hand on the pod — see remote_deploy/RUNBOOK.md.

Usage:
    1. Start a pod in the RunPod console, note its SSH IP and port
    2. Put them in .env  (see .env.example)
    3. uv run python remote_deploy/gpu.py                  # full provision
       uv run python remote_deploy/gpu.py --check-driver   # host CUDA driver only (fast)
       uv run python remote_deploy/gpu.py --verify         # just re-check CUDA
       uv run python remote_deploy/gpu.py --fetch          # just verify assets are present

Requires in .env:
    GPU_IP_ADDRESS, GPU_PUBLIC_PORT, GPU_GIT_NAME, GPU_GIT_EMAIL
    WANDB_API_KEY   (optional, for --wandb runs)
    HF_TOKEN        (needed later for gated LLaMA-3)
"""

from __future__ import annotations

import argparse
import os
import shlex
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

# The repo-root .env is the ONLY env file, and it is named explicitly rather than found by
# search. Bare load_dotenv() walks up from this file's own directory, so a stray
# remote_deploy/.env silently won this lookup while copy_env() below still scp'd the
# root one — GPU_IP_ADDRESS came from a different file than the tokens sent to the pod.
ENV_FILE = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(ENV_FILE, override=True)

REPO = "git@github.com:benji-benji/BBK-final-report-repo.git"
PROJECT_DIR = "/workspace/BBK-final-report-repo"
SSH_HOST = "runpod_bbk"


def required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise ValueError(f"{name} must be set in .env before running gpu.py.")
    return value


def check_agent() -> bool:
    """The SSH agent must hold a key before anything else works.

    gpu.py authenticates by agent (not -i) because the pod ALSO needs the forwarded key to
    clone the private GitHub repo. An empty agent produces a bare `root@...'s password:`
    prompt, which is an unhelpful way to learn this — hence checking up front.

    The agent empties on every reboot, so this will recur.
    """
    r = subprocess.run(["ssh-add", "-L"], capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip():
        print(
            "\nERROR: no SSH keys in the agent.\n"
            "  The pod cannot authenticate you, and cannot clone the private repo.\n\n"
            "  Fix:  ssh-add ~/.ssh/github_key\n"
            "  (needed again after each reboot; add --apple-use-keychain to persist)\n",
            file=sys.stderr,
        )
        return False
    n = len(r.stdout.strip().splitlines())
    print(f"ssh agent: {n} key(s) loaded")
    return True


def ssh_base(public_port: str, ip: str) -> list[str]:
    return [
        "ssh", "-A",
        "-o", "ForwardAgent=yes",
        "-o", "StrictHostKeyChecking=no",
        "-o", "UserKnownHostsFile=/dev/null",
        "-o", "BatchMode=yes",          # fail loudly instead of prompting for a password
        "-o", "ConnectTimeout=20",
        "-p", str(public_port),
        f"root@{ip}",
        "bash", "-s",
    ]


def run_remote(public_port: str, ip: str, commands: str, label: str) -> bool:
    """Run a bash script on the pod, streaming output.

    Streamed rather than captured: these steps take minutes (pip resolution, model
    download, covariance compute) and silence makes a hang indistinguishable from work.
    """
    print(f"\n=== {label} ===", flush=True)
    try:
        proc = subprocess.run(ssh_base(public_port, ip), input=commands, text=True)
        ok = proc.returncode == 0
        print(f"{'OK' if ok else 'FAILED'}: {label}", flush=True)
        return ok
    except Exception as e:  # noqa: BLE001
        print(f"FAILED: {label}\n{e}", file=sys.stderr)
        return False


def check_driver(public_port: str, ip: str, required_major: int = 13) -> bool:
    """Check the host's CUDA driver BEFORE the 25-minute uv sync.

    Learned the hard way: a pod with a CUDA 12.4 driver installed torch 2.11.0+cu130
    (PyPI's linux wheel for 2.11 is cu13-only), and the mismatch only surfaced after the
    full install. The driver belongs to the physical host, so it cannot be upgraded from
    inside the container — the fix is to redeploy on a host with a newer driver, filtered
    in the RunPod deploy page.
    """
    print("\n=== check CUDA driver (before the slow install) ===", flush=True)
    r = subprocess.run(
        ssh_base(public_port, ip),
        input="nvidia-smi --query-gpu=driver_version --format=csv,noheader\n"
              "nvidia-smi | grep -oE 'CUDA Version: [0-9.]+'\n",
        text=True, capture_output=True,
    )
    out = r.stdout.strip()
    err = r.stderr.strip()
    print(out or err[:300], flush=True)

    if r.returncode != 0 or not out:
        print(
            "\nERROR: could not reach the pod.\n"
            "  - is it running? (a stopped or terminated pod refuses connections)\n"
            "  - do GPU_IP_ADDRESS / GPU_PUBLIC_PORT in .env match the CURRENT pod?\n"
            "    they change on every deploy.\n",
            file=sys.stderr,
        )
        return False

    import re
    m = re.search(r"CUDA Version: (\d+)\.(\d+)", out)
    if not m:
        print("WARNING: reachable, but could not parse the CUDA version — continuing",
              flush=True)
        return True
    major, minor = int(m.group(1)), int(m.group(2))
    if major < required_major:
        print(
            f"\nERROR: host driver supports CUDA {major}.{minor}, but this project's "
            f"torch build needs CUDA {required_major}.x.\n"
            f"  PyPI's torch 2.11.0 for linux is +cu130 and will report "
            f"'cuda available: False' on this host.\n\n"
            f"  Fix: terminate this pod and redeploy, filtering for CUDA {required_major}.x\n"
            f"       on the RunPod deploy page. The driver is host-level and cannot be\n"
            f"       changed from inside the container.\n\n"
            f"  Alternative (only if {required_major}.x hosts are unavailable): pin torch to\n"
            f"       2.9.1 with the matching cu12x index — but that diverges from the local\n"
            f"       stack, so local and remote results stop being byte-comparable.\n",
            file=sys.stderr,
        )
        return False
    print(f"OK: driver supports CUDA {major}.{minor}", flush=True)
    return True


def provision(public_port: str, ip: str, git_name: str, git_email: str) -> bool:
    """Clone the repo and install system tools + python deps."""
    return run_remote(public_port, ip, f"""
set -euo pipefail
export GIT_SSH_COMMAND="ssh -o StrictHostKeyChecking=no"
ssh-add -L || echo "WARNING: no forwarded SSH keys - the clone will fail for a private repo"

# Everything uv needs must live on the network volume, or a new pod rebuilds the
# environment from scratch every session:
#
#   UV_CACHE_DIR         package cache. On container disk it is a different filesystem
#                        from .venv, so uv cannot hardlink and physically copies ~5GB —
#                        that is what made the first install take 25 minutes.
#   UV_PYTHON_INSTALL_DIR uv's managed interpreters. Default is under $HOME on container
#                        disk, so .venv/bin/python3 becomes a dangling symlink the moment
#                        the pod is replaced ("Ignoring existing virtual environment
#                        linked to non-existent Python interpreter") and the whole venv is
#                        rebuilt. Putting it on the volume makes .venv genuinely reusable.
export UV_CACHE_DIR=/workspace/.uv-cache
export UV_PYTHON_INSTALL_DIR=/workspace/.uv-python
export HF_HOME=/workspace/.hf-cache
mkdir -p "$UV_CACHE_DIR" "$UV_PYTHON_INSTALL_DIR" "$HF_HOME"
for v in 'export UV_CACHE_DIR=/workspace/.uv-cache' \
         'export UV_PYTHON_INSTALL_DIR=/workspace/.uv-python
export HF_HOME=/workspace/.hf-cache'; do
  grep -qF "$v" ~/.bashrc || echo "$v" >> ~/.bashrc
done

git config --global user.name {shlex.quote(git_name)}
git config --global user.email {shlex.quote(git_email)}

apt-get update -qq
# tmux is not optional: an n=100 harness run outlives any ssh session
apt-get install -y -qq tmux nvtop htop pigz git curl

curl -Ls https://astral.sh/uv/install.sh | bash
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

mkdir -p /workspace && cd /workspace
if [ -d {shlex.quote(PROJECT_DIR)}/.git ]; then
  cd {shlex.quote(PROJECT_DIR)}
  # fetch + hard reset, NOT pull. The pod is a disposable execution environment, not
  # somewhere to develop, so its checkout should always match origin exactly.
  #
  # `git pull` fails with "divergent branches" whenever the pod holds a commit that was
  # never pushed — which happens easily: a commit succeeds on the pod but the push fails
  # because SSH agent forwarding died with its session. The repo lives on the network
  # volume, so that stale commit survives pod replacement and blocks every later provision.
  #
  # TRADE-OFF: this DISCARDS anything committed or modified on the pod but not pushed.
  # Pull results down (scp) before re-provisioning. Results also persist on the network
  # volume under artifacts/, so a reset does not destroy them on disk — only the git commit.
  git fetch origin
  echo "--- discarding any pod-local changes, resetting to origin/main ---"
  git log --oneline origin/main..HEAD 2>/dev/null | sed 's/^/    dropping: /' || true
  git reset --hard origin/main
  git log --oneline -1
else
  git clone {shlex.quote(REPO)}
  cd {shlex.quote(PROJECT_DIR)}
fi

uv sync
""", "provision: clone, tmux/nvtop, uv sync")


def copy_env(public_port: str, ip: str, env_file: Path) -> bool:
    """Copy .env (WANDB_API_KEY, HF_TOKEN) to the pod. Never committed."""
    print("\n=== copying .env ===", flush=True)
    proc = subprocess.run(
        ["scp", "-P", str(public_port), "-o", "StrictHostKeyChecking=no",
         str(env_file), f"root@{ip}:{PROJECT_DIR}/.env"],
        text=True,
    )
    ok = proc.returncode == 0
    print(f"{'OK' if ok else 'FAILED'}: .env copy", flush=True)
    return ok


def verify_cuda(public_port: str, ip: str) -> bool:
    """Confirm torch sees the GPU before spending time on anything else.

    Worth its own step: an MPS autograd bug silently broke the z-optimisation for a whole
    session locally (DEV-001), so 'the device behaves as expected' is now checked, not
    assumed.
    """
    return run_remote(public_port, ip, f"""
set -euo pipefail
export PATH="$HOME/.local/bin:$PATH"
export UV_CACHE_DIR=/workspace/.uv-cache
export UV_PYTHON_INSTALL_DIR=/workspace/.uv-python
export HF_HOME=/workspace/.hf-cache
cd {shlex.quote(PROJECT_DIR)}
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
uv run python -c "
import torch
print('torch', torch.__version__)
print('cuda available:', torch.cuda.is_available())
assert torch.cuda.is_available(), 'no CUDA device visible to torch'
print('device:', torch.cuda.get_device_name(0))
print('capability:', torch.cuda.get_device_capability(0))
"
""", "verify CUDA")


# --fetch used to run against whatever commit the pod happened to hold, so a local fix
# looked like it had not worked — twice in twenty minutes. The pod is a disposable
# execution environment, never a place to develop, so every remote step syncs first and
# prints the commit it is actually running.
#
# NOTE: this hard-resets to origin/main, so it DISCARDS an uncommitted harness_config.json
# edited by hand on the pod. Edit the config after provisioning, not before.
SYNC_TO_ORIGIN = """echo "--- syncing pod to origin/main ---"
git fetch origin --quiet
git reset --hard origin/main --quiet
git log --oneline -1 | sed 's/^/    pod at: /'"""


def fetch_assets(public_port: str, ip: str, cov_samples: int, model: str,
                 force_cov: bool = False) -> bool:
    """Verify the gitignored assets are present. Does NOT fetch, despite the flag name.

    Everything it checks for already lives on the network volume, so this checks and fails
    loudly with instructions rather than pretending to fetch. The two scripts that would
    build them do now exist and work — scripts/download_benchmarks.py and
    scripts/compute_covariances.py — so this could call them; it deliberately does not,
    because compute_covariances is expensive and should be an explicit decision.
    """
    return run_remote(public_port, ip, f"""
set -euo pipefail
export PATH="$HOME/.local/bin:$PATH"
export UV_CACHE_DIR=/workspace/.uv-cache
export UV_PYTHON_INSTALL_DIR=/workspace/.uv-python
export HF_HOME=/workspace/.hf-cache
cd {shlex.quote(PROJECT_DIR)}
{SYNC_TO_ORIGIN}

fail=0
check() {{ if [ -e "$1" ]; then echo "  ok      $1"; else echo "  MISSING $1"; fail=1; fi }}

echo "--- weights ---"
check models/{model}/model.safetensors
echo "--- covariance cache ---"
check artifacts/covariances/{model}
echo "--- benchmark data ---"
check data/raw/counterfact/counterfact.json
check data/raw/zsre/zsre.json
check data/raw/ripple/popular.json
check data/raw/ripple/ripple_qid_labels.json
check data/raw/mquake/mquake.json
echo "--- genie (regenerate offline from the tracked table) ---"
if [ ! -e data/raw/genie/genie.json ]; then
  uv run python -m genie_bench.scripts.genie_full_generation
fi
check data/raw/genie/genie.json

if [ "$fail" = "1" ]; then
  echo ""
  echo "Missing assets are on the network volume at /workspace/bbk-model-editing-final-report."
  echo "Relocate them once, by hand:"
  echo "  mv ../bbk-model-editing-final-report/models/* models/"
  echo "  mv ../bbk-model-editing-final-report/artifacts/covariance artifacts/covariances"
  exit 1
fi
""", f"verify assets for {model}")




def print_ssh_config(ssh_host: str, public_port: str, ip: str) -> None:
    print(f"""
--------------------------------------
Add to ~/.ssh/config:

Host {ssh_host}
  HostName {ip}
  User root
  Port {public_port}
  ForwardAgent yes

Then: ssh {ssh_host}

The pod is now provisioned and NOTHING has been run on the GPU. Start runs by hand.

Long runs — always inside tmux, an n=100 run outlives any ssh session:
  ssh {ssh_host}
  tmux new -s eval
  cd {PROJECT_DIR}
  # harness.py takes no arguments: it reads harness_config.json from the repo root
  nano harness_config.json          # pick models x methods x benchmarks x quantity
  uv run python -u harness.py
  # detach: Ctrl-b d      reattach: tmux attach -t eval

Smoke test by hand — one method per invocation. The harness has no try/except around
run_edits, so six methods in one config means the first one that raises takes down every
cell after it:
  1. memit x counterfact x n=3   expect efficacy 0.000 -> 1.000, p_first 0.018 -> 0.987
  2. one method at a time, same bench
  3. check "max restore drift: 0.00e+00" on EVERY cell — anything else means teardown
     failed and every case after it in that run is contaminated
Genie is the only benchmark with generation-scored probes, so it is the only cell that
exercises REMEDI's forward pre-hook during generate().

Results land in results/<model>_<method>_<bench>_n<n>/ on the pod. results/ IS tracked,
but the pod is EPHEMERAL and `provision` hard-resets to origin/main — so push before
terminating, or scp them down:
  cd {PROJECT_DIR} && git add results/ && git commit -m "results: ..." && git push
--------------------------------------""")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verify", action="store_true", help="only re-check CUDA")
    ap.add_argument("--check-driver", action="store_true",
                    help="only check the host CUDA driver (fast, do this first)")
    ap.add_argument("--cuda-major", type=int, default=13,
                    help="CUDA major version the torch build needs (default 13)")
    ap.add_argument("--fetch", action="store_true", help="only re-fetch weights/data/covariance")
    ap.add_argument("--cov-samples", type=int, default=20000,
                    help="covariance samples (local default was 1000; reference uses 100000)")
    ap.add_argument("--model", default="gpt2-xl")
    ap.add_argument("--force-cov", action="store_true",
                    help="rebuild the covariance cache even if present "
                         "(use when raising --cov-samples)")
    args = ap.parse_args()

    ip = required_env("GPU_IP_ADDRESS")
    port = required_env("GPU_PUBLIC_PORT")

    if not check_agent():
        return 2

    if args.check_driver:
        return 0 if check_driver(port, ip, args.cuda_major) else 1
    if args.verify:
        return 0 if verify_cuda(port, ip) else 1
    if args.fetch:
        return 0 if fetch_assets(port, ip, args.cov_samples, args.model,
                                 force_cov=args.force_cov) else 1
    # The chain ends at "fetch assets". It deliberately does NOT run anything on the GPU.
    #
    # It used to end in a six-method smoke sweep, which wrote harness_config.json once per
    # cell — so provisioning a pod silently overwrote whatever run configuration was in the
    # repo, and there was no way to provision without also spending GPU time. Runs are now
    # started by hand: edit harness_config.json, `uv run python -u harness.py`.
    steps = [
        ("check driver", lambda: check_driver(port, ip, args.cuda_major)),
        ("provision", lambda: provision(port, ip, required_env("GPU_GIT_NAME"),
                                        required_env("GPU_GIT_EMAIL"))),
        ("copy .env", lambda: copy_env(port, ip, ENV_FILE)),
        ("verify CUDA", lambda: verify_cuda(port, ip)),
        ("fetch assets", lambda: fetch_assets(port, ip, args.cov_samples, args.model,
                                              force_cov=args.force_cov)),
    ]
    for name, fn in steps:
        if not fn():
            print(f"\nStopped at: {name}. Fix, then re-run "
                  f"(--verify / --fetch to resume a single step).", file=sys.stderr)
            return 1

    print_ssh_config(SSH_HOST, port, ip)
    return 0


if __name__ == "__main__":
    sys.exit(main())
