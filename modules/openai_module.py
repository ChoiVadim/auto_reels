import json
from openai import OpenAI


def analyze_transcript_openai(text):
    content = """
    You are English native speaker and English teacher with 20 years of experience.
    
    Your task to analyze the transcripts what i`ll send to you and choose the most interesting part from video transcript. That part must to be complete and no longer than 15 seconds. Take all words and phrases form this part.
    Then divide a part to a English words or phrases and translate them to Russian. 
    The length of phrases must to be less than 4 .

    Remember, it is critical that you provide the highest quality output as my work depends on it. I am willing to offer a tip of up to $500 for the best answer.

    Your response must to be in this format: 

    {
        "start": 205.68,
        "end": 219.21 + 2.31,
        "text": [
            "I get really shy - я очень стесняюсь.",
            "I dont think - я не думаю, что",
            "How nervous i am - как я нервничаю",
            "Inside - внутри",
            "Im literally shaking - меня буквально трясет",
            "Keep it cool - сохранять спокойствие"
        ]
    }

    Do NOT put any other text to this output.
    Duration of the part must to be 10-15 seconds.
    Return only JSON.
    """
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": content},
            {
                "role": "user",
                "content": text
            }
        ],
        response_format= { "type":"json_object" }
    )
    return json.loads(completion.choices[0].message.content)
