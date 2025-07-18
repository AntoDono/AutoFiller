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
                    "You will receive a redacted medical document where sensitive information is replaced with \"___\". Your task is to fill in the redacted areas with plausible personal identification information and return the result in a structured format with PII mappings.",
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
                    "1. Maintain the original document's format, including line breaks or the lack thereof.",
                    "2. Make it diverse and realistic. Use names from different ethnicities and cultures (e.g., Asian, Hispanic, Middle Eastern, African, European), varying ages, genders, and backgrounds.",
                    "3. Replace each filled-in piece of information with a placeholder like <<PII_1>>, <<PII_2>>, etc.",
                    "4. Return the result in the following JSON format:",
                    "```json",
                    "{",
                    "  \"mapping_text\": \"...\",",
                    "  \"pii_mappings\": {",
                    "    \"<<PII_1>>\": {",
                    "      \"type\": \"NAME\",",
                    "      \"value\": \"John Smith\"",
                    "    },",
                    "    \"<<PII_2>>\": {",
                    "      \"type\": \"DATE\",",
                    "      \"value\": \"01/15/1980\"",
                    "    }",
                    "  }",
                    "}",
                    "```",
                    "",
                    "**Example:**",
                    "",
                    "If the input is: \"Patient Name: ___\"",
                    "Your output should be ONLY JSON:",
                    "```json",
                    "{",
                    "  \"mapping_text\": \"Patient Name: <<PII_1>>\",",
                    "  \"pii_mappings\": {",
                    "    \"<<PII_1>>\": {",
                    "      \"type\": \"NAME\",",
                    "      \"value\": \"Hubert Wolfeschlegelstein\"",
                    "    }",
                    "  }",
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
    text = text.split("</think>")[-1]
    text = text.replace("```json", "").replace("```", "")
    try:
        parsed_json = json.loads(text)
    except:
        print(text)
    return parsed_json

def evaluate_redacted(redacted_json):
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "\n".join([
                    "You are an expert evaluator for PII (Personally Identifiable Information) generation quality.",
                    "",
                    "Your task is to evaluate whether generated PII data is realistic, consistent, and properly formatted.",
                    "",
                    "INPUT FORMAT:",
                    "You will receive a JSON object with:",
                    "- mapping_text: Text with PII placeholder tokens like <<PII_1>>, <<PII_2>>, etc.",
                    "- pii_mappings: Dictionary mapping each token to its type and generated value",
                    "",
                    "EVALUATION CRITERIA:",
                    "1. COMPLETENESS: Are all the \"___\" placeholders in the original text replaced with PII tokens?",
                    "2. MAPPING CONSISTENCY: Does each PII token in mapping_text have a corresponding entry in pii_mappings?",
                    "",
                    "OUTPUT FORMAT:",
                    "Respond with ONLY valid JSON in this exact format:",
                    "```json",
                    "{",
                    "  \"passed\": true/false,",
                    "  \"reasoning\": \"Brief 2-3 sentence explanation of your evaluation, including specific issues found or confirmation that all criteria are met\"",
                    "}",
                    "```",
                    "",
                    "Do not include any text outside the JSON block."
                ])
            },
            {
                "role": "user",
                "content": redacted_json
            }
        ]
    )
    
    text = completion.choices[0].message.content
    text = text.split("</think>")[-1]
    text = text.replace("```json", "").replace("```", "")
    
    try:
        parsed_json = json.loads(text)
        return parsed_json
    except:
        print(text)
        return {}

def main():
    redacted_text = "Patient Name: ___ ___"
    filled_text = fill_redacted_text(redacted_text)
    print(filled_text)

if __name__ == "__main__":
    main()
