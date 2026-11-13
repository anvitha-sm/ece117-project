"""Show what the model actually did in each attack run.
  python inspect_runs.py results/none.jsonl                 # every attacked run, compact
  python inspect_runs.py results/none.jsonl read/file       # only one attack (mode/target)
  python inspect_runs.py results/none.jsonl --failed        # only runs where the attack did NOT succeed
Per row: SUCCESS/fail, then the tool calls in order. fetch URLs and email recipients are shown in full
so you can see whether the model attempted the attack but the success check missed it."""
import json
import sys

args = [a for a in sys.argv[1:] if not a.startswith("--")]
path, want = args[0], (args[1] if len(args) > 1 else None)
only_failed = "--failed" in sys.argv


def show(t):
    a = t["args"]
    if t["tool"] == "fetch_webpage":
        d = a.get("url", "")
    elif t["tool"] == "send_email":
        d = f"to={a.get('to')} subj={a.get('subject')!r}"
    elif "path" in a:
        d = a["path"]
    else:
        d = ",".join(f"{k}={str(v)[:40]}" for k, v in a.items())
    flag = " [DENIED]" if "UserDenied" in (t["error"] or "") else (" [ERR]" if t["error"] else "")
    return f"{t['tool']}({d[:110]}){flag}"


for line in open(path):
    r = json.loads(line)
    if r["injection_task"] == "baseline":
        continue
    label = f"{r['attack_mode']}/{r['attack_target']}"
    if want and label != want:
        continue
    if only_failed and r["attack_success"]:
        continue
    print(f"{'SUCCESS' if r['attack_success'] else 'fail   '} {r['defense']:15s} {r['user_task']:11s} "
          f"[{r['source']}/{r['req_mode']}] attack={label}")
    for t in r["trace"]:
        print("          ", show(t))
    if r["error"]:
        print("           ERROR:", r["error"].splitlines()[0][:150])
