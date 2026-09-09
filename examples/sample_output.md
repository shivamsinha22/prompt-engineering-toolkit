# Sample Run: Prompt Strategy Comparison

Task: Write a product description for **"a smart water bottle that tracks hydration"**
(friendly tone, ≤60 words). Run in mock mode — no API key required.

## Responses by Strategy

### zero_shot
> Introducing a smart solution designed for everyday life. With built-in tracking, a sleek
> design, and eco-friendly materials, it's the smart choice for anyone on the move.

### few_shot
> Meet the product that blends style, function, and smart tech. With built-in tracking, a
> sleek design, and eco-friendly materials, it's the smart choice for anyone on the move.

### chain_of_thought
> Reasoning: (1) hydration tracking is a key differentiator, (2) sustainability appeals to
> eco-conscious buyers, (3) app integration adds convenience.
>
> Final description: Stay hydrated smarter with a bottle that thinks ahead. With built-in
> tracking, a sleek design, and eco-friendly materials, it's the smart choice for anyone on
> the move.

### role_based
> As your personal hydration coach, this bottle keeps you on track effortlessly. With
> built-in tracking, a sleek design, and eco-friendly materials, it's the smart choice for
> anyone on the move.

## Scoring Results

| Strategy          | Score | Words | Keyword Hits |
|--------------------|-------|-------|---------------|
| chain_of_thought   | 10.0  | 48    | 5/5           |
| role_based         | 8.2   | 30    | 5/5           |
| few_shot           | 6.76  | 28    | 4/5           |
| zero_shot          | 6.52  | 26    | 4/5           |

**Best strategy: `chain_of_thought`** — it hit all 5 required keywords and landed closest
to the target word count, because reasoning through the selling points first led to more
complete coverage of the product's features.

## Takeaway

This is exactly the kind of signal prompt engineering work should produce: not just "which
output sounds best," but a repeatable, scorable comparison that explains *why* one strategy
outperformed the others for this specific task.
