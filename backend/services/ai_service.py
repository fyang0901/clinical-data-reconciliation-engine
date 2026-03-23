#OpenAI call and prompt functions
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

CACHE = {}


def get_ai_response(prompt: str) -> str:
    if prompt in CACHE:
        return CACHE[prompt]

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    text = response.output_text
    CACHE[prompt] = text
    return text