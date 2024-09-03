from langchain_community.llms import Ollama
from modules.utils import analyze_transcript


output_example = """{
    "start": 205.68,
    "end": 219.21 + 2.31,
    "text": [
        "I get really shy - я очень стесняюсь.",
        "Speak English - говорить на Английском.",
        "I dont think - я не думаю, что",
        "People realize - люди осознают",
        "How nervous i am - как я нервничаю",
        "Inside - внутри",
        "I`m literally shaking - меня буквально трясет",
        "Keep it cool - сохранять спокойствие"
    ]
}"""


input_example = analyze_transcript("UHXCSeoU-YM&t")

prompt = (
    "Im learning english analyze this transcript and return some  interesting for learning words or phrases with translations: "
    + "\n".join(str(i) for i in input_example)
    + "\n"
    + "Your response must to be in this format: "
    + "\n"
    + output_example
    + "\n"
)

with open("test.txt", "w") as f:
    f.write(prompt)

llm = Ollama(model="llama3.1")
response = llm.invoke(prompt)

print(response)
