"""
prompt_builder.py

Loads prompt strategy templates and fills them with task-specific variables
to produce final, ready-to-send prompts.
"""

import json
import os


class PromptBuilder:
    def __init__(self, template_path=None):
        if template_path is None:
            template_path = os.path.join(
                os.path.dirname(__file__), "..", "templates", "strategies.json"
            )
        with open(template_path, "r", encoding="utf-8") as f:
            self.strategies = json.load(f)

    def list_strategies(self):
        """Return the names of all available prompting strategies."""
        return list(self.strategies.keys())

    def describe(self, strategy_name):
        """Return the human-readable description of a strategy."""
        return self.strategies[strategy_name]["description"]

    def build(self, strategy_name, variables):
        """
        Fill a named strategy's template with the given variables dict.

        Example:
            builder.build("zero_shot", {
                "output_type": "product description",
                "subject": "a smart water bottle",
                "tone": "friendly",
                "max_words": 60
            })
        """
        if strategy_name not in self.strategies:
            raise ValueError(
                f"Unknown strategy '{strategy_name}'. "
                f"Available: {self.list_strategies()}"
            )
        template = self.strategies[strategy_name]["template"]
        try:
            return template.format(**variables)
        except KeyError as e:
            raise ValueError(
                f"Missing variable {e} required by strategy '{strategy_name}'"
            )

    def build_all(self, variables):
        """Build prompts for every strategy at once. Returns {strategy: prompt}."""
        return {
            name: self.build(name, variables) for name in self.strategies
        }
