from google import genai
from google.genai import types
import json
import os

client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

def generate_flashcards(lyrics):
    response_schema = {
    "type": "OBJECT",
    "properties": {
        "language": {"type": "STRING"},
        "cards": {
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
    },
    "required": ["language", "cards"]
    }
    
    prompt = f"""You are a language learning assistant helping young adults learn languages through music and street culture.
    These are lyrics from a non-English song: {lyrics}
    Pick 6-10 interesting, cool, intermediate or advanced words or phrases from the lyrics.
    Ignore common filler words, repeated sounds, or onomatopoeia (e.g., 'la la la', 'yeah') and focus on unique vocabulary, slang or cultural expressions that learners would find genuinely useful.
    Write the context in a casual, friendly tone as if explaining to a friend learning the language. Keep it brief — 1-2 sentences max.
    For each one return:
    - front: the word or phrase in the original language
    - back: the English translation
    - context: a brief explanation of the word or phrase, any cultural meaning or fun facts
    Also detect and return the language of the lyrics as a single string (e.g. "Portuguese", "French", "Spanish").
    For songs where the lyrics are predominantly in two languages (roughly 30% or more in each), return both languages as a single string (e.g. "Spanish/Catalan", "French/Lingala").
    If one language makes up less than 30% of the lyrics, return only the dominant language.
    """
    
    try:
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
    except Exception as e:
        # raise exception if fails so views.py can return the right HTTP response
        raise Exception(f"Gemini API error: {str(e)}")