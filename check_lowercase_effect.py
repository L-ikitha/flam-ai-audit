import tiktoken

enc = tiktoken.get_encoding("gpt2")

text = open(
    "corpus_sample/eng_sample.txt",
    encoding="utf-8"
).read()

lines = [x.strip() for x in text.splitlines() if x.strip()]

for i, line in enumerate(lines, start=1):
    original = len(enc.encode(line))
    lower = len(enc.encode(line.lower()))

    if original != lower:
        print("Line:", i)
        print("Sentence:", line)
        print("Original tokens:", original)
        print("Lowercase tokens:", lower)
        print("Difference:", lower - original)
        print()