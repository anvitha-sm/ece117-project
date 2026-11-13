"""Gemini key/model tester.
  python ping_gemini.py                 -> list the models your key can use, ping each candidate once, show which work
  python ping_gemini.py <model-name>    -> ping just one model (e.g. gemini-3.8-flash)
Pings use 1 tiny request each. Model names are printed ready to paste into:  --model gemini:<name>"""
import os
import sys
import time

from google import genai
from google.genai import types

key = os.environ.get("GEMINI_API_KEY", "").strip()
print(f"key_length={len(key)}  key_prefix={key[:4]!r}")
client = genai.Client(api_key=key, http_options=types.HttpOptions(timeout=30_000))


def ping(model):
    t0 = time.time()
    try:
        r = client.models.generate_content(model=model, contents="Reply with the single word OK.")
        return f"OK        ({time.time() - t0:.1f}s) -> {(r.text or '').strip()[:20]!r}"
    except Exception as e:
        msg = str(e).replace("\n", " ")
        kind = "QUOTA/429" if "429" in msg or "RESOURCE_EXHAUSTED" in msg else "ERROR    "
        return f"{kind} {type(e).__name__}: {msg[:230]}"


if len(sys.argv) > 1:
    print(sys.argv[1], "->", ping(sys.argv[1]))
    sys.exit()

SKIP = ("image", "tts", "live", "embed", "audio", "imagen", "veo", "robotics", "computer-use", "aqa", "learnlm")
names = []
for m in client.models.list():
    actions = getattr(m, "supported_actions", None) or []
    n = (m.name or "").replace("models/", "")
    if "generateContent" in actions and not any(s in n for s in SKIP):
        names.append(n)
print(f"{len(names)} text models available to your key. Pinging the flash/lite ones (4 s apart):\n")
cands = [n for n in names if "flash" in n or "lite" in n] or names[:8]
for n in cands:
    print(f"{n:45s} {ping(n)}", flush=True)
    time.sleep(4)
print("\nOther available models (not pinged):", ", ".join(n for n in names if n not in cands) or "none")
print("\nA 429 that mentions 'PerMinute' clears in about a minute; one that mentions 'PerDay' resets at midnight Pacific.")