from pathlib import Path
import unicodedata


CORPUS_DIR = Path(__file__).parent / "corpus"

FILES = {
    "eng": "eng.txt",
    "hin": "hin.txt",
    "tam": "tam.txt",
    "tel": "tel.txt",
}


for language, filename in FILES.items():

    path = CORPUS_DIR / filename

    with open(path, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    non_empty = [line for line in lines if line.strip()]
    duplicates = len(non_empty) - len(set(non_empty))

    total_chars = sum(len(line) for line in non_empty)
    total_words = sum(len(line.split()) for line in non_empty)

    invalid_unicode = 0

    for line in non_empty:
        for char in line:
            if unicodedata.category(char) == "Cs":
                invalid_unicode += 1

    print(f"\nLanguage: {language}")
    print(f"  Lines:              {len(lines)}")
    print(f"  Non-empty lines:    {len(non_empty)}")
    print(f"  Duplicate lines:    {duplicates}")
    print(f"  Characters:         {total_chars}")
    print(f"  Whitespace words:   {total_words}")
    print(f"  Invalid Unicode:    {invalid_unicode}")
    