# Remote runbook — hands-on pod operation

Written 27 Aug 2026. Companion to [RUNPOD-CONFIG.md](RUNPOD-CONFIG.md),

**Every command below is marked `[LOCAL]` (your laptop) or `[POD]` (inside SSH).** 

Step	Where	What
1	manual	fire up the pod
2	manual	IP + port into .env
3.1[LOCAL] 	ssh-add ~/.ssh/github_key     
3.2[LOCAL]	ssh-add -l 
4	[LOCAL]	provision — on new pods only
5  [LOCAL] bbk-ssh-sync
6	[POD]	navigate the volume
7	[POD]	sync code
8  [POD] open new tmux  

| Project dir on pod | `/workspace/BBK-final-report-repo` |
| SSH alias | `runpod_bbk` |
| Repo root `.env` | the **only** env file — `gpu.py` names it explicitly |
| tmux session name | `eval` (convention, not enforced) |
| Results | `results/<model>_<method>_<bench>_n<n>/` — **tracked in git** | ** might change 
| Name of Volume | miniature_gray_damselfly

## 3. SSH agent 

```bash
ssh-add ~/.ssh/github_key          # [LOCAL] needed again after every reboot
ssh-add -l                         # [LOCAL] confirm at least one key
```

## 4. Provision
```bash
uv run python remote_deploy/gpu.py
```

## 5. SSH into pod 

```bash
bbk-ssh-sync && ssh runpod_bbk
```

## 6. Move into correct directory on attached volume on pod 

cd /workspace/BBK-final-report-repo

## 7. Git pull and changes made

## 8. Start tmux session


tmux new -s <session-name>

or reattach tmux window
tmux ls                 # list sessions                                            │
tmux attach             # reattach to the most recent                              │
tmux attach -t pod      # reattach to a named one


Without the alias, straight from `.env` (the subshell keeps your tokens out of the session):

```bash
(set -a; . ./.env; set +a; ssh -A -p "$GPU_PUBLIC_PORT" "root@$GPU_IP_ADDRESS")
```