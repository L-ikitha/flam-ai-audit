from pathlib import Path
import unicodedata

path = Path("corpus_sample/eng_sample.txt")

lines = []

with open(path, "r", encoding="utf-8") as f:
    for raw in f:
        line = raw.strip()

        if not line:
            continue

        line = unicodedata.normalize("NFC", line)
        lines.append(line)

for i, line in enumerate(lines, start=1):
    old_words = line.lower().split(" ")
    new_words = line.lower().split()

    if len(old_words) != len(new_words):
        print("Problem found!")
        print("Line number:", i)
        print("Sentence:", line)
        print('split(" ") count:', len(old_words))
        print("split() count:", len(new_words))
        print('split(" ") result:', old_words)
        print("split() result:", new_words)