import json
from openai import OpenAI


def analyze_transcript_openai(text):
    content = """
    You are English native speaker and English teacher with 20 years of experience.
    
    Your task to analyze the transcripts what i`ll send to you and choose the most 
    interesting and fool of words or phrases for study English part from video transcript.
    That part must to be complete and no longer than 15 seconds.

    Take this transcript and return some interesting words or phrases and translate them to Russian.
    Example:
        "I get really shy - я очень стесняюсь."
        "I dont think - я не думаю, что"
        "How nervous i am - как я нервничаю"
        "Inside - внутри"
        "Im literally shaking - меня буквально трясет"
        "Keep it cool - сохранять спокойствие"
        
    Do not translate word like names of people or places or any other names.
    Do not make it too long and too short.
    
    Duration of the video must to be not less than 4 seconds and not more than 15 seconds!

    Remember, it is critical that you provide the highest quality output as my work depends on it.
    I am willing to offer a tip of up to $500 for the best answer.

    Check a time when when video starts and ends correctly. Its really important!
    For example, if you took these part as a first part {'text': "text example", 'start': 1.8, 'duration': 5.89} 
    than start must to be less than 1.8 and if you took this part as a last part {'text': "text example", 'start': 205.68, 'duration': 2.31}
    than end must to be 205.68+2.31+1=207.99.
    
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

    Return only JSON.
    """
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": content},
            {"role": "user", "content": text},
        ],
        response_format={"type": "json_object"},
    )

    return json.loads(completion.choices[0].message.content)
