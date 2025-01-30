import requests
import json
import csv
from datetime import datetime, timedelta
import config
import os
import time

def task():
    print("Download in progress...")
    API = config.API_KEYS["sam_api"] 

    URL = config.URL["sam_url"] 

    ncode = config.DATABASE["ncode1"] 

    today_date = datetime.today()

    today_text = today_date.strftime("%m/%d/%Y")

    yesterday_date = today_date - timedelta(days=1)

    yesterday_text = yesterday_date.strftime("%m/%d/%Y")
    yesterday = yesterday_date.strftime("%m-%d-%Y")
    save_folder = "downloaded_data"
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)  # Create the folder if it doesn't exist

    # Generate the file name with the correct format
    file_name = f"{yesterday}_{ncode}.JSON"
    file_path = os.path.join(save_folder, file_name)

    api_url = f"{URL}&api_key={API}&postedFrom={yesterday_text}&postedTo={today_text}&ncode={ncode}"
    #api_url = "https://api.sam.gov/prod/opportunities/v2/search?deptname=general&limit=100&api_key=vuJ9yFCVSsdyCOji0UoYBWvNOI2ZKJB0xeoqMsjp&postedFrom=01/01/2025&postedTo=01/17/2025&ptype=a&ncode=541330"
    print(api_url)


    def get_Json(api_url):
        # Send the GET request
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Assuming the response is in JSON format
            data = response.json()
            
            # Print the JSON response or process the data as needed
            print(data)
            json_file_path = file_path
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
        csv_file_path =SaveAT
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers, delimiter=',')
            writer.writeheader()  # Write the headers
            writer.writerows(csv_data)  # Write the data rows

        print(f"CSV file with dynamic headers has been saved as {csv_file_path}")


    data = get_Json(api_url)

    #get_csvFromJson(data)

while True:
    task()
    time.sleep(86400)
