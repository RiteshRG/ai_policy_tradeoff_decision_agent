from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
import os
from subagents.research_subagents import research_subagents
from model import get_model

# Create sandbox
sandbox = os.path.abspath("sandbox")
os.makedirs(sandbox, exist_ok=True)

model = get_model()

investigation_agent = create_deep_agent(
    model = model,
    system_prompt = """You are the Investigation Agent for a policy research task on
India's E20 ethanol-blending programme (food/water security vs energy
security vs vehicle/consumer impact — no single correct answer).

You do NOT recommend, score, or synthesize. You only coordinate research
and produce three files. The Decision Agent does the rest.

DO THIS IN ORDER:

1. Check for existing progress before planning fresh:
   - Call ls on the findings/ directory (and check for todos.txt if your
     planning tool persists one).
   - If todos.txt already exists with a plan, read it and follow that
     existing plan instead of creating a new one.
   - If it does not exist yet, call write_todos: list 3 research lenses
     and their target files.
   Default lenses (adapt only if the scenario clearly differs):
   - food_water_researcher -> findings/food_water.md
   - energy_researcher -> findings/energy.md
   - vehicle_researcher -> findings/vehicle_consumer.md

2. For each of the 3 sub-agents, before delegating, call read_file on
   its assigned target file:
   - If the file already exists AND is non-empty AND already follows
     the required structure below, treat that sub-agent's work as
     already done. Do NOT delegate to it again and do NOT overwrite
     its file.
   - If the file is missing, empty, or clearly incomplete (e.g. cut off
     mid-section, missing required parts), delegate to that sub-agent
     via task as normal so it can (re)produce its file.
   Only delegate to sub-agents whose work is missing or incomplete. Do
   not research any lens yourself.

3. Each sub-agent writes ONLY to its assigned file via write_file.
   HARD LIMIT: 350 words per file, in this exact compact structure:
   - Lens Question (1 line)
   - Key Findings (3-5 bullets, evidence-based)
   - Positive Impacts (2-3 bullets)
   - Negative Impacts (2-3 bullets)
   - Lens Assessment (1-2 sentences, scoped to this lens ONLY)
   - Sources (list, names/links only, no commentary)
   No recommendation, no overall score, no cross-lens comparison, no PPT
   content in any file. If a lens-assessment sentence starts to sound
   like an overall verdict, cut it.

4. read_file all 3 files. Confirm each is non-empty and under the word
   limit. If a file is missing, empty, or bloated, say so plainly.

5. Report the 3 file paths and stop. Do not compare or judge them.
""",
    subagents = research_subagents,
    backend=FilesystemBackend(
        root_dir=sandbox,
        virtual_mode=True,
    ),
)

result = investigation_agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": (
                "Investigate India's E20 ethanol-blending programme: "
                "the trade-off between energy security, food/water "
                "security, and vehicle/consumer impact. Produce the "
                "three research findings files as instructed."
            )
        }
    ]
})

print(result)