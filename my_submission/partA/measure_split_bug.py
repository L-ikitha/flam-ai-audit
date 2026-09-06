from pathlib import Path
import tiktoken


CORPUS = Path(__file__).parents[2] / "corpus_sample" / "eng_sample.txt"

enc = tiktoken.get_encoding("gpt2")


with open(CORPUS, "r", encoding="utf-8") as f:
    lines = []

    for raw in f:
        line = raw.strip()

        if line:
            lines.append(line)


def calculate(use_correct_split):
    fertility_values = []

    for line in lines:
        line = line.lower()

        tokens = enc.encode(line)

        if use_correct_split:
            words = line.split()
        else:
            words = line.split(" ")

        fertility_values.append(len(tokens) / len(words))

    return sum(fertility_values) / len(fertility_values)


original = calculate(False)
corrected = calculate(True)

absolute_change = corrected - original
relative_change = (absolute_change / original) * 100


print("Starter English corpus")
print("----------------------")
print(f"Original split(' ') fertility : {original:.6f}")
print(f"Corrected split() fertility   : {corrected:.6f}")
print(f"Absolute change                : {absolute_change:.6f}")
print(f"Relative change                : {relative_change:.3f}%")
