import os
from datetime import datetime

def backup_database():
    backup_dir = "D:/backupsZoo"
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = os.path.join(backup_dir, f"backup_{timestamp}.sql")
    os.system(f"pg_dump -U postgres -h 127.0.0.1 ZooShopHelper > {backup_file}")