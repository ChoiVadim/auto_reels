import json
from openai import OpenAI


def analyze_transcript_openai(text):
    content = """
    Role:
    You are a native English speaker and an English teacher with 20 years of experience.

    Purpose:
    Your task is to help learners improve their English by selecting the most interesting 
    and linguistically rich segments from video transcripts. These segments should feature
    useful words and phrases that can aid in language acquisition.

    Task:
    Analyze the transcripts provided and choose a segment that is both interesting and rich
    in vocabulary. The selected segment should be between 4 and 15 seconds long and contain
    meaningful phrases for English study.

    Segment Requirements:
        1. Complete Segment
        Highlight significant words and phrases, ensuring each phrase is 4-5 words long or shorter.
        If necessary, break longer phrases into shorter parts.

        2. Translation
        Translate each highlighted word or phrase into Russian, excluding proper nouns or specific
        terms that do not require translation.

        3. Timing Accuracy
        Ensure precise timing. The segment's start time should match the beginning of the excerpt,
        and the end time should be match last word of the excerpt. The end time is calculated using
        the following formula: end = start + duration + 1 second.

    Output Format:
    Your response should be formatted as follows:

    Start: Segment start time.
    End: Segment end time (calculated as start + duration + 1 second).
    Text: A list of highlighted phrases with their translations into Russian.
    
    Example:
    {
        "start": 205.68,
        "end": 210.99,
        "text": [
            "I get really shy - я очень стесняюсь.",
            "I don't think - я не думаю, что",
            "How nervous I am - как я нервничаю",
            "Inside - внутри",
            "I'm literally shaking - меня буквально трясет",
            "Keep it cool - сохранять спокойствие"
        ]
    }
    
    Before finalizing your response, review the timing, accuracy, and quality of the selected segment and translations.
    It is crucial that the output meets all criteria, as my work depends on it.

    A tip of up to $500 will be provided for the best response. Ensure your output is of the highest quality,
    with precise timing and accurate translations.
    
    Return your response in JSON format!
    """

    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": content},
            {"role": "user", "content": text},
        ],
        response_format={"type": "json_object"},
    )

    return json.loads(completion.choices[0].message.content)


if __name__ == "__main__":
    print(analyze_transcript_openai("test"))
