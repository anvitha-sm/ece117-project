# ece117-project

1. There are three defenses that need to be coded up: provenance, user confirmation, and least-privilege. The stubs for these defenses are in the codebase, but they need to be developed out.

2. There are four LLM models that I'm using for the backbone: Gemini 3.1 Flash-Lite, Gemini 3.5 Flash-Lite, Qwen 3 with 0.6B parameters, and Qwen3 with 1.7B parameters. For Gemini, get an API key and export it in terminal as GEMINI_API_KEY in the environment. For Qwen 3, install ollama and pull the qwen3:0.6b and qwen3:1.7b models.

3. This is what one trial call looks like.

```
python run_grid.py --model ollama:qwen3:1.7b --out qwen3-1.7b-ignore-3/qwen.jsonl --defenses none --attack ignore_previous
```

Model can be one of four things: `gemini:gemini-3.1-flash-lite`, `gemini:gemini-3.5-flash-lite`, `ollama:qwen3:0.6b`, or `ollama:qwen3:1.7b`

Out just needs a unique folder name followed by a .jsonl file.

Defenses is where you pass in what kind of defense you are running: provenance, user confirmation, or least-privilege. Use `none` to run the baseline attack.

Attack is how the prompt is being injected into the source: it can be `important_instructions`, `ignore_previous`, or `plain`.

4. To run all the defenses, you must run each of the following lines of code. Three trials are run for each defense and attack configuration. 

```
python run_grid.py --model ollama:qwen3:0.6b --out qwen3-0.6b-ignore-provenance-1/qwen.jsonl --defenses provenance --attack ignore_previous
python run_grid.py --model ollama:qwen3:0.6b --out qwen3-0.6b-ignore-provenance-2/qwen.jsonl --defenses provenance --attack ignore_previous
python run_grid.py --model ollama:qwen3:0.6b --out qwen3-0.6b-ignore-provenance-3/qwen.jsonl --defenses provenance --attack ignore_previous
python run_grid.py --model ollama:qwen3:0.6b --out qwen3-0.6b-plain-provenance-1/qwen.jsonl --defenses provenance --attack plain
python run_grid.py --model ollama:qwen3:0.6b --out qwen3-0.6b-plain-provenance-2/qwen.jsonl --defenses provenance --attack plain
python run_grid.py --model ollama:qwen3:0.6b --out qwen3-0.6b-plain-provenance-3/qwen.jsonl --defenses provenance --attack plain
python run_grid.py --model ollama:qwen3:0.6b --out qwen3-0.6b-important-provenance-1/qwen.jsonl --defenses provenance --attack important_instructions
python run_grid.py --model ollama:qwen3:0.6b --out qwen3-0.6b-important-provenance-2/qwen.jsonl --defenses provenance --attack important_instructions
python run_grid.py --model ollama:qwen3:0.6b --out qwen3-0.6b-important-provenance-3/qwen.jsonl --defenses provenance --attack important_instructions
```

```
python run_grid.py --model ollama:qwen3:1.7b --out qwen3-1.7b-ignore-provenance-1/qwen.jsonl --defenses provenance --attack ignore_previous
python run_grid.py --model ollama:qwen3:1.7b --out qwen3-1.7b-ignore-provenance-2/qwen.jsonl --defenses provenance --attack ignore_previous
python run_grid.py --model ollama:qwen3:1.7b --out qwen3-1.7b-ignore-provenance-3/qwen.jsonl --defenses provenance --attack ignore_previous
python run_grid.py --model ollama:qwen3:1.7b --out qwen3-1.7b-plain-provenance-1/qwen.jsonl --defenses provenance --attack plain
python run_grid.py --model ollama:qwen3:1.7b --out qwen3-1.7b-plain-provenance-2/qwen.jsonl --defenses provenance --attack plain
python run_grid.py --model ollama:qwen3:1.7b --out qwen3-1.7b-plain-provenance-3/qwen.jsonl --defenses provenance --attack plain
python run_grid.py --model ollama:qwen3:1.7b --out qwen3-1.7b-important-provenance-1/qwen.jsonl --defenses provenance --attack important_instructions
python run_grid.py --model ollama:qwen3:1.7b --out qwen3-1.7b-important-provenance-2/qwen.jsonl --defenses provenance --attack important_instructions
python run_grid.py --model ollama:qwen3:1.7b --out qwen3-1.7b-important-provenance-3/qwen.jsonl --defenses provenance --attack important_instructions
```

```
python run_grid.py --model gemini:gemini-3.1-flash-lite --out 3.1-ignore-provenance-1/qwen.jsonl --defenses provenance --attack ignore_previous
python run_grid.py --model gemini:gemini-3.1-flash-lite --out 3.1-ignore-provenance-2/qwen.jsonl --defenses provenance --attack ignore_previous
python run_grid.py --model gemini:gemini-3.1-flash-lite --out 3.1-ignore-provenance-3/qwen.jsonl --defenses provenance --attack ignore_previous
python run_grid.py --model gemini:gemini-3.1-flash-lite --out 3.1-plain-provenance-1/qwen.jsonl --defenses provenance --attack plain
python run_grid.py --model gemini:gemini-3.1-flash-lite --out 3.1-plain-provenance-2/qwen.jsonl --defenses provenance --attack plain
python run_grid.py --model gemini:gemini-3.1-flash-lite --out 3.1-plain-provenance-3/qwen.jsonl --defenses provenance --attack plain
python run_grid.py --model gemini:gemini-3.1-flash-lite --out 3.1-important-provenance-1/qwen.jsonl --defenses provenance --attack important_instructions
python run_grid.py --model gemini:gemini-3.1-flash-lite --out 3.1-important-provenance-2/qwen.jsonl --defenses provenance --attack important_instructions
python run_grid.py --model gemini:gemini-3.1-flash-lite --out 3.1-important-provenance-3/qwen.jsonl --defenses provenance --attack important_instructions
```

```
python run_grid.py --model gemini:gemini-3.5-flash-lite --out 3.5-ignore-provenance-1/qwen.jsonl --defenses provenance --attack ignore_previous
python run_grid.py --model gemini:gemini-3.5-flash-lite --out 3.5-ignore-provenance-2/qwen.jsonl --defenses provenance --attack ignore_previous
python run_grid.py --model gemini:gemini-3.5-flash-lite --out 3.5-ignore-provenance-3/qwen.jsonl --defenses provenance --attack ignore_previous
python run_grid.py --model gemini:gemini-3.5-flash-lite --out 3.5-plain-provenance-1/qwen.jsonl --defenses provenance --attack plain
python run_grid.py --model gemini:gemini-3.5-flash-lite --out 3.5-plain-provenance-2/qwen.jsonl --defenses provenance --attack plain
python run_grid.py --model gemini:gemini-3.5-flash-lite --out 3.5-plain-provenance-3/qwen.jsonl --defenses provenance --attack plain
python run_grid.py --model gemini:gemini-3.5-flash-lite --out 3.5-important-provenance-1/qwen.jsonl --defenses provenance --attack important_instructions
python run_grid.py --model gemini:gemini-3.5-flash-lite --out 3.5-important-provenance-2/qwen.jsonl --defenses provenance --attack important_instructions
python run_grid.py --model gemini:gemini-3.5-flash-lite --out 3.5-important-provenance-3/qwen.jsonl --defenses provenance --attack important_instructions
```

Then, you can run the line below to generate the summary.md in each folder
```
python report.py {folder_name}\qwen.jsonl
```

