from google.oauth2.service_account import Credentials
import gspread
import json

# Define Google Sheets API scope
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Authenticate with Google Sheets API
creds = Credentials.from_service_account_file("xxxxxxxxx.json", scopes=SCOPES)
client = gspread.authorize(creds)

# Open the sheet
sheet = client.open("HASHPREP_DSA_SHEET").sheet1
data = sheet.get_all_values()

# Extract headers
headers = data[0]

# Convert to structured format
structured_data = [dict(zip(headers, row)) for row in data[1:]]

# Convert fields to match web scraping format
formatted_problems = []

for row in structured_data:
    formatted_problems.append({
        "Problem Name": row["title"],
        "Topic": row["topic"],
        "Difficulty": row["difficulty"],
        "Platform": row["platform"],
        "Link": row["link"],
        "Tags": row["tags"].split(", ") if row["tags"] else [],  # Convert to list, handle empty values
        "Companies": row["company_tags"].split(", ") if row["company_tags"] else [],
        "Solved Status": int(row["solved_status"]) if row["solved_status"].isdigit() else 0,  # Default to 0 if empty
        "Needs Revision": bool(int(row["needs_revision"])) if row["needs_revision"].isdigit() else False,  # Default to False if empty
        "Notes": row["notes"]
    })

# Print formatted data
for problem in formatted_problems:  # Print only the first 10 for testing
    print(json.dumps(problem, indent=4))

# Define the output file name
output_file = "gsheet_data.txt"

# Save the formatted data to a text file
with open(output_file, "w", encoding="utf-8") as file:
    for problem in formatted_problems:
        file.write(json.dumps(problem, indent=4) + "\n\n")

print(f"✅ Data saved to {output_file}")