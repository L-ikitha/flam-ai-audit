import tiktoken

enc = tiktoken.get_encoding("gpt2")

words = [
    "नमस्ते",
    "भारत",
    "किताब",
    "पानी",
    "मुझे",
    "hello",
    "India",
    "book",
    "water",
]

for word in words:
    tokens = enc.encode(word)

    print("Text:", word)
    print("Token IDs:", tokens)
    print("Number of tokens:", len(tokens))
    print()