"""
api_client.py

A small, pluggable client for sending prompts to an LLM.
Supports three modes, chosen via the LLM_PROVIDER environment variable:

  - "mock"      (default) — no API key needed, returns a deterministic
                 simulated response so the toolkit is demoable out of the box.
  - "openai"    — requires OPENAI_API_KEY and the `openai` package.
  - "anthropic" — requires ANTHROPIC_API_KEY and the `anthropic` package.
"""

import os
import random


class LLMClient:
    def __init__(self, provider=None):
        self.provider = provider or os.environ.get("LLM_PROVIDER", "mock")

    def generate(self, prompt, strategy_name="unknown"):
        """Send a prompt to the configured provider and return the text response."""
        if self.provider == "openai":
            return self._call_openai(prompt)
        elif self.provider == "anthropic":
            return self._call_anthropic(prompt)
        else:
            return self._mock_response(prompt, strategy_name)

    def _call_openai(self, prompt):
        from openai import OpenAI  # imported lazily so mock mode has zero deps

        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content

    def _call_anthropic(self, prompt):
        import anthropic  # imported lazily so mock mode has zero deps

        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    def _mock_response(self, prompt, strategy_name):
        """
        Deterministic-ish fake response generator so the toolkit can be run
        and demoed with zero setup. Response length/style varies slightly
        by strategy so comparisons look realistic.
        """
        random.seed(strategy_name)  # same strategy -> same mock output each run

        openers = {
            "zero_shot": "Introducing a smart solution designed for everyday life.",
            "few_shot": "Meet the product that blends style, function, and smart tech.",
            "chain_of_thought": (
                "Reasoning: (1) hydration tracking is a key differentiator, "
                "(2) sustainability appeals to eco-conscious buyers, "
                "(3) app integration adds convenience.\n\n"
                "Final description: Stay hydrated smarter with a bottle that "
                "thinks ahead."
            ),
            "role_based": "As your personal hydration coach, this bottle keeps you on track effortlessly.",
        }

        body = openers.get(strategy_name, "This is a generated product description.")
        extra = (
            " With built-in tracking, a sleek design, and eco-friendly materials, "
            "it's the smart choice for anyone on the move."
        )
        return body + extra
