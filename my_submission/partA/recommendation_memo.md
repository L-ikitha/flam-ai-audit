# Part A4 - Tokenizer Recommendation Memo

## Decision

The current v0 conclusion that Hindi requires approximately 6x more serving cost than English is not supported. The corrected audit shows that tokenizer choice is a major driver of Indic tokenization efficiency.

## Corrected headline numbers

The audit used 500 sentences each of English, Hindi, Tamil, and Telugu and compared GPT-2 with XLM-R.

For GPT-2, token counts were:

- English: 10,910
- Hindi: 72,510
- Tamil: 110,019
- Telugu: 75,106

For XLM-R:

- English: 11,959
- Hindi: 13,612
- Tamil: 10,993
- Telugu: 8,412

Compared with GPT-2, XLM-R reduced Indic token counts by approximately:

- Hindi: 81.2%
- Tamil: 90.0%
- Telugu: 88.8%

Therefore, the large Indic token inflation observed with GPT-2 is not an inherent property of the scripts. It is strongly dependent on tokenizer vocabulary and segmentation.

The audit also found a real whitespace-counting bug in `fertility.py`: `split(" ")` counts empty strings created by repeated spaces and does not treat all whitespace consistently. Replacing it with `split()` changed the starter-corpus fertility by +1.411%.

## Routing recommendation

Do not route traffic based on the v0 fertility number or on language alone.

For production routing, evaluate the actual tokenizer associated with each candidate model and use its measured token count for the incoming request. An Indic-aware multilingual tokenizer such as XLM-R should be evaluated for Indic traffic because the audit shows substantially lower token counts for Hindi, Tamil, and Telugu than GPT-2.

However, this experiment alone is not sufficient to declare XLM-R the production tokenizer because the corpus contains only 500 sentences per language and is not specifically conversational.

## Biggest caveat

The corpus is a relatively small 500-sentence sample per language derived from a parallel corpus. Its domain and sentence distribution may not represent the casual/conversational traffic expected in production.

Also, tokens/word, tokens/character, and tokens/byte are diagnostic measures rather than direct serving-cost measures. Character counts depend on the definition of "character," while UTF-8 bytes describe text representation rather than model inference cost.

## Production metric to monitor

The primary production metric should be:

**actual input tokenizer tokens per request**, measured using the tokenizer of the model serving that request.

For complete serving-cost analysis, monitor both input and generated output tokens per request, along with latency and throughput.

The routing/capacity decision should therefore be based on actual model token usage rather than a language-level fertility multiplier.