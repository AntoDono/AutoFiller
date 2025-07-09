from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def fill_redacted_text(redacted_text):
    completion = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[
            {
                "role": "system",
                "content": "\n".join([
                    "**Task: Filling Redacted Medical Documents**",
                    "",
                    "You will receive a redacted medical document where sensitive information is replaced with \"___\". Your task is to fill in the redacted areas with plausible personal identification information. The filled-in information can be a single word or phrase.",
                    "",
                    "**Requirements:**",
                    "",
                    "1. Maintain the original document's format, including line breaks or the lack thereof.",
                    "2. Make it diverse and realistic. Use names from different ethnicities and cultures (e.g., Asian, Hispanic, Middle Eastern, African, European), varying ages, genders, and backgrounds.",
                    "3. Return the filled-in text and the original redacted text in the following JSON format:",
                    "```json",
                    "{",
                    "  \"filled\": \"...\",",
                    "  \"redacted\": \"...\"",
                    "}",
                    "```",
                    "**Example:**",
                    "",
                    "If the input is: \"Patient Name: ___ ___\"",
                    "Your output should be ONLY JSON:",
                    "```json",
                    "{",
                    "  \"filled\": \"Patient Name: Hubert Wolfeschlegelstein\",",
                    "  \"redacted\": \"Patient Name: ___ ___\"",
                    "}",
                    "```"
                ])
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
