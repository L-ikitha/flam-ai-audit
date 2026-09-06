# A1 — Multilingual Evaluation Corpus

## Languages

The evaluation corpus contains four languages:

- English (`eng`)
- Hindi (`hin`)
- Tamil (`tam`)
- Telugu (`tel`)

This satisfies the requirement to evaluate English, Hindi, and two Dravidian languages.

## Source

The corpus was constructed from the AI4Bharat Samanantar dataset available through Hugging Face.

Dataset:
- `ai4bharat/samanantar`

Samanantar provides English–Indic parallel sentence pairs. We used:
- `hi` configuration for English and Hindi
- `ta` configuration for English and Tamil
- `te` configuration for English and Telugu

For each configuration, the English sentence is stored in the `src` field and the Indic-language sentence is stored in the `tgt` field.

## Corpus Size

We extracted 500 sentences per language:

| Language | Sentences |
|---|---:|
| English | 500 |
| Hindi | 500 |
| Tamil | 500 |
| Telugu | 500 |
| **Total** | **2,000** |

The sentence counts were verified using PowerShell `Get-Content` with UTF-8 encoding.

## Extraction Procedure

The dataset was accessed using the Hugging Face `datasets` library with:

- `split="train"`
- `streaming=True`

Streaming was used so that the complete large dataset did not need to be downloaded locally.

We sequentially collected sentences until 500 usable sentences had been obtained for each language.

## Preprocessing

The extraction script applied only minimal preprocessing:

1. Leading and trailing whitespace was removed using `.strip()`.
2. Empty sentences were discarded.
3. Sentences longer than 500 characters were discarded.
4. No translation or rewriting was performed.
5. No lowercasing was performed.
6. No punctuation removal was performed.
7. Unicode text was preserved using UTF-8 encoding.
8. Each sentence was written as one line in its corresponding `.txt` file.

## Domain

Samanantar is a broad English–Indic parallel corpus rather than a corpus specifically designed for conversational dialogue.

Therefore, the resulting evaluation corpus should be considered **general-domain multilingual text**, not a representative sample of casual user conversations.

The extracted examples may include news, informational, literary, religious, entertainment, and other general-domain material.

## Caveats

1. The corpus is derived from parallel translation data, so it may not represent naturally occurring monolingual text.
2. The domain distribution may differ across languages.
3. The first 500 usable sentences from each streamed configuration are not necessarily statistically representative of the entire dataset.
4. The corpus contains only four languages and therefore does not represent all Indic languages.
5. The corpus is substantially larger than the original 10-sentence-per-language starter samples, but 500 sentences per language is still a relatively small evaluation corpus.
6. Tokenizer results should therefore be interpreted as evidence for this evaluation corpus rather than as universal language-level properties.

## Reproducibility

The corpus was generated using:

```text
my_submission/partA/download_corpus.py


The generated files are:

eng.txt
hin.txt
tam.txt
tel.txt


### One correction before you save it

There's an important distinction we should preserve:

**We have verified the dataset and our extraction process, but we have NOT yet independently verified every statement about Samanantar's overall domain/content distribution.**

So don't present those broader domain claims as experimentally measured facts. In the final audit, we'll distinguish:

- **What we directly measured** → 500 sentences, languages, extraction, preprocessing.
- **What the dataset documentation says** → source/dataset characteristics.
- **Our caveats/inference** → representativeness limitations.

That's exactly the kind of evidence discipline this assignment is looking for.

---

### Next

After saving `corpus_metadata.md`, **don't run fertility.py yet**.

Our next A1 step is to create a **corpus quality check** that measures things such as:

- number of lines
- character counts
- word counts
- empty lines
- duplicate sentences
- Unicode validity

That gives us actual evidence that the four corpora are usable **before** we start the tokenizer audit.

