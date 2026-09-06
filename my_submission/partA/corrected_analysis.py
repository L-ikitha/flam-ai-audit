from pathlib import Path
import tiktoken
from transformers import AutoTokenizer


# --------------------------------------------------
# 1. Paths and tokenizers
# --------------------------------------------------

CORPUS_DIR = Path(__file__).parent / "corpus"

FILES = {
    "eng": "eng.txt",
    "hin": "hin.txt",
    "tam": "tam.txt",
    "tel": "tel.txt",
}

gpt2 = tiktoken.get_encoding("gpt2")
xlmr = AutoTokenizer.from_pretrained("xlm-roberta-base")


# --------------------------------------------------
# 2. Load corpus
# --------------------------------------------------

def load_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


# --------------------------------------------------
# 3. Analyze one language with one tokenizer
# --------------------------------------------------

def analyze(lines, tokenizer_name):
    total_tokens = 0
    total_words = 0
    total_chars = 0
    total_bytes = 0

    for line in lines:

        # Whitespace-word denominator
        words = line.split()

        # Character denominator
        chars = len(line)

        # UTF-8 byte denominator
        bytes_count = len(line.encode("utf-8"))

        # Token count
        if tokenizer_name == "gpt2":
            tokens = gpt2.encode(line)

        elif tokenizer_name == "xlmr":
            tokens = xlmr.encode(
                line,
                add_special_tokens=False
            )

        total_tokens += len(tokens)
        total_words += len(words)
        total_chars += chars
        total_bytes += bytes_count

    return {
        "tokens": total_tokens,
        "words": total_words,
        "chars": total_chars,
        "bytes": total_bytes,
        "tok_per_word": total_tokens / total_words,
        "tok_per_char": total_tokens / total_chars,
        "tok_per_byte": total_tokens / total_bytes,
    }


# --------------------------------------------------
# 4. Run analysis
# --------------------------------------------------

print("CORRECTED TOKENIZER ANALYSIS")
print("=" * 80)
print("Corpus: 500 sentences per language")
print("Languages: English, Hindi, Tamil, Telugu")
print("Tokenizers: GPT-2 and XLM-R")
print()


for language, filename in FILES.items():

    lines = load_lines(CORPUS_DIR / filename)

    print(f"\nLANGUAGE: {language}")
    print("-" * 80)

    for tokenizer_name in ["gpt2", "xlmr"]:

        result = analyze(lines, tokenizer_name)

        print(f"\nTokenizer: {tokenizer_name}")
        print(f"  Total tokens:       {result['tokens']}")
        print(f"  Total words:        {result['words']}")
        print(f"  Total characters:   {result['chars']}")
        print(f"  Total UTF-8 bytes:  {result['bytes']}")
        print(f"  Tokens / word:      {result['tok_per_word']:.4f}")
        print(f"  Tokens / character: {result['tok_per_char']:.4f}")
        print(f"  Tokens / byte:      {result['tok_per_byte']:.4f}")