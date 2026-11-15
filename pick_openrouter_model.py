"""OpenRouter free-model picker: finds free models that support tools, smallest first, and tests each with a real
tool call (1 request per model, so mind the 50/day cap on unpaid accounts).
  python pick_openrouter_model.py            -> probe the 5 smallest free tool models
  python pick_openrouter_model.py 10         -> probe the 10 smallest
  python pick_openrouter_model.py <model-id> -> probe just one (e.g. google/gemma-4-26b-a4b-it:free)
Parameter counts are guessed from the model id/name (e.g. '2.6b'); models with no size in the name sort last.
Working models are printed ready to paste into:  --model openrouter:<id>"""
import json
import os
import re
import sys
import time
import urllib.request

TOOL = [{"type": "function", "function": {
    "name": "read_email", "description": "Read an email by its id.",
    "parameters": {"type": "object", "properties": {"email_id": {"type": "string"}}, "required": ["email_id"]}}}]


def size_b(m):
    """Total parameters in billions guessed from the name; skips active-param tags like 'a4b'. None if unknown."""
    text = f"{m.get('id', '')} {m.get('name', '')}".lower()
    nums = re.findall(r"(?<![a-z0-9])(\d+(?:\.\d+)?)b(?![a-z])", text)
    return float(nums[0]) if nums else None


def free_tool_models():
    with urllib.request.urlopen("https://openrouter.ai/api/v1/models", timeout=30) as r:
        data = json.load(r)["data"]
    ms = [m for m in data if m["id"].endswith(":free") and "tools" in (m.get("supported_parameters") or [])]
    return sorted(ms, key=lambda m: (size_b(m) is None, size_b(m) or 0, m["id"]))


def ping(client, model):
    t0 = time.time()
    try:
        r = client.chat.completions.create(
            model=model, temperature=0, max_tokens=512, tools=TOOL, tool_choice="auto",
            messages=[{"role": "user", "content": "Use the tool to read email e2."}])
        if not getattr(r, "choices", None):
            return f"NO_CHOICES   ({time.time() - t0:.1f}s) {str(r)[:120]}"
        tcs = r.choices[0].message.tool_calls
        if not tcs:
            return f"NO_TOOL_CALL ({time.time() - t0:.1f}s) answered in plain text"
        try:
            args = json.loads(tcs[0].function.arguments or "{}")
        except json.JSONDecodeError:
            return f"BAD_JSON     ({time.time() - t0:.1f}s) {tcs[0].function.arguments[:80]!r}"
        ok = tcs[0].function.name == "read_email" and args.get("email_id") == "e2"
        return f"{'TOOL_OK     ' if ok else 'WRONG_CALL  '} ({time.time() - t0:.1f}s) {tcs[0].function.name}({args})"
    except Exception as e:
        msg = str(e).replace("\n", " ")
        kind = ("GONE/404     " if "404" in msg else "QUOTA/429    " if "429" in msg else "ERROR        ")
        return f"{kind} {type(e).__name__}: {msg[:200]}"


def main():
    from openai import OpenAI
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if len(key) < 10:
        sys.exit("export OPENROUTER_API_KEY=sk-or-... first")
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=key, max_retries=0, timeout=60)
    arg = sys.argv[1] if len(sys.argv) > 1 else "5"
    if not arg.isdigit():
        print(arg, "->", ping(client, arg))
        return
    models = free_tool_models()
    print(f"{len(models)} free models with tool support right now (smallest first):\n")
    for m in models:
        s = size_b(m)
        print(f"  {m['id']:60s} {'~%gB' % s if s else 'size ?':8s} ctx={m.get('context_length')}")
    n = int(arg)
    print(f"\nProbing the {n} smallest (4 s apart):\n")
    good = []
    for m in models[:n]:
        res = ping(client, m["id"])
        print(f"{m['id']:60s} {res}", flush=True)
        if res.startswith("TOOL_OK"):
            good.append(m["id"])
        time.sleep(4)
    print("\nUsable:" if good else "\nNone of those worked; try a larger N or a bigger model.")
    for g in good:
        print(f"  --model openrouter:{g}")


if __name__ == "__main__":
    main()
