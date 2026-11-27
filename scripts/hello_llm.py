import time

import ollama

MODEL = "qwen2.5:3b"


def ask(question: str) -> str:
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": question}],
    )
    return response["message"]["content"]


if __name__ == "__main__":
    start = time.time()
    answer = ask("In two sentences, what is a 10-K filing?")
    delay = time.time() - start
    print(answer)
    print(f"\n[answered in {delay:.1f} seconds]")
