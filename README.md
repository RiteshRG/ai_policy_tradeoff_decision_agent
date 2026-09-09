# AI Policy Trade-off Decision Agent

A multi-agent AI system built with [deepagents](https://github.com/langchain-ai/deepagents) that investigates a real-world policy trade-off, reasons through it using scoped sub-agents and deterministic tools, and produces a single-slide `.pptx` recommendation.

Built as an academic lab exercise.

## The problem it investigates

India's Ethanol Blended Petrol (EBP) Programme pushed petrol to a 20% ethanol blend (E20) — achieved in 2025, five years ahead of schedule. This reduces crude-oil import dependence, but ethanol comes almost entirely from sugarcane, maize, and rice, competing with food production and stressed groundwater. Vehicle owners also report a mileage penalty.

This is a genuine **food vs. fuel** trade-off — energy security for vehicles vs. food and water security for people vs. cost/compatibility for consumers. The system does not try to "solve" it. It investigates each side independently, surfaces disagreement explicitly, and produces a conditional, sourced recommendation.

## Architecture

Two independently-run stages, each a `create_deep_agent()` orchestrator, sharing one sandboxed filesystem as the handoff between them.

```
                              SCENARIO INPUT
                                    │
        ┌───────────────────────────────────────────────────┐
        │              STAGE 1: investigation_agent          │
        └───────────────────────────────────────────────────┘
                                    │
                    check todos.txt / findings/ (resume?)
                                    │
                              write_todos (plan)
                                    │
              ┌─────────────────────┼─────────────────────┐
              ↓                     ↓                     ↓
     energy_researcher   food_water_researcher   vehicle_consumer_researcher
              ↓                     ↓                     ↓
     findings/energy.md   findings/food_water.md   findings/vehicle_consumer.md
              └─────────────────────┼─────────────────────┘
                                    ↓
                        orchestrator reads & verifies
                                    │
                                    ↓
        ┌───────────────────────────────────────────────────┐
        │       STAGE 2: decision_presentation_agent          │
        └───────────────────────────────────────────────────┘
                                    │
                          decision_subagent
                    (reads all 3 findings files)
                                    │
                          score_policy_options
                         (deterministic Python tool)
                                    │
                        conflict identification
                                    │
                          decision_report.md
                                    │
                        ppt_generation_subagent
                                    │
                          generate_decision_ppt
                        (deterministic Python tool)
                                    │
                      output/final_decision.pptx
```

## Project structure

```
├── investigation.py                        # Stage 1 orchestrator
├── decision_presentation.py                # Stage 2 orchestrator
├── model.py                                # Model client (Groq / Cerebras)
├── subagents/
│   ├── research_subagents.py               # 3 research sub-agents
│   └── decision_presentation_subagents.py  # 2 decision/slide sub-agents
├── tools/
│   ├── research_subagents_tools.py         # search_energy_sources, search_food_water_sources, search_vehicle_sources
│   └── decision_presentation_tools.py      # score_policy_options, generate_decision_ppt
├── sandbox/                                # Virtual filesystem (created at runtime)
│   ├── todos.txt
│   ├── findings/
│   │   ├── energy.md
│   │   ├── food_water.md
│   │   └── vehicle_consumer.md
│   └── decision_report.md
├── output/
│   └── final_decision.pptx                 # Final one-slide deliverable
└── .env                                    # API keys (not committed)
```

## Sub-agents

| Sub-agent | Stage | Lens | Tool | Output |
|---|---|---|---|---|
| `energy_researcher` | 1 | Crude-oil import dependence, energy-security effects | `search_energy_sources` | `findings/energy.md` |
| `food_water_researcher` | 1 | Feedstock crops, farmland shifts, groundwater stress | `search_food_water_sources` | `findings/food_water.md` |
| `vehicle_consumer_researcher` | 1 | Vehicle compatibility, mileage, consumer impact | `search_vehicle_sources` | `findings/vehicle_consumer.md` |
| `decision_subagent` | 2 | Synthesizes all 3 findings, scores options, flags conflicts | `score_policy_options` | `decision_report.md` |
| `ppt_generation_subagent` | 2 | Converts decision report into one slide | `generate_decision_ppt` | `output/final_decision.pptx` |

## Custom tools

- **`search_energy_sources` / `search_food_water_sources` / `search_vehicle_sources`** — keyword-gated search wrappers; reject any query outside their assigned lens before searching, enforcing topic separation structurally rather than only through prompting.
- **`score_policy_options(findings_json, weights_json)`** — deterministic Python scoring function. Takes structured 0–10 criterion values per policy option and a weights dict, returns a weighted numeric score per option. Same inputs always reproduce the same output; the LLM never states or estimates a score itself.
- **`generate_decision_ppt(report_json)`** — deterministic `python-pptx` tool. Builds exactly one slide containing the recommendation, scores, trade-offs, conflicts, caveats, decision conditions, and sources. Saves atomically (temp file + move) to avoid corrupted output on interrupted writes.

## Design principles

- **Explicit tool grounding** — every sub-agent prompt states the exact tool names and parameter signatures (e.g. `file_path`, not `path`) available to it, preventing hallucinated tool calls.
- **Resumability** — every orchestrator checks the filesystem (`ls`, `read_file`) before delegating, skipping sub-agents whose output already exists and is complete. A rate-limited or interrupted run can be re-invoked and will continue from where it left off.
- **Deterministic scoring and slide generation** — both the policy score and the final slide are produced by real Python functions, never by the LLM narrating a number or layout.
- **Conflict is surfaced, never hidden** — when lenses disagree (e.g. energy favors one option, food/water favors another), this is stated explicitly in both the decision report and the final slide.
- **Conditional, not absolute, recommendations** — the final recommendation states the conditions under which it holds, and notes what would change the answer.

## Setup

```bash
pip install deepagents python-pptx langchain-groq python-dotenv
```

Create a `.env` file:

```
GROQ_API_KEY=your_key_here
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_key_here
LANGSMITH_PROJECT=your_project_name
```

## Running the pipeline

```bash
# Stage 1 — research
python investigation.py

# Stage 2 — decision + slide (after Stage 1 completes)
python decision_presentation.py
```

Output: `output/final_decision.pptx`

## Observability

Both stages are traced via [LangSmith](https://smith.langchain.com). Every `write_todos` plan, `task` delegation, tool call, and model turn is captured and viewable per run, including retries after rate-limit interruptions.

## Known constraints

- Runs on Groq's free tier (`openai/gpt-oss-120b`), capped at 8,000 tokens/minute — the pipeline may hit transient rate limits mid-run on longer scenarios. Resumability logic and a rate-limit-aware retry wrapper handle this without losing completed work.
- Word limits are enforced on generated files (350 words per findings file, 750 words for the decision report) to stay within free-tier token budgets while preserving evidence quality.
