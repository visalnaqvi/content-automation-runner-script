import pandas as pd
import requests
import time
from datetime import datetime

# Load the Excel file
file_path = "/home/visalnaqvi/content-automation-runner-script/blogs.xlsx"  # Ensure this file exists
df = pd.read_excel(file_path)

# Read domains from file
with open("domains.txt", "r") as file:
    domains = [line.strip() for line in file.readlines() if line.strip()]

# Define valid months
valid_months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# Get today's date in the same format as 'publish_date' column
today_date = datetime.today().strftime("%Y-%m-%d")  # Modify based on date format in Excel

# Filter rows where publish_date is today
filtered_rows = df[df['publish_date'] == today_date]

# Function to validate blog request
def validate_blog_request(payload):
    errors = []

    if not payload.get("topic"):
        errors.append("Missing required field: topic")
    elif len(payload["topic"]) > 50:
        errors.append("Topic must be less than 50 characters")

    if not payload.get("slug"):
        errors.append("Missing required field: slug")
    elif len(payload["slug"]) > 50:
        errors.append("Slug must be less than 50 characters")
    elif not payload["slug"].replace("-", "").isalnum():
        errors.append("Slug can only contain letters, numbers, and hyphens")

    if not payload.get("category"):
        errors.append("Missing required field: category")

    if not payload.get("year"):
        errors.append("Missing required field: year")
    elif not str(payload["year"]).isdigit() or len(str(payload["year"])) != 4:
        errors.append("Year must be a 4-digit number")

    if not payload.get("keyword"):
        errors.append("Missing required field: keyword")

    if not payload.get("wordLength"):
        errors.append("Missing required field: wordLength")
    elif not isinstance(payload["wordLength"], int):
        errors.append("Word length must be a number")

    if not payload.get("audience"):
        errors.append("Missing required field: audience")

    if not payload.get("numberOfSubheading"):
        errors.append("Missing required field: numberOfSubheading")
    elif not isinstance(payload["numberOfSubheading"], int):
        errors.append("Number of subheadings must be a number")

    if not payload.get("contentPara"):
        errors.append("Missing required field: contentPara")
    elif not isinstance(payload["contentPara"], int):
        errors.append("ContentPara must be a number")

    if not payload.get("contentWords"):
        errors.append("Missing required field: contentWords")

    if not payload.get("month"):
        errors.append("Missing required field: month")
    elif payload["month"] not in valid_months:
        errors.append("Invalid month. Valid values are: " + ", ".join(valid_months))

    if not payload.get("description"):
        errors.append("Missing required field: description")

    if not payload.get("image"):
        errors.append("Missing required field: image")

    return errors


# Iterate over filtered rows
for _, row in filtered_rows.iterrows():
    # Construct the request body
    payload = {
        "topic": row["topic"],
        "slug": row["slug"],
        "category": row["category"],
        "month": row["month"],
        "year": row["year"],
        "keyword": row["keyword"],
        "wordLength": row["wordLength"],
        "audience": row["audience"],
        "numberOfSubheading": row["numberOfSubheading"],
        "contentPara": row["contentPara"],
        "contentWords": row["contentWords"],
        "note": row["note"],
        "description": row["description"],
        "image": row["image"]
    }

    headers = {"Content-Type": "application/json"}

    # Validate the request before sending
    validation_errors = validate_blog_request(payload)
    if validation_errors:
        print(f"Validation Failed for blog '{payload['topic']}':")
        for error in validation_errors:
            print(f"- {error}")
        print("Skipping this request...\n")
        continue  # Skip this blog post and move to the next

    print(f"✅ Payload validated successfully: {payload}")

    # Loop through each domain and send the POST request with a 5-minute delay
    for domain in domains:
        endpoint = f"{domain}generate-blog"
        try:
            response = requests.post(endpoint, json=payload, headers=headers)
            print(f"Request sent to {endpoint}, Status: {response.status_code}, Response: {response.text}")
            print(f"************Success in adding blog to {endpoint}*****************")

            # Wait for 5 minutes (300 seconds) before sending the next request
            print("Waiting for 3 minutes before the next request...")
            time.sleep(180)

        except Exception as e:
            print(f"Error sending request to {endpoint}: {str(e)}")
            print(f"_____________________Failed in adding blog to {endpoint}________________________\n")
