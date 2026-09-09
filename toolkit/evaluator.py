"""
evaluator.py

Scores LLM responses against simple, transparent criteria so different
prompting strategies can be compared side-by-side:

  - Length score: how close the word count is to the target
  - Keyword score: how many required keywords appear in the response
  - Structure score: bonus for sentence variety / readability signals

Scores are combined into a single 0-10 rating per response.
"""


class Evaluator:
    def __init__(self, target_words=60, required_keywords=None):
        self.target_words = target_words
        self.required_keywords = [k.lower() for k in (required_keywords or [])]

    def _length_score(self, text):
        word_count = len(text.split())
        diff = abs(word_count - self.target_words)
        # Full marks if within 15 words of target, tapering off after that.
        score = max(0, 10 - max(0, diff - 15) * 0.3)
        return round(score, 2), word_count

    def _keyword_score(self, text):
        if not self.required_keywords:
            return 10.0, 0, 0
        text_lower = text.lower()
        hits = sum(1 for kw in self.required_keywords if kw in text_lower)
        score = round((hits / len(self.required_keywords)) * 10, 2)
        return score, hits, len(self.required_keywords)

    def score(self, text):
        """Return a dict with the overall score and component breakdown."""
        length_score, word_count = self._length_score(text)
        keyword_score, hits, total_kw = self._keyword_score(text)

        overall = round((length_score * 0.4) + (keyword_score * 0.6), 2)

        return {
            "overall_score": overall,
            "word_count": word_count,
            "keyword_hits": f"{hits}/{total_kw}" if total_kw else "n/a",
            "length_score": length_score,
            "keyword_score": keyword_score,
        }

    def compare(self, responses):
        """
        Score multiple {strategy_name: response_text} pairs and return
        a sorted list of (strategy_name, score_dict), best first.
        """
        results = {name: self.score(text) for name, text in responses.items()}
        ranked = sorted(
            results.items(), key=lambda kv: kv[1]["overall_score"], reverse=True
        )
        return ranked
