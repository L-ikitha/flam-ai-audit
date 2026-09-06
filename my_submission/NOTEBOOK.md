# FlamAI AI Team Intern Assignment â€” Audit Notebook

This notebook records the investigation chronologically using:

Hypothesis â†’ Experiment â†’ Result â†’ Revision

Experimental numbers are based on the supplied starter resources or scripts
run locally. Planning assumptions are explicitly labeled as assumptions.

---

# Part A â€” Tokenizer Audit

## Experiment 1 â€” Reproduce v0

### Hypothesis

The previous report's tokenizer numbers should be reproducible from the
supplied `fertility.py` and sample corpora.

### Experiment

Ran:

    python fertility.py --corpus eng=corpus_sample/eng_sample.txt --corpus hin=corpus_sample/hin_sample.txt --tokenizer gpt2

### Result

English fertility: 1.27 tok/word

Hindi fertility: 7.45 tok/word

Hindi/English ratio: 5.89x

### Revision

The v0 numbers are reproducible, so the original measurements can be
audited directly rather than relying only on the report.

---

## Experiment 2 â€” Repeated Whitespace

### Hypothesis

Using `split(" ")` may count empty strings as words when repeated whitespace
occurs.

### Experiment

Compared `split(" ")` with `split()` on the supplied English corpus while
keeping the tokenizer and fertility calculation unchanged.

### Result

`split(" ")`: 79 words

`split()`: 78 words

The problematic sentence was:

    "Please keep the books  in the cupboard."

For the fertility calculation:

Original: 1.265206 tok/word

Corrected: 1.283063 tok/word

Absolute change: +0.017857 tok/word

Relative change: +1.411%

### Revision

The implementation has a real word-counting bug.

`split(" ")` counts empty strings created by repeated spaces as words,
which increases the denominator and therefore underestimates fertility.

The measured effect on this small English sample is +1.41%, so the bug
should be reported without overstating its magnitude.

---

## Experiment 3 â€” Lowercasing

### Hypothesis

Lowercasing the corpus may change tokenizer counts, so preprocessing
choices should be treated as part of the fertility measurement.

### Experiment

Compared GPT-2 token counts on the supplied English sample with and without
lowercasing, while keeping the corpus and tokenizer unchanged.

### Result

Original GPT-2 token count: 96

Lowercased GPT-2 token count: 99

Absolute change: +3 tokens

Relative change: +3.125%

Affected lines: 2, 6, and 10.

### Revision

Lowercasing changes the measured token count and therefore changes fertility.

It should not be applied silently.

The corrected analysis keeps the original capitalization and documents
preprocessing explicitly.

---

## Experiment 4 â€” Per-Sentence vs Corpus-Level Aggregation

### Hypothesis

Averaging per-sentence fertility ratios may produce a different result from
computing total tokens divided by total words.

### Experiment

Measured GPT-2 fertility on the 500-sentence English corpus using:

1. Mean of individual sentence token/word ratios.
2. Total tokens divided by total words.

### Result

Total tokens: 10,910

Total words: 8,382

Corpus-level ratio:

    10,910 / 8,382 = 1.301599 tok/word

Mean sentence-level ratio:

    1.308973 tok/word

Absolute difference:

    0.007374 tok/word

Relative difference:

    approximately 0.567%

### Revision

Both calculations are mathematically valid, but they answer different
questions.

For corpus-level routing and cost analysis, total tokens divided by total
words is the clearer aggregate because it uses the total corpus denominator.

---

## Experiment 5 â€” Unicode NFC Normalization

### Hypothesis

Unicode normalization may change tokenizer behavior for visually identical
text represented by different Unicode sequences.

### Experiment

Compared:

    cafÃ©

with:

    cafe + combining acute accent

Measured GPT-2 token counts before and after NFC normalization.

### Result

Before NFC normalization:

    cafÃ©: 3 tokens
    cafe + combining acute accent: 4 tokens

After NFC normalization:

    both forms: 3 tokens

### Revision

NFC normalization is not a bug in this context.

It makes canonically equivalent Unicode representations consistent before
tokenization.

Although normalization initially looked suspicious because it changes the
input representation, the controlled experiment showed that it removes an
encoding-representation difference rather than introducing a counting error.

---

## Experiment 6 â€” GPT-2 vs XLM-R

### Hypothesis

If high Indic fertility were primarily caused by the scripts themselves,
different tokenizers should show similarly poor behavior.

### Experiment

Compared GPT-2 and XLM-R on 10 English and 10 Hindi sentences using the
same text and whitespace-word denominator.

### Result

English:

    GPT-2: 96 tokens / 78 words = 1.231 tok/word
    XLM-R: 97 tokens / 78 words = 1.244 tok/word

Hindi:

    GPT-2: 459 tokens / 61 words = 7.525 tok/word
    XLM-R: 88 tokens / 61 words = 1.443 tok/word

XLM-R therefore produced approximately 80.8% fewer Hindi tokens than GPT-2
on this small comparison.

### Revision

The result contradicts the interpretation that all tokenizers inherently
struggle with Hindi.

Tokenization efficiency is strongly tokenizer-dependent.

This motivated a larger four-language corrected analysis using 500 sentences
per language.

---

## Experiment 7 â€” Build a Multilingual Evaluation Corpus

### Hypothesis

A larger multilingual corpus covering English and multiple Indic languages
will provide a more useful basis for tokenizer comparison than the original
two-language sample.

### Experiment

Created a local corpus using AI4Bharat Samanantar with:

- English
- Hindi
- Tamil
- Telugu

Used 500 sentences per language.

Total:

    500 Ã— 4 = 2,000 sentences

Preprocessing:

- strip surrounding whitespace
- discard empty sentences
- discard sentences longer than 500 characters
- preserve capitalization
- preserve punctuation
- no translation or rewriting
- UTF-8 encoding

### Result

The resulting corpus contains 500 sentences for each of the four languages.

The corpus was checked for:

- line counts
- duplicate lines
- invalid Unicode
- word counts
- character counts

### Revision

The corpus is suitable for a controlled tokenizer comparison, but it is
still limited in size and domain.

It is a broad-domain parallel corpus rather than a conversational corpus,
so production conclusions should remain cautious.

---

## Experiment 8 â€” Corrected Multilingual Tokenizer Analysis

### Hypothesis

After correcting the word-counting issue and explicitly defining the
preprocessing, comparing GPT-2 and XLM-R on the larger multilingual corpus
will provide a better basis for routing and cost conclusions.

### Experiment

Used:

- 500 sentences each
- English, Hindi, Tamil, Telugu
- GPT-2 and XLM-R

Measured:

- total tokenizer tokens
- whitespace-separated words
- Unicode characters
- UTF-8 bytes
- tokens/word
- tokens/character
- tokens/byte

### Result

English:

    GPT-2:
      tokens = 10,910
      words = 8,382
      tok/word = 1.3016
      tok/char = 0.2189
      tok/byte = 0.2189

    XLM-R:
      tokens = 11,959
      words = 8,382
      tok/word = 1.4267
      tok/char = 0.2400
      tok/byte = 0.2400

Hindi:

    GPT-2:
      tokens = 72,510
      words = 9,141
      tok/word = 7.9324
      tok/char = 1.5283
      tok/byte = 0.5944

    XLM-R:
      tokens = 13,612
      words = 9,141
      tok/word = 1.4891
      tok/char = 0.2869
      tok/byte = 0.1116

Tamil:

    GPT-2:
      tokens = 110,019
      words = 4,529
      tok/word = 24.2921
      tok/char = 2.7159
      tok/byte = 0.9942

    XLM-R:
      tokens = 10,993
      words = 4,529
      tok/word = 2.4272
      tok/char = 0.2714
      tok/byte = 0.0993

Telugu:

    GPT-2:
      tokens = 75,106
      words = 3,607
      tok/word = 20.8223
      tok/char = 2.6894
      tok/byte = 0.9928

    XLM-R:
      tokens = 8,412
      words = 3,607
      tok/word = 2.3321
      tok/char = 0.3012
      tok/byte = 0.1112

Compared with GPT-2, XLM-R reduced Indic token counts by approximately:

    Hindi: 81.2%
    Tamil: 90.0%
    Telugu: 88.8%

### Revision

The corrected analysis strongly supports tokenizer-dependent routing rather
than language-only routing.

Tokens/word, tokens/character, and tokens/byte are useful diagnostic
measurements, but actual tokenizer tokens per request should drive
production routing and cost estimation because model inference and context
usage depend directly on the tokens processed by the selected tokenizer.

### Caveats

The corpus contains only 500 sentences per language.

It is sourced from a parallel corpus and is not specifically conversational.

Unicode code points are not the same thing as user-perceived graphemes.

Therefore these measurements should not be treated as universal production
fertility values.

---

# Part B â€” Capacity Audit

## Experiment 1 â€” KV-Cache Capacity

### Hypothesis

The model specification should allow the KV-cache memory required per token
and the approximate number of 4096-token sequences fitting on the L4 GPU to
be calculated directly.

### Experiment

Used the supplied model specification:

- 28 layers
- 8 KV heads
- head dimension 128
- FP16 KV cache = 2 bytes/value

KV-cache bytes per token:

    2 Ã— 28 Ã— 8 Ã— 128 Ã— 2
    = 114,688 bytes
    = 112 KiB

For a 4096-token sequence:

    114,688 Ã— 4096
    = 469,762,048 bytes
    = 448 MiB

Usable GPU memory:

    24 GB Ã— 0.92
    = 22.08 GB

After subtracting the supplied 1.6 GB non-KV runtime overhead:

    22.08 âˆ’ 1.6
    = 20.48 GB

Approximate number of complete 4096-token sequences:

    20.48 / 0.469762
    â‰ˆ 43.6

Therefore:

    approximately 43 complete sequences

### Result

The simplified theoretical capacity is approximately 43 sequences.

The benchmark shows:

    Batch 24: 93% KV utilization, 0 preemptions
    Batch 32: 97% KV utilization, 7 preemptions
    Batch 48: 97% KV utilization, 23 preemptions

### Revision

The theoretical 43-sequence calculation should not be treated as a safe
production batch size.

The benchmark shows that scheduler/KV-cache pressure appears before that
theoretical upper bound becomes practically useful.

Practical concurrency should therefore be based on measured behavior.

---

## Experiment 2 â€” Long-Context Throughput Anomaly

### Hypothesis

The apparent increase in throughput for long prompts may be caused by the
definition of the throughput counter rather than by faster generation.

### Experiment

Inspected the long-context rows where:

    prompt_len = 3584
    gen_len = 512

For batch 24:

    24 Ã— (3584 + 512) / 61.16
    â‰ˆ 1607.3 tok/s

This matches the reported:

    1607.4 tok/s

Therefore the `reported_tok_s` value includes both prompt and generated
tokens.

### Result

Reported throughput:

    Batch 24: 1607.4 tok/s
    Batch 32: 1384.0 tok/s
    Batch 48: 1298.5 tok/s

Actual generated-token rates:

    Batch 24: 200.9 tok/s
    Batch 32: 173.0 tok/s
    Batch 48: 162.3 tok/s

KV-cache utilization and preemptions:

    Batch 24: 93%, 0 preemptions
    Batch 32: 97%, 7 preemptions
    Batch 48: 97%, 23 preemptions

### Revision

The apparent long-context throughput advantage is misleading because the
reported counter includes the large prompt-token contribution.

Increasing concurrency beyond batch 24 reduces useful generated-token
throughput and coincides with increased KV-cache/scheduler pressure.

### Proposed Configuration Change

For this deployment, cap long-context concurrency at batch 24, or use a
separate long-context serving pool with an equivalent concurrency limit.

The observed generated throughput at batch 24 is approximately 200.9 tok/s.

This is approximately:

    16.1% higher than batch 32
    23.8% higher than batch 48

Batch 24 also has zero observed preemptions in the supplied benchmark.

---

## Experiment 3 â€” Correcting the Misread Throughput Column

### Hypothesis

The previous report's claim that longer prompts improve throughput may have
been caused by misinterpreting the `reported_tok_s` column.

### Experiment

Used two independent calculations for batch 24.

Method 1 â€” generated tokens divided by wall-clock time:

    24 Ã— 512 / 61.16
    = 200.9 generated tok/s

Method 2 â€” remove the prompt contribution from reported throughput:

    1607.4 Ã— 512 / (3584 + 512)
    â‰ˆ 200.9 generated tok/s

### Result

Both methods produce approximately:

    200.9 generated tok/s

Observed long-context generated goodput:

    Batch 24: 200.9 tok/s
    Batch 32: 173.0 tok/s
    Batch 48: 162.3 tok/s

The previous estimate of approximately 3200 tok/s at batch 48 is not
supported by the supplied benchmark.

### Revision

The correct interpretation is that larger long-context batches do not
produce better useful generation throughput in this benchmark.

The report should instead state that concurrency beyond batch 24 increases
KV-cache/scheduler pressure and reduces generated-token goodput.

---

## Experiment 4 â€” Serving Metric for the Proposed Mechanism

### Hypothesis

If KV-cache/scheduler pressure causes the throughput degradation, a
preemption/recompute metric should increase as long-context concurrency
increases.

### Experiment

Used the supplied `preempted_seqs` benchmark column as the available evidence.

### Result

    Batch 24: 0 preempted sequences
    Batch 32: 7 preempted sequences
    Batch 48: 23 preempted sequences

### Revision

The increasing preemption count supports the KV-cache/scheduler-pressure
explanation.

For production serving, a KV-cache sequence preemption/recompute counter
would be an appropriate metric to monitor.

The exact framework-specific counter name is not specified by the supplied
resources.

---

# Part C â€” Decision Analysis

## Initial Constraints

### Hypothesis

The best solution should satisfy the product requirement while respecting
the limited compute, reviewer capacity, and three-week launch deadline.

### Experiment / Analysis

The assignment provides:

- Target languages: Hindi, Kannada, Tamil, Telugu, Bengali, Marathi
- Compute: 1 Ã— A100-80GB
- Experiment/training window: 2 weeks
- Native reviewer: Hindi + Kannada
- Reviewer availability: 10 hours/week
- Launch deadline: 3 weeks
- External API budget: none

### Result

Available reviewer time over two weeks:

    10 hours/week Ã— 2 weeks
    = 20 reviewer-hours

The assignment does not specify a reviewer examples/hour rate.

### Revision

No reviewer throughput number should be treated as a supplied fact.

Any review-rate calculation must explicitly state its assumption.

---

## Experiment 1 â€” Day-1 Experiment Design

### Hypothesis

Prompt engineering may be sufficient to make the assistant's responses more
casual and conversational without the cost and deployment complexity of
training or adding a separate rewriter model.

### Experiment

Proposed a balanced pilot set:

    Hindi:    20 examples
    Kannada:  20 examples
    Tamil:    20 examples
    Telugu:   20 examples
    Bengali:  20 examples
    Marathi:  20 examples
    -----------------------
    Total:   120 examples

This 120-example pilot size is an experiment-design choice, not a fact
supplied by the assignment.

Compare:

    Current baseline prompt
    vs
    Prompt-only conversational version

using identical inputs.

### Evaluation

Proposed conversational-naturalness scale:

    1 = very formal/unnatural
    2 = mostly formal
    3 = acceptable but somewhat formal
    4 = clearly conversational/natural
    5 = highly natural

Proposed success criterion:

    average score >= 4/5

with:

    no reviewed language below 3/5

### Revision

The assignment only provides a native reviewer for Hindi and Kannada.

Therefore native-speaker validation cannot honestly be claimed for Tamil,
Telugu, Bengali, or Marathi.

The 120-example set and 1â€“5 scale are proposed experimental choices rather
than measured evidence.

---

## Experiment 2 â€” Part C Baseline Evidence

### Hypothesis

A quantitative baseline should be established before claiming that any
intervention improves conversational quality.

### Experiment

Inspected the supplied resources for:

- current model outputs
- model checkpoint
- baseline responses
- baseline conversational-naturalness scores
- response-generation benchmark

### Result

The supplied resources do not contain:

- baseline model outputs for the six target languages
- a baseline conversational-naturalness score
- an executable Part C model checkpoint
- a Part C response-generation benchmark

The assignment itself provides only the qualitative statement that current
outputs are too formal/textbook.

### Revision

The qualitative baseline is recorded as an assignment-provided scenario.

No numerical baseline quality score is claimed.

A numerical baseline must be generated by the proposed Day-1 experiment if
the actual model becomes available.

---

## Experiment 3 â€” <=1B Inference-Time Rewriter

### Hypothesis

A small <=1B rewriter could transform the main model's formal/textbook
responses into more casual and conversational responses without retraining
the main model.

### Proposed Architecture

    User request
        â†“
    Main assistant
        â†“
    Draft response
        â†“
    <=1B rewriter
        â†“
    Final conversational response

The rewriter should preserve the meaning and factual content of the draft
while changing only the response style.

### Analysis

Main-model-only path:

    1 main-model generation

Rewriter path:

    1 main-model generation
    + 1 rewriter inference

The supplied resources do not contain:

- a <=1B rewriter checkpoint
- inference benchmark
- serving configuration
- infrastructure pricing

### Result

No numerical latency, throughput, or dollar-cost claim can be made for
the rewriter from the supplied resources.

### Revision

If prompt-only fails its success criterion, the rewriter becomes the next
experiment.

The same evaluation set should be used for:

    1. Baseline
    2. Prompt-only
    3. Main model + <=1B rewriter

Measure:

- conversational-naturalness
- semantic preservation
- factual preservation
- rewriter latency
- end-to-end latency

---

## Experiment 4 â€” SFT Feasibility

### Hypothesis

SFT could teach the main model the desired conversational style directly,
but it requires a sufficiently large and useful synthetic training set,
training compute, and evaluation time.

### Planning Assumptions

These are planning assumptions, not measurements supplied by the assignment:

1. 2,000 synthetic casualized pairs per target language.
2. Six target languages.
3. Approximately 150 tokens per training example.
4. Three training epochs.
5. Reviewer availability of 10 hours/week for two weeks.
6. Two minutes per reviewed example.

### Data-Volume Arithmetic

    2,000 examples/language Ã— 6 languages
    = 12,000 synthetic training pairs

At approximately 150 tokens/example:

    12,000 Ã— 150
    = 1,800,000 training tokens per epoch

For three epochs:

    1,800,000 Ã— 3
    = 5,400,000 token presentations

### Reviewer Arithmetic

Available reviewer time:

    10 Ã— 2
    = 20 reviewer-hours

Under the 2-minute/example assumption:

    20 Ã— 60 / 2
    = 600 examples

However, the reviewer is specified as fluent only in Hindi and Kannada.

Therefore the full 12,000-example synthetic dataset cannot be
native-speaker reviewed under the stated constraint.

### Training-Cost Limitation

The supplied resources do not provide:

- SFT base-model checkpoint
- training throughput
- GPU utilization
- GPU rental/electricity price
- framework configuration

Therefore an exact GPU-hour or dollar-cost estimate cannot be derived.

### Revision

SFT is technically possible in principle, but its schedule and training
cost are uncertain.

It introduces more dependencies than prompt-only:

    synthetic data
        â†“
    data validation
        â†“
    training
        â†“
    evaluation
        â†“
    launch review

Therefore SFT should not be the first experiment unless simpler approaches
fail.

---

## Experiment 5 â€” Final Part C Decision

### Hypothesis

The simplest intervention that can be evaluated quickly should be tested
before introducing training or another serving model.

### Experiment / Decision Analysis

Compared:

### (a) SFT

Advantages:

- Changes the main model's behavior directly.
- No additional inference-stage model after deployment.

Risks:

- Synthetic training data required.
- Training run required.
- Data-quality validation required.
- Training throughput is unknown.
- Exact GPU cost is unknown.
- Native reviewer covers only Hindi and Kannada.
- Three-week launch schedule creates schedule risk.

### (b) <=1B Rewriter

Advantages:

- No main-model retraining required.
- Can target response style after generation.

Risks:

- Adds another inference stage.
- Adds serving complexity.
- Adds latency.
- No rewriter checkpoint or benchmark is supplied.

### (c) Prompt Engineering

Advantages:

- No training.
- No additional model deployment.
- No external API.
- Lowest implementation complexity.
- Can be tested immediately.

Risk:

- Prompting may not be sufficient to reach the desired conversational
  quality.

### Result

Select:

    (c) Prompt Engineering Only

as the first intervention.

This decision is based on the supplied constraints and relative
implementation risk.

It is NOT based on a claimed measured improvement because the supplied
resources contain no executable Part C model or outputs.

### Revision / Fallback

If prompt-only fails the predefined success criterion by the end of Week 1:

    Move to the <=1B inference-time rewriter.

If the rewriter also fails or has unacceptable serving cost/latency:

    Consider SFT if its measured benefit justifies the remaining
    compute and schedule.

---

## Part C â€” Final Decision Rule

Use the simplest intervention that meets the predefined quality threshold.

    1. Test prompt-only first.
    2. Keep prompt-only if it achieves the success criterion.
    3. If it fails by the end of Week 1, test the <=1B rewriter.
    4. Consider SFT only if simpler approaches fail and measured benefit
       justifies the remaining compute and schedule.

---

# Evidence Boundaries

The following distinctions are intentional.

## Measured locally

- Part A tokenizer counts
- Part A fertility changes
- Part A aggregation comparison
- Part A Unicode normalization test
- Part A GPT-2 vs XLM-R comparison
- Part A multilingual tokenizer analysis
- Part B KV-cache arithmetic
- Part B throughput calculations
- Part B generated-token goodput
- Part B benchmark/preemption observations

## Supplied by the assignment

- Part C target languages
- A100-80GB compute constraint
- two-week experiment/training window
- reviewer language coverage
- reviewer availability
- three-week launch review
- no external API budget
- qualitative statement that current responses are too formal/textbook

## Explicit planning assumptions

- 20 examples per language for the Day-1 pilot
- 120 total pilot examples
- 1â€“5 conversational-naturalness scale
- success threshold of >=4/5
- 2,000 synthetic SFT pairs per language
- 150 tokens/example
- three SFT epochs
- two minutes per reviewed example

## Not claimed because the supplied resources do not support them

- numerical Part C baseline quality
- prompt-only quality improvement
- rewriter quality improvement
- SFT quality improvement
- exact SFT GPU hours
- exact dollar training cost
- exact rewriter latency
- exact rewriter serving cost

These quantities require an actual model, benchmark, or additional
infrastructure information.
