import tiktoken
from transformers import AutoTokenizer

# Load tokenizers
gpt2 = tiktoken.get_encoding("gpt2")
xlmr = AutoTokenizer.from_pretrained("xlm-roberta-base")

languages = {
    "English": "corpus_sample/eng_sample.txt",
    "Hindi": "corpus_sample/hin_sample.txt",
}

for language, path in languages.items():

    lines = []

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()

            if not line:
                continue

            lines.append(line)

    print("\n" + language)
    print("-" * 40)

    for name, tokenizer in [
        ("GPT-2", gpt2),
        ("XLM-R", xlmr),
    ]:

        total_tokens = 0
        total_words = 0
        total_chars = 0

        for line in lines:

            tokens = tokenizer.encode(line, add_special_tokens=False) \
                if name == "XLM-R" else tokenizer.encode(line)

            total_tokens += len(tokens)
            total_words += len(line.split())
            total_chars += len(line)

        tokens_per_word = total_tokens / total_words
        tokens_per_char = total_tokens / total_chars

        print(name)
        print("  Tokens:", total_tokens)
        print("  Words:", total_words)
        print("  Characters:", total_chars)
        print("  Tokens/word:", round(tokens_per_word, 3))
        print("  Tokens/character:", round(tokens_per_char, 3))