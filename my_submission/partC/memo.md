# Part C - Decision Memo

## Recommendation

Choose **(c) prompt engineering only** as the first intervention.

The assignment describes the current outputs in Hindi, Kannada, Tamil, Telugu, Bengali, and Marathi as too formal/textbook. Prompt engineering is the lowest-risk first intervention because it requires no training run, no additional deployed model, and no external API budget.

Keep the **<=1B inference-time rewriter** as the fallback if prompt-only fails the predefined quality threshold. Do not start with SFT because its data and training requirements are more uncertain under the three-week launch schedule.

## Assumptions

These are planning assumptions, not measurements supplied by the assignment:

- Day-1 pilot: 20 examples/language x 6 languages = **120 examples**.
- Reviewer rate: **2 minutes/example**.
- Conversational-naturalness scale: **1-5**.
- Score 4 or above means clearly conversational output.

## Back-of-envelope arithmetic

Reviewer availability:

**10 h/week x 2 weeks = 20 reviewer-hours.**

At the 2-minute/example planning rate:

**20 x 60 / 2 = 600 reviewable examples.**

The reviewer is fluent only in Hindi and Kannada, so this does not provide native-speaker validation for Tamil, Telugu, Bengali, or Marathi.

For an SFT planning scenario, assume 2,000 synthetic pairs/language and 150 tokens/example:

**2,000 x 6 = 12,000 pairs**

**12,000 x 150 = 1.8M training tokens/epoch**

At 3 epochs:

**1.8M x 3 = 5.4M token presentations.**

The assignment does not provide a base-model checkpoint, training throughput, rewriter benchmark, or infrastructure price. Therefore I do not claim an exact GPU-hour, dollar, latency, or throughput figure.

Prompt-only adds **0 training GPU-hours and 0 additional inference-model stages** relative to the existing system.

## Day-1 experiment

Use the same 120 inputs for:

1. Current baseline prompt.
2. Prompt-only version explicitly requesting natural, casual/conversational language.

Score both with the predefined 1-5 conversational-naturalness rubric. Also check that the intervention does not change intended meaning or factual content.

The comparison should use identical inputs so that the measured difference can be attributed to the prompting intervention.

## Success metric

Prompt-only succeeds if:

- Mean conversational-naturalness **>= 4/5** on examples evaluated by the native reviewer.
- No reviewed language scores **< 3/5**.

Because the available native reviewer covers Hindi and Kannada only, native validation is limited to those languages.

## Kill criterion

By the **end of Week 1**, abandon prompt-only if the native-reviewed evaluation fails either threshold above.

If it fails, run the <=1B rewriter against the same evaluation set and measure conversational quality, semantic/factual preservation, and end-to-end latency.

## Decision rationale

Prompt engineering is the cheapest first experiment and has the lowest deployment risk. The rewriter adds another inference stage; SFT adds synthetic-data, training, and schedule risk.

Therefore, the decision is not that prompting is proven to work. The decision is to **test the lowest-cost intervention first and escalate only when measured evidence shows it is insufficient**.

## Biggest caveat

The largest evidence gap is evaluation coverage: the launch targets six languages, but the available native reviewer covers only Hindi and Kannada. In addition, no Part C model outputs are included in the supplied resources, so no numerical baseline or improvement is claimed here.