# src/capstone/scripts/run_eval.py

import asyncio
import sys
from pathlib import Path

from google.adk.evaluation.agent_evaluator import AgentEvaluator


# run_eval.py の位置:
# src/capstone/scripts/run_eval.py
# → プロジェクトルートは 3 つ上
PROJECT_ROOT = Path(__file__).resolve().parents[3]

EVAL_DIR = PROJECT_ROOT / "src" / "capstone" / "scripts" / "eval"
AGENT_MODULE = "capstone.scripts.eval.agent"


async def main():
    print("=== Running ADK eval via AgentEvaluator ===")
    print(f"- agent_module: {AGENT_MODULE}")
    print(f"- eval dir    : {EVAL_DIR} (exists={EVAL_DIR.exists()})")

    if not EVAL_DIR.exists():
        print("ERROR: Eval directory not found.")
        return 1

    try:
        await AgentEvaluator.evaluate(
            agent_module=AGENT_MODULE,
            eval_dataset_file_path_or_dir=str(EVAL_DIR),
            num_runs=1,
        )
    except AssertionError as e:
        print("\n=== Evaluation FAILED ===")
        print(str(e))
        return 1
    except Exception as e:
        print("\n=== Evaluation ERROR ===")
        print(type(e), str(e))
        return 1

    print("\n=== Evaluation PASSED ===")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
