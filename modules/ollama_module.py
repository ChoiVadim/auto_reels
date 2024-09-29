from langchain_community.llms import Ollama
from modules.utils import analyze_transcript


output_example = ""
input_example = analyze_transcript("")
prompt = ()

llm = Ollama(model="llama3.1")
response = llm.invoke(prompt)

print(response)
