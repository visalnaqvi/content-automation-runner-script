import requests

# Define category payload
category_payload = {
        "name": "CUET UG",
        "image": "https://www.cuet.edu.in/wp-content/uploads/2023/03/CUET-Logo.png",
        "description": "The Common University Entrance Test (CUET UG) is a national-level entrance exam conducted by the National Testing Agency (NTA) for admission to undergraduate programs in central, state, deemed, and private universities across India. It provides a single-window opportunity for students to apply to multiple universities based on their CUET scores.",
        "key": "cuet-ug",
        "blogs": []
    }


headers = {"Content-Type": "application/json"}

with open("domains.txt", "r") as file:
    domains = [line.strip() for line in file.readlines() if line.strip()]

for domain in domains:
    endpoint = f"{domain}category"

    print(f"Sending request to {endpoint}...")

    try:
        response = requests.post(endpoint, json=category_payload, headers=headers)
        print(f"Response Status: {response.status_code}, Response: {response.text}")
        print(f"************Success in adding category to {endpoint}*****************")
    except Exception as e:
        print(f"Error sending request to {endpoint}: {str(e)}")
        print(f"_____________________Failed in adding category to {endpoint}________________________")

