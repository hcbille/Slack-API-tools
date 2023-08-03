import csv
import json
import time
import requests

# Load config options from a JSON file
with open('config.json', 'r') as f:
    config = json.load(f)

# Load user/channel data from a CSV file
with open('users_channels.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader) # skip header row
    row_num = 2 # start at row 2
    for row in reader:
        user_idV = row[0]
        channel_idV = row[1]
        retries = 0
        
        while retries < config['MAX_RETRIES']:
            # Construct request payload
            payload = {
                'user_ids': user_idV,
                'channel_id': channel_idV
            }
            
            # Construct request headers
            headers = {
                'Authorization': 'Bearer ' + config['SLACK_TOKEN'],
                'Content-Type': 'application/json'
            }
            
            # Send request
            response = requests.post('https://slack.com/api/admin.conversations.invite', headers=headers, json=payload)
            
            # Check response code
            if response.status_code == 200:
                # Success, print response code and row number, and move on to next row
                print(f"Row {row_num}: {response.status_code}")
                break
            else:
                # Failure, print response code and row number, and retry after delay
                print(f"Row {row_num}: {response.status_code} (retrying)")
                retries += 1
                time.sleep(config['RETRY_INTERVAL'])
        
        if retries == config['MAX_RETRIES']:
            # Max retries reached, print error message and quit
            print(f"Row {row_num}: Max retries exceeded, quitting...")
            break
        
        row_num += 1
        time.sleep(config['REQUEST_INTERVAL'])
