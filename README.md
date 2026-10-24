# Aitells — open spec for AI-writing-tells detection

**Aitells** (AI + tells) is a rules-based heuristic spec for detecting common
AI-writing tells: vocabulary ("delve", "tapestry", "pivotal"), hype verbs,
"not just X but Y" structures, hedging, transition-word stuffing, em-dash
overuse, rule-of-three lists, uniform sentence length and formulaic sentence
starts.

It is **not proof of AI authorship** — it is a signal, with an honest,
explainable score.

* Live API: `https://utils.bigfloppy.net/v1/aitells`
* Reference implementation: [`aitells.py`](aitells.py) (~90 lines, MIT, no deps)
* Python client: [`client.py`](client.py) — JavaScript: [`js/example.mjs`](js/example.mjs)

## Quick start (no account needed)

```bash
curl -s -X POST https://utils.bigfloppy.net/v1/aitells \
  -H 'Content-Type: application/json' \
  -d '{"text":"In today'"'"'s fast-paced world, it is not just important — it is crucial."}'
```

Response (abridged):

```json
{
  "score": 78,
  "verdict": "strong AI-writing signals",
  "words": 16,
  "categories": {"hype": 2, "structure": 2, "vocab": 1},
  "style": {"em_dash_count": 1, "rule_of_three_lists": 0,
            "sentence_len_stdev": 0.0, "formulaic_sentence_starts_pct": 100.0},
  "top_patterns": [{"pattern": "\\bin today'?s\\b", "category": "structure", "count": 1}]
}
```

## Scoring model (deterministic, no LLM)

| Component | Weight |
|---|---|
| tells per 1k words | ×5 |
| em-dashes per 1k words | ×8 |
| rule-of-three triads per 1k words | ×6 |
| sentence-length stdev < 4.5 (n≥8 sentences) | +18 |
| formulaic starts > 25% / > 15% | +15 / +7 |

Score is clamped to 0–99. Verdicts: `0–19` no strong AI tells · `20–39` mixed
signals · `40–63` likely AI-assisted or unedited AI · `64+` strong AI-writing
signals. Humans use em-dashes too; AI-free text scores 0–20.

## Paid tier (detailed report)

`POST /v1/aitells/detailed` returns every pattern match with sentence-level
examples — useful for editors triaging content farms. Pricing is machine-native
[x402](https://www.x402.org): the first request returns `402` with a
`WWW-Authenticate` challenge; pay the quoted USDC amount to the challenge
address and retry with the `X-PAYMENT` header. No signups, no API keys.

```js
const r = await fetch('https://utils.bigfloppy.net/v1/aitells/detailed', {method:'POST',
  headers:{'Content-Type':'application/json'},
  body: JSON.stringify({text})});
if (r.status === 402) {
  const challenge = JSON.parse(r.headers.get('WWW-Authenticate') ?? '{}');
  // pay challenge.amountUSDC to challenge.payTo with any x402-compatible wallet…
}
```

## Reference rules

See `aitells.py` — the single source of truth for the rule list. PRs that add
a rule **must** include a one-line example text that triggers it and one that
shouldn't.

## License

MIT.
