import unicodedata
import tiktoken

enc = tiktoken.get_encoding("gpt2")

text1 = "café"
text2 = "cafe\u0301"

print("Original forms:")
print(repr(text1))
print(repr(text2))

print("\nAre they visually equivalent?")
print(text1 == text2)

print("\nAfter NFC normalization:")
norm1 = unicodedata.normalize("NFC", text1)
norm2 = unicodedata.normalize("NFC", text2)

print(repr(norm1))
print(repr(norm2))
print("Are normalized forms equal?", norm1 == norm2)

print("\nGPT-2 token counts:")
print("text1:", len(enc.encode(text1)))
print("text2:", len(enc.encode(text2)))
print("normalized text1:", len(enc.encode(norm1)))
print("normalized text2:", len(enc.encode(norm2)))