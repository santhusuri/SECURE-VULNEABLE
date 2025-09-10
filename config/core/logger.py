import os
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Absolute paths for logs
IDS_LOG_FILE = os.path.join(BASE_DIR, "logs/ids.log")
AIRS_LOG_FILE = os.path.join(BASE_DIR, "logs/airs.log")

# Ensure directory exists
os.makedirs(os.path.dirname(IDS_LOG_FILE), exist_ok=True)
os.makedirs(os.path.dirname(AIRS_LOG_FILE), exist_ok=True)

# Create files if not exist
open(IDS_LOG_FILE, 'a').close()
open(AIRS_LOG_FILE, 'a').close()

def write_ids_log(user_id, action):
    """Write to IDS log"""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(IDS_LOG_FILE, "a") as f:
        f.write(f"{timestamp} | User: {user_id} | {action}\n")

def write_airs_log(alert_type):
    """Write to AIRS log"""
    from datetime import datetime
    import random
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alert_id = random.randint(1000, 9999)
    with open(AIRS_LOG_FILE, "a") as f:
        f.write(f"{timestamp} | Alert ID: {alert_id} | Type: {alert_type}\n")
