from filler import fill_redacted_text
import json
import os

with open("redact.txt", "r") as file:
    redacted_text = file.read()

filled_text = fill_redacted_text(redacted_text)

if not os.path.exists("./outputs/manual_output.json"):
    data = [filled_text]
else:
    with open("./outputs/manual_output.json", "r") as file:
        data = json.load(file)
        data.append(filled_text)

with open("./outputs/manual_output.json", "w") as file:
    json.dump(data, file)
