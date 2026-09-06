from pathlib import Path
import unicodedata
import tiktoken

path = Path("corpus_sample/eng_sample.txt")

lines = []

with open(path, "r", encoding="utf-8") as f:
    for raw in f:
        line = raw.strip()

        if not line:
            continue

        line = unicodedata.normalize("NFC", line)
        lines.append(line)

enc = tiktoken.get_encoding("gpt2")

old_results = []
new_results = []

for line in lines:
    line = line.lower()

    tokens = enc.encode(line)

    old_words = line.split(" ")
    new_words = line.split()

    old_fertility = len(tokens) / len(old_words)
    new_fertility = len(tokens) / len(new_words)

    old_results.append(old_fertility)
    new_results.append(new_fertility)

old_fertility = sum(old_results) / len(old_results)
new_fertility = sum(new_results) / len(new_results)

print("Original fertility:", old_fertility)
print("Corrected fertility:", new_fertility)
print("Difference:", new_fertility - old_fertility)
print("Relative change (%):",
      (new_fertility - old_fertility) / old_fertility * 100)
