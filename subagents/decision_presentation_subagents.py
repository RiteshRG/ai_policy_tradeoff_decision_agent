from tools.decision_presentation_tools import score_policy_options, generate_decision_ppt

decision_presentation_subagents = [
    {
    "name": "decision_subagent",
    "description": (
        "Reads the three research findings files, derives structured "
        "criterion scores per policy option, calls the deterministic "
        "scoring tool, identifies conflicts between lenses, and writes "
        "decision_report.md in the required 11-section format."
    ),
    "system_prompt": (
        "You have access to exactly these tools: read_file, write_file, "
        "ls, and score_policy_options. These are the ONLY tools that "
        "exist — do not call any other name (e.g. open_file does not "
        "exist).\n\n"

        "STEP 1 — READ: Use read_file on findings/energy.md, "
        "findings/food_water.md, and findings/vehicle_consumer.md.\n\n"

        "STEP 2 — STRUCTURE: From each file's evidence, assign a 0-10 "
        "value per policy option per lens (your judgment, grounded in "
        "the evidence you just read — do not invent evidence not in "
        "the files).\n\n"

        "STEP 3 — SCORE: Call score_policy_options with these "
        "structured values (as findings_json) and a weights dict (as "
        "weights_json) — default weights: food_water 0.35, energy "
        "0.35, vehicle_consumer 0.30, unless the scenario states "
        "otherwise. The Overall Score column in your report MUST come "
        "verbatim from this tool's output. Never state, estimate, or "
        "adjust an overall score yourself.\n\n"

        "STEP 4 — CONFLICTS: Identify genuine disagreement between "
        "lenses (e.g. energy favors Option A, food/water favors Option "
        "B). State it plainly — never average it away or omit it.\n\n"

        "STEP 5 — WRITE: Call write_file on decision_report.md with "
        "EXACTLY this structure (keep each bullet section to 2-4 short "
        "bullets, not paragraphs, to stay concise):\n\n"

        "# Decision Report\n"
        "## 1. Problem / Scenario\n"
        "## 2. Policy Options (Option A, B, [C if applicable] — name + "
        "1-line description each)\n"
        "## 3. Decision Criteria (table: Criterion | Weight)\n"
        "## 4. Evidence Summary (3 subsections: Food & Water Security, "
        "Energy Security, Vehicle & Consumer Impact — 2-3 bullets each, "
        "drawn from the files you read)\n"
        "## 5. Conflicts / Disagreements (which lenses disagree, why, "
        "how it affects the decision)\n"
        "## 6. Deterministic Scores (table: Policy Option | Food/Water "
        "| Energy | Vehicle/Consumer | Overall Score — Overall Score "
        "column from the tool only. Add one line: 'Scoring was "
        "calculated by the deterministic scoring tool.')\n"
        "## 7. Trade-off Analysis (per option: 1 advantage, 1 "
        "disadvantage)\n"
        "## 8. Recommendation (Recommended Option: [X], reasoning tied "
        "to evidence + score + trade-offs + stakeholder impact)\n"
        "## 9. Confidence & Uncertainty (Confidence: High/Medium/Low; "
        "2-3 key uncertainties; 2-3 caveats)\n"
        "## 10. Decision Conditions (2-3 conditions under which this "
        "recommendation holds; note it may change if conditions "
        "change)\n"
        "## 11. Sources (list from the three findings files' own "
        "Sources sections)\n\n"

        "HARD LIMIT: 450 words total across all 11 sections. Do not "
        "pad — every section should be scannable in seconds, since "
        "this feeds directly into a ONE-SLIDE presentation next."
    ),
    "tools": [score_policy_options],
},

{
    "name": "ppt_generation_subagent",

    "description": (
        "Reads decision_report.md, extracts the final recommendation, "
        "deterministic scores, trade-offs, conflicts, caveats, and "
        "decision conditions, then creates exactly one-slide PPTX "
        "using the PPT generation tool."
    ),

    "system_prompt": (
    "You have access to exactly these tools: read_file, ls, and "
    "generate_decision_ppt. These are the ONLY tools that exist.\n\n"

    "Your ONLY job is to convert decision_report.md into ONE slide. "
    "Do NOT research, recalculate scores, or change the recommendation.\n\n"

    "STEP 1 — Read decision_report.md fully via read_file.\n\n"

    "STEP 2 — Extract from it: title/problem, the recommended option "
    "(Section 8), the Overall Score per option from the Deterministic "
    "Scores table (Section 6), 1-2 key trade-offs (Section 7), 1-2 "
    "conflicts (Section 5), 1-2 caveats (Section 9), decision "
    "conditions (Section 10), and sources (Section 11).\n\n"

    "STEP 3 — Call generate_decision_ppt with EXACTLY ONE argument, "
    "report_json, which must be a single JSON STRING (not an object) "
    "shaped like this example:\n"
    '\'{"title": "...", "recommendation": "...", "scores": '
    '{"Option A": 7.15, "Option B": 7.40}, "trade_offs": ["...", '
    '"..."], "conflicts": ["..."], "caveats": ["..."], '
    '"decision_conditions": ["..."], "sources": ["...", "..."]}\'\n'
    "Copy the scores exactly as written in decision_report.md — do not "
    "recompute them.\n\n"

    "STEP 4 — Report the returned file path and stop."
),

    "tools": [
        generate_decision_ppt
    ],
}
]