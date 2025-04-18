import requests
import json
import time
import http.server
import socketserver
import threading
import os
from datetime import datetime, timedelta

# Configuration (loaded from add-on options)
CONFIG_FILE = "/data/options.json"
with open(CONFIG_FILE, 'r') as f:
    config = json.load(f)

CSRF_TOKEN = config["tuya_csrf_token"]
COOKIES = config["tuya_cookies"]
PROJECT_CODE = config["tuya_project_code"]
SOURCE_ID = config["tuya_source_id"]
DEVICE_ID = config["tuya_device_id"]
REGION = config["tuya_region"]
POLL_INTERVAL = config["poll_interval"]

# Tuya API endpoint
API_URL = f"https://{REGION.lower()}.platform.tuya.com/micro-app/cloud/api/v10/device/log/list"

# Headers from curl
HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/json; charset=UTF-8",
    "csrf-token": CSRF_TOKEN,
    "origin": f"https://{REGION.lower()}.platform.tuya.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": f"https://{REGION.lower()}.platform.tuya.com/cloud/device/detail/?id={PROJECT_CODE}&sourceId={SOURCE_ID}&sourceType=4&region={REGION}&deviceKey=deviceLogs&deviceId={DEVICE_ID}",
    "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}

# Store latest data
latest_data = []

def fetch_tuya_data():
    global latest_data
    # Calculate time range (last 24 hours)
    end_time = int(time.time() * 1000)
    start_time = end_time - (24 * 60 * 60 * 1000)  # 24 hours ago

    payload = {
        "startRowId": "",
        "pageNo": 1,
        "pageSize": 10,
        "code": "25",  # From curl
        "startTime": start_time,
        "endTime": end_time,
        "projectCode": PROJECT_CODE,
        "sourceId": SOURCE_ID,
        "sourceType": "4",
        "deviceId": DEVICE_ID,
        "pageStartRow": "",
        "region": REGION
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, cookies={"cookie": COOKIES}, json=payload)
        response.raise_for_status()
        data = response.json()
        if data.get("success"):
            latest_data = data["result"]["datas"]
            print(f"Fetched {len(latest_data)} records at {datetime.now()}")
        else:
            print(f"API error: {data}")
    except Exception as e:
        print(f"Error fetching data: {e}")

# Simple HTTP server to expose data
class DataHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/data":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(latest_data).encode())
        else:
            self.send_response(404)
            self.end_headers()

def start_server():
    PORT = 8000
    with socketserver.TCPServer(("", PORT), DataHandler) as httpd:
        print(f"Serving data at port {PORT}")
        httpd.serve_forever()

# Polling loop
def poll_data():
    while True:
        fetch_tuya_data()
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    # Start HTTP server in a separate thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Start polling
    poll_data()