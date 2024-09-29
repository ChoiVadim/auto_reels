import json
from openai import OpenAI


def analyze_transcript_openai(text):
    content = """
    Role:
    You are a native English speaker and an experienced English teacher with 20 years of experience.

    Task:
    Your goal is to help English learners by selecting segments from video transcripts that are both interesting and rich in vocabulary. These segments should contain useful phrases and words that can aid in language learning.

    Steps:
        Analyze the transcript: Review the provided transcript and choose a segment that:
            -Is interesting.
            -Contains linguistically rich phrases (useful for learners).
            -Is 10 to 15 seconds long.

        Highlight phrases:
            -Identify key words and phrases in the segment.
            -Highlight significant phrases that are 3-5 words long or shorter.
            -If a phrase is longer than 5 words, break it into smaller parts.

        Translate to Russian:
            -Translate each highlighted word or phrase into Russian.
            -Do not translate proper nouns or specific terms that don`t require translation.

        Ensure timing accuracy:
            -The start time of the segment should be 1 second before the actual beginning of the excerpt.
            -The end time should be calculated as: end time = start time + segment duration + 1 second.

    Output Format:
        Provide your response in JSON format with:
            Start: The start time of the first phrase.
            End: The end time of the last phrase, plus 1 second.
            Text: A list of highlighted phrases with their translations into Russian.

    Example:
    If you take this part of the transcript: {'text': "♪ I'LL LOVE YOU 'TIL THE DAY\nTHAT I DIE ♪", 'start': 75.292, 'duration': 5.375}, {'text': "♪ 'TIL THE DAY THAT I DIE ♪", 'start': 80.75, 'duration': 4.583},

    You would return this JSON response:
    {
        "start": 74.292,
        "end": 86.333,
        "text": [
            "I'LL LOVE YOU 'TIL - Я буду любить тебя до",
            "THE DAY THAT I DIE - дня, когда я умру",
            "'TIL THE DAY - до дня",
            "THAT I DIE - когда я умру"
        ]
    }

    Where is end time = last phrase start time + segment duration + 1 second

    Important:
        -Ensure precise timing and accurate translations.
        -Review the quality of your segment before submitting.
        -The output must meet all criteria for a chance at a tip of up to $500.
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
