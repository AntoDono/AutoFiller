from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def fill_redacted_text(redacted_text):
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        messages=[
            {
                "role": "system",
                "content": "**Task: Filling Redacted Medical Documents**\n\nYou will receive a redacted medical document where sensitive information is replaced with \"___\". Your task is to fill in the redacted areas with plausible personal identification information. The filled-in information should be a single word or a phrase connected with hyphens (e.g., \"John-Smith\").\n\n**Requirements:**\n\n1. Maintain the original document's format, including line breaks or the lack thereof.\n2. Return the filled-in text and the original redacted text in the following JSON format:\n```json\n{\n  \"filled\": \"...\",\n  \"redacted\": \"...\"\n}\n```\n**Example:**\n\nIf the input is: \"Patient Name: ___ ___\"\nYour output should be ONLY JSON:\n```json\n{\n  \"filled\": \"Patient Name: John-Smith\",\n  \"redacted\": \"Patient Name: ___ ___\"\n}\n```"
            },
            {
                "role": "user",
                "content": redacted_text
            }
        ],
        temperature=1,
        stream=False,
        stop=None,
    )

    text = completion.choices[0].message.content
    text = text.replace("```json", "").replace("```", "")
    return json.loads(text)

def main():
    redacted_text = "Patient Name: ___ ___"
    filled_text = fill_redacted_text(redacted_text)
    print(filled_text)

if __name__ == "__main__":
    main()
