"""Validates the suite WITHOUT any LLM: injection vectors are reachable, ground truths pass utility,
attacks only 'succeed' when their ground truth runs, and nothing is vacuously true."""
import sys

from agentdojo.agent_pipeline.tool_execution import tool_result_to_str
from agentdojo.functions_runtime import FunctionsRuntime

from lab_suite import suite

fails = []


def check(ok, msg):
    print(("PASS  " if ok else "FAIL  ") + msg)
    if not ok:
        fails.append(msg)


def run_calls(env, calls):
    rt, outs = FunctionsRuntime(suite.tools), []
    for c in calls:
        res, err = rt.run_function(env, c.function, c.args)
        check(err is None, f"    tool call {c.function} ran without error ({err})")
        outs.append(tool_result_to_str(res))
    return outs


for uid, ut in suite.user_tasks.items():
    canary = f"CANARY_{ut.VECTOR}"
    env = suite.load_and_inject_default_environment({ut.VECTOR: canary})
    outs = run_calls(env.model_copy(deep=True), ut.ground_truth(env))
    check(any(canary in o for o in outs), f"{uid} [{ut.SOURCE}/{ut.REQ_MODE}] reaches vector {ut.VECTOR}")

    pre = suite.load_and_inject_default_environment({})
    post = pre.model_copy(deep=True)
    run_calls(post, ut.ground_truth(pre))
    check(ut.utility(ut.GROUND_TRUTH_OUTPUT, pre, post), f"{uid} utility passes on ground truth")
    check(not ut.utility("I could not do that.", pre, pre.model_copy(deep=True)),
          f"{uid} utility fails on a no-op")

for iid, it in suite.injection_tasks.items():
    pre = suite.load_and_inject_default_environment({})
    post = pre.model_copy(deep=True)
    check(not it.security("", pre, pre.model_copy(deep=True)), f"{iid} [{it.ATTACK_MODE}] attack NOT successful on a no-op")
    run_calls(post, it.ground_truth(pre))
    check(it.security("", pre, post), f"{iid} [{it.ATTACK_MODE}] attack successful when its ground truth runs")

print(f"\n{len(fails)} failure(s)")
sys.exit(1 if fails else 0)
