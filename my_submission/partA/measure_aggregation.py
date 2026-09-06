from pathlib import Path
import tiktoken


CORPUS = Path(__file__).parent / "corpus" / "eng.txt"

enc = tiktoken.get_encoding("gpt2")

with open(CORPUS, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]


# Method 1:
# Mean of individual sentence ratios
per_sentence_ratios = []

total_tokens = 0
total_words = 0

for line in lines:
    tokens = enc.encode(line)
    words = line.split()

    per_sentence_ratios.append(len(tokens) / len(words))

    total_tokens += len(tokens)
    total_words += len(words)


mean_of_ratios = sum(per_sentence_ratios) / len(per_sentence_ratios)


# Method 2:
# Corpus-level ratio
corpus_ratio = total_tokens / total_words


print("English corpus — aggregation comparison")
print("----------------------------------------")
print(f"Sentences:                  {len(lines)}")
print(f"Total tokens:               {total_tokens}")
print(f"Total words:                {total_words}")
print(f"Mean of sentence ratios:   {mean_of_ratios:.6f}")
print(f"Corpus-level tok/word:      {corpus_ratio:.6f}")
print(f"Difference:                 {mean_of_ratios - corpus_ratio:.6f}")
print(
    f"Relative difference:        "
    f"{((mean_of_ratios - corpus_ratio) / corpus_ratio) * 100:.3f}%"
)