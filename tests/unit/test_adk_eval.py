# tests/integration/test_adk_eval.py

import asyncio
from pathlib import Path

from google.adk.evaluation.agent_evaluator import AgentEvaluator


EVAL_DIR = Path(__file__).parents[2] / "src" / "capstone" / "scripts" / "eval"


def test_adk_eval_runs_successfully():
    async def _run():
        await AgentEvaluator.evaluate(
            agent_module="capstone.scripts.eval.agent",
            eval_dataset_file_path_or_dir=str(EVAL_DIR),
        )

    asyncio.run(_run())
