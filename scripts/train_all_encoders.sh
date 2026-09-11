#!/usr/bin/env bash
# Train every REMEDI encoder — one per (model, benchmark), ten in all.
#
#     ./scripts/train_all_encoders.sh [facts_per_encoder]
#
# Sequential on purpose. They share one GPU, so running them together only risks an OOM
# (LLaMA training peaks ~20GB of 24) without finishing any sooner. A failure is recorded
# and the remaining encoders still run, because losing nine to one bad benchmark is worse
# than reading a summary at the end.
#
# Everything is teed to $LOG, which lives outside the repo so `git pull` cannot disturb it.
# Copy it off the pod before tearing the pod down.

set -u

N=${1:-5000}
LOG=${LOG:-$HOME/encoders.log}
MODELS=(gpt2-xl llama3-8b)
BENCHES=(counterfact zsre mquake ripple genie)

exec > >(tee -a "$LOG") 2>&1

started=$(date -u +%s)
failed=()

for model in "${MODELS[@]}"; do
  for bench in "${BENCHES[@]}"; do
    echo
    echo "######## $model · $bench · $(date -u +%H:%M:%S) UTC ########"
    if ! time uv run python -m scripts.train_encoder \
        --model "$model" --bench "$bench" --n "$N"; then
      failed+=("$model/$bench")
      echo "!!!! FAILED $model/$bench"
    fi
  done
done

elapsed=$(( $(date -u +%s) - started ))
echo
printf 'total %dh %02dm\n' $((elapsed / 3600)) $(((elapsed % 3600) / 60))

if ((${#failed[@]})); then
  echo "${#failed[@]} FAILED: ${failed[*]}"
  exit 1
fi
echo "all ${#MODELS[@]} x ${#BENCHES[@]} encoders trained -> models/encoders/"
