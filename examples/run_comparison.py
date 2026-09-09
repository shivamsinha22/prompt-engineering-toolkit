"""
run_comparison.py

End-to-end demo of the toolkit:
  1. Build the same task as 4 different prompt strategies
  2. Send each to the LLM client (mock mode by default)
  3. Score every response
  4. Print a ranked comparison table
  5. Save the full run as a JSON log for later reference
"""

import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from toolkit.prompt_builder import PromptBuilder
from toolkit.api_client import LLMClient
from toolkit.evaluator import Evaluator


def main():
    task_variables = {
        "output_type": "product description",
        "subject": "a smart water bottle that tracks hydration",
        "tone": "friendly",
        "max_words": 60,
        "example_1": "The UltraBrew Mug keeps your coffee at the perfect temp for hours.",
        "example_2": "The TrailPack backpack adapts to any adventure, rain or shine.",
    }

    builder = PromptBuilder()
    client = LLMClient()
    evaluator = Evaluator(
        target_words=60,
        required_keywords=["hydration", "smart", "track", "eco", "design"],
    )

    prompts = builder.build_all(task_variables)
    responses = {}

    print("Running prompt comparison across strategies...\n")
    for strategy, prompt in prompts.items():
        response = client.generate(prompt, strategy_name=strategy)
        responses[strategy] = response
        print(f"--- {strategy} ---")
        print(response)
        print()

    ranked = evaluator.compare(responses)

    print("=" * 60)
    print(f"{'Strategy':<18}{'Score':<8}{'Words':<8}{'Keywords':<10}")
    print("-" * 60)
    for name, s in ranked:
        print(f"{name:<18}{s['overall_score']:<8}{s['word_count']:<8}{s['keyword_hits']:<10}")
    print("=" * 60)
    print(f"Best strategy: {ranked[0][0]} (score: {ranked[0][1]['overall_score']})")

    # Save run to logs/
    log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(
        log_dir, f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "task_variables": task_variables,
                "prompts": prompts,
                "responses": responses,
                "scores": {name: s for name, s in ranked},
            },
            f,
            indent=2,
        )
    print(f"\nFull run saved to {log_path}")


if __name__ == "__main__":
    main()
