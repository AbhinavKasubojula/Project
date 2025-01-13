import requests
import json
import csv
from datetime import datetime, timedelta
import config

# Access APIs
API = config.API_KEYS["sam_api"]
URL = config.URL["sam_url"]
ncode1 = config.DATABASE["ncode1"]
ncode2 = config.DATABASE["ncode2"]
# Get today's date
today_date = datetime.today()

# Format today's date as MM/DD/YYYY
today_text = today_date.strftime("%m/%d/%Y")

# Get yesterday's date
yesterday_date = today_date - timedelta(days=1)

# Format yesterday's date as MM/DD/YYYY
yesterday_text = yesterday_date.strftime("%m/%d/%Y")

api_url = f"{URL}&api_key={API}&postedFrom={yesterday_text}&postedTo={today_text}&ncode={ncode1}"
print(api_url)
# Define the API URL
#api_url = "https://api.sam.gov/opportunities/v2/search?limit=10&api_key=rbMq9Ts3Lw123csLQ2sLRuQmNxY5sunID7nM2vwi&postedFrom=01/05/2025&postedTo=07/12/2025&ncode=332613"


def get_Json(api_url):
    # Send the GET request
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Assuming the response is in JSON format
        data = response.json()
        
        # Print the JSON response or process the data as needed
        print(data)
        json_file_path = r"C:\Users\AbhinavKasubojula\OneDrive - Kenall Inc\Desktop\code\downloaded_data\response_data.json"
        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        print(f"JSON data saved to {json_file_path}")
        return data
        
    else:
        print(f"Error: {response.status_code}, {response.text}")

def get_csvFromJson(data):
    # Extract the 'opportunitiesData' field
    opportunities_data = data.get('opportunitiesData', [])

    # Dynamically extract the headers (all unique keys)
    headers = set()
    for record in opportunities_data:
        headers.update(record.keys())

    # Convert headers to a list and sort if desired
    headers = list(headers)

    # Prepare the data for CSV
    csv_data = []
    for record in opportunities_data:
        row = {key: record.get(key, '') for key in headers}
        csv_data.append(row)

    # Write the data to a CSV file with dynamic headers
    csv_file_path =r"C:\Users\AbhinavKasubojula\OneDrive - Kenall Inc\Desktop\code\downloaded_data\dynamic_headers_data.csv"
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers, delimiter=',')
        writer.writeheader()  # Write the headers
        writer.writerows(csv_data)  # Write the data rows

    print(f"CSV file with dynamic headers has been saved as {csv_file_path}")


data = get_Json(api_url)

get_csvFromJson(data)
