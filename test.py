import re


def to_mark(text):
    text = re.sub(
            r"\*{2}\{?([^*\}]*)\}?\*{2}",
            r"<b>\1</b>",
            text
            )

    return text

print(to_mark("Eu estou testando"))
print(to_mark("Eu estou **testando**"))
print(to_mark("Eu estou **{testando}**"))

