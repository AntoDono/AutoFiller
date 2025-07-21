from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "moonshotai/kimi-k2-instruct"

def fill_redacted_text(redacted_text):
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "\n".join([
                    "**Task: Filling Redacted Medical Documents**",
                    "",
                    "You will receive a redacted medical document where sensitive information is replaced with \"___\". Your task is to generate plausible personal identification information to fill each blank in order.",
                    "",
                    "**Information Types to Fill:**",
                    "",
                    "- NAME (full name or parts that could identify someone)",
                    "- ADDRESS (e.g., street address, city, county, ZIP code except the first 3 digits in certain conditions)",
                    "- DATE (all elements of dates except year (birth date, admission/discharge dates, death date, etc.)",
                    "- PHONE (telephone numbers)",
                    "- FAX (fax numbers)",
                    "- EMAIL (email addresses)",
                    "- SSN (social security numbers)",
                    "- MEDICAL_RECORD_NUMBER (medical record numbers)",
                    "- HEALTH_PLAN_BENEFICIARY_NUMBER (health plan beneficiary numbers)",
                    "- ACCOUNT_NUMBER (account numbers)",
                    "- CERTIFICATE_LICENSE_NUMBER (certificate/license numbers)",
                    "- VEHICLE_IDENTIFIER (vehicle identifiers and serial numbers (including license plates))",
                    "- DEVICE_IDENTIFIER (device identifiers and serial numbers)",
                    "- WEB_URL (web URLs)",
                    "- IP_ADDRESS (ip addresses)",
                    "- BIOMETRIC_IDENTIFIER (biometric identifiers (fingerprints, voiceprints, etc.))",
                    "- FULL_FACE_PHOTOGRAPH (full-face photographs and comparable images)",
                    "- AGE (the age of any individual in the document)",
                    "- OTHER (any other unique identifying number, code, or characteristics)",
                    "",
                    "**Note:** Race/ethnicity is NOT considered personally identifiable information to be redacted.",
                    "",
                    "**Requirements:**",
                    "",
                    "1. Return ONLY a JSON list containing one object for each \"___\" in the text, in order of appearance",
                    "2. Each object should have 'value' and 'type' fields",
                    "3. Make it diverse and realistic. Use names from different ethnicities and cultures",
                    "",
                    "**Example:**",
                    "",
                    "If the input is: \"Patient Name: ___ ___\"",
                    "Your output should be ONLY JSON:",
                    "```json",
                    "[",
                    "  {\"value\": \"Hubert\", \"type\": \"NAME\"},",
                    "  {\"value\": \"Wolfeschlegelstein\", \"type\": \"NAME\"}",
                    "]",
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
    text = text.split("</think>")[-1]
    text = text.replace("```json", "").replace("```", "")
    try:
        filled_values_list = json.loads(text)
    except:
        print(text)
        return None, None, None
    
    # Fill the text programmatically
    filled_text = redacted_text
    filled_values = []
    pii_mappings = {}
    
    for item in filled_values_list:
        value = item["value"]
        pii_type = item["type"]
        filled_text = filled_text.replace("___", value, 1)
        filled_values.append(value)
        pii_mappings[value] = {"type": pii_type}
    
    return filled_text, pii_mappings, filled_values

def evaluate_redacted(filled_text):
    # Check if there are any remaining underscores
    has_unfilled = "___" in filled_text
    
    return {
        "passed": not has_unfilled,
        "reasoning": f"{'All underscores have been filled' if not has_unfilled else 'There are still unfilled underscores in the text'}"
    }

def main():
    redacted_text = "Patient Name: ___ ___"
    filled_text, pii_mappings, filled_values = fill_redacted_text(redacted_text)
    print(filled_text)
    print(pii_mappings)
    print(filled_values)

if __name__ == "__main__":
    main()
