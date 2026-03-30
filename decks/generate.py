from google import genai
from google.genai import types
import json
import os

# # The client gets the API key from the environment variable `GEMINI_API_KEY`.
# client = genai.Client()

# response = client.models.generate_content(
#     model="gemini-3-flash-preview",
#     contents="Explain how AI works in a few words"
# )
# print(response.text)
client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

def generate_flashcards(lyrics):
    response_schema = {
        "type": "ARRAY",
        "items": {
            "type": "OBJECT",
            "properties": {
                "front": {"type": "STRING"},
                "back": {"type": "STRING"},
                "context": {"type": "STRING"}
            },
            "required": ["front", "back", "context"]
        }
    }
    
    prompt = f"""You are a language learning assistant helping young adults learn languages through music and street culture.
    These are lyrics from a non-English song: {lyrics}
    Pick 6-10 interesting, cool, intermediate or advanced words or phrases from the lyrics.
    Ignore common filler words, repeated sounds, or onomatopoeia (e.g., 'la la la', 'yeah') and focus on unique vocabulary, slang or cultural expressions that learners would find genuinely useful.
    Write the context in a casual, friendly tone as if explaining to a friend learning the language. Keep it brief — 1-2 sentences max.
    For each one return:
    - front: the word or phrase in the original language
    - back: the English translation
    - context: a brief explanation of the word or phrase, any cultural meaning or fun facts"""
    
    # TODO: add error handling for gemini API failures (rate limits, invalid responses)
    # and return a clean 503 or 429 response instead of a 500
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        # structured output via response_mime_type ensures consistent JSON 
        # without needing to parse or clean markdown from the response
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=response_schema
        )
    )
    
    return json.loads(response.text)