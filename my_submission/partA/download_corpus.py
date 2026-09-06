from datasets import load_dataset
from pathlib import Path


# --------------------------------------------------
# Configuration
# --------------------------------------------------

NUM_SENTENCES = 500

OUTPUT_DIR = Path(__file__).parent / "corpus"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Helper function
# --------------------------------------------------

def collect_sentences(language_code, output_filename, field):
    print(f"\nLoading Samanantar: {language_code}")

    dataset = load_dataset(
        "ai4bharat/samanantar",
        language_code,
        split="train",
        streaming=True
    )

    sentences = []

    for row in dataset:
        sentence = row[field].strip()

        # Basic quality filtering
        if not sentence:
            continue

        # Ignore extremely long entries
        if len(sentence) > 500:
            continue

        sentences.append(sentence)

        if len(sentences) == NUM_SENTENCES:
            break

    output_path = OUTPUT_DIR / output_filename

    with open(output_path, "w", encoding="utf-8") as f:
        for sentence in sentences:
            f.write(sentence + "\n")

    print(f"Saved {len(sentences)} sentences to {output_path}")


# --------------------------------------------------
# English
# --------------------------------------------------
# We take English from the Hindi-English subset.
# This gives us a deterministic English sample.

collect_sentences(
    language_code="hi",
    output_filename="eng.txt",
    field="src"
)


# --------------------------------------------------
# Hindi
# --------------------------------------------------

collect_sentences(
    language_code="hi",
    output_filename="hin.txt",
    field="tgt"
)


# --------------------------------------------------
# Tamil
# --------------------------------------------------

collect_sentences(
    language_code="ta",
    output_filename="tam.txt",
    field="tgt"
)


# --------------------------------------------------
# Telugu
# --------------------------------------------------

collect_sentences(
    language_code="te",
    output_filename="tel.txt",
    field="tgt"
)


print("\nCorpus creation complete!")