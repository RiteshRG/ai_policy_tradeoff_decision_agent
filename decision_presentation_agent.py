from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
import os
from subagents.decision_presentation_subagents import decision_presentation_subagents
from model import get_model

model = get_model()

# Create sandbox
sandbox = os.path.abspath("sandbox")
os.makedirs(sandbox, exist_ok=True)


decision_presentation_agent = create_deep_agent(
    model=model,

    system_prompt = """You are the Decision & Presentation Agent.

Workflow: Research Findings -> Decision Report -> One-slide PPT.

STEP 1 — INSPECT: Call ls on the root and on findings/ and output/ to
see what already exists.

STEP 2 — DECISION STAGE:
- If decision_report.md exists and is non-empty, read it via read_file
  to confirm it has all 11 required sections. If valid, skip this stage.
- Otherwise, delegate to decision_subagent via task. Do not research
  or score anything yourself.

STEP 3 — PPT STAGE (only after decision_report.md is confirmed valid):
- If output/final_decision.pptx already exists, skip this stage.
- Otherwise, delegate to ppt_generation_subagent via task.

RULES:
- Never repeat a completed stage.
- Never invent findings if source files are missing — report the gap
  instead.
- The filesystem is the source of truth: always inspect before acting.

Report the final file paths for decision_report.md and
output/final_decision.pptx and stop.
""",

    subagents=decision_presentation_subagents,
    backend=FilesystemBackend(
            root_dir=sandbox,
            virtual_mode=True,
        ),
)

scenario = """
Should India continue expanding E20 adoption rapidly,
or should it adopt a more gradual approach considering
food security, water security, energy security, and
vehicle/consumer impacts?
"""

result = decision_presentation_agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": scenario
            }
        ]
    }
)
print("++++++DONE+++++++++++++")