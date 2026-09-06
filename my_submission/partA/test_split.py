test_strings = [
    "one two three",
    "one  two three",
    "one   two   three",
    "one\ttwo three",
]

for text in test_strings:
    print("\nText:", repr(text))

    print("split(' '):", text.split(" "))
    print("count:", len(text.split(" ")))

    print("split():  ", text.split())
    print("count:", len(text.split()))