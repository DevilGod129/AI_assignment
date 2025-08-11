import os
import csv
import json
import re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from essay_text import essay  

# Load API key
load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)

# Helper: extract JSON string if wrapped in ```json ... ```
def extract_json_string(text):
    match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

# Prompt for the whole essay at once
prompt = f"""
Extract structured company information from the following text in JSON format.
Return a JSON array where each element is an object with keys:
- company_name (string)
- founding_date (YYYY-MM-DD, fill missing day/month with 01)
- founders (list of strings)
In certain scenarios, the complete date information may not be available. To handle such cases:
If only the year is provided, default the date to January 1st of that year.
If the year and month are provided, default the date to the 1st day of the specified month.

If no company info is found, return an empty array [].

Text:
{essay}
"""

# One single API call
response = llm.invoke(prompt)
raw_content = response.content

# Clean up JSON from possible markdown formatting
json_str = extract_json_string(raw_content)

try:
    company_list = json.loads(json_str)
except json.JSONDecodeError:
    print("Failed to parse JSON output:")
    print(raw_content)
    company_list = []

# Prepare CSV rows
rows = []
for i, item in enumerate(company_list, start=1):
    if all(k in item for k in ("company_name", "founding_date", "founders")):
        rows.append([
            i,
            item["company_name"],
            item["founding_date"],
            str(item["founders"])
        ])

# Save CSV
with open("company_info.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["S.N.", "Company Name", "Founded in", "Founded by"])
    writer.writerows(rows)

print("✅ company_info.csv created successfully!")
