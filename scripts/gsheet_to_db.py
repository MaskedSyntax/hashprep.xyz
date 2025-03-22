import sys
import os

# Get the absolute path of the current script's directory
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Get the absolute path to the backend directory
backend_path = os.path.abspath(os.path.join(current_script_dir, "../backend"))

# Add the backend directory explicitly to sys.path
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app import create_app
from extensions import db
from models import Problem, Tag, CompanyTag
from google.oauth2.service_account import Credentials
import gspread

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Create Flask app context to access database
app = create_app()
app.app_context().push()

# Authenticate with Google Sheets API
creds = Credentials.from_service_account_file("hashprep-dev.json", scopes=SCOPES)
client = gspread.authorize(creds)

# Open the sheet
sheet = client.open("HASHPREP_DSA_SHEET").sheet1
data = sheet.get_all_values()

# Extract headers
headers = data[0]

# Process each row
for row in data[1:]:
    row_data = dict(zip(headers, row))

    # Check if Problem already exists (avoid duplicates)
    problem = Problem.query.filter_by(link=row_data["link"]).first()

    if not problem:
        problem = Problem(
            title=row_data["title"],
            topic=row_data["topic"],
            difficulty=row_data["difficulty"],
            platform=row_data["platform"],
            link=row_data["link"],
        )
        db.session.add(problem)
        db.session.flush()  # get ID immediately if it's new

    # Process tags without duplicates
    tags = row_data["tags"].split(", ") if row_data["tags"] else []
    for tag_name in tags:
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.session.add(tag)
            db.session.flush()

        # Check before adding to avoid duplicates
        if tag not in problem.tags:
            problem.tags.append(tag)

    # Process company tags without duplicates
    companies = row_data["company_tags"].split(", ") if row_data["company_tags"] else []
    for company_name in companies:
        company = CompanyTag.query.filter_by(name=company_name).first()
        if not company:
            company = CompanyTag(name=company_name)
            db.session.add(company)
            db.session.flush()

        # Check before adding to avoid duplicates
        if company not in problem.company_tags:
            problem.company_tags.append(company)

# Commit everything at once
db.session.commit()
print("Data successfully inserted into the database.")
