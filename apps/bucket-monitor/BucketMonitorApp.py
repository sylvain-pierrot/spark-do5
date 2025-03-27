import os
import time
import boto3
from pyspark.sql import SparkSession
from datetime import datetime
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore", category=InsecureRequestWarning)

endpoint_url = os.environ["S3_ENDPOINT"]
access_key = os.environ["S3_ACCESS_KEY"]
secret_key = os.environ["S3_SECRET_KEY"]
bucket_name = os.environ["S3_BUCKET"]
prefix = os.environ.get("S3_PREFIX", "") 
interval = int(os.environ.get("MONITOR_INTERVAL", "1")) 

spark = SparkSession.builder.appName("BucketMonitorApp").getOrCreate()

s3 = boto3.client(
    "s3",
    endpoint_url=endpoint_url,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    verify=False
)

def list_files():
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    return sorted([obj["Key"] for obj in response.get("Contents", [])])

print(f"[{datetime.now()}] 📦 Monitoring bucket '{bucket_name}' (prefix: '{prefix}') every {interval}s...\n")

previous_files = list_files()
no_change_reported = False

try:
    while True:
        time.sleep(interval)
        current_files = list_files()

        added = sorted(set(current_files) - set(previous_files))
        removed = sorted(set(previous_files) - set(current_files))

        if added or removed:
            print(f"[{datetime.now()}] 🔄 Change detected in bucket '{bucket_name}'")
            if added:
                print(f"  ➕ Added files ({len(added)}):")
                for f in added:
                    print(f"     - {f}")
            if removed:
                print(f"  ➖ Removed files ({len(removed)}):")
                for f in removed:
                    print(f"     - {f}")
            no_change_reported = False
        else:
            if not no_change_reported:
                print(f"[{datetime.now()}] ✅ No changes detected.")
                no_change_reported = True

        previous_files = current_files

except KeyboardInterrupt:
    print(f"\n[{datetime.now()}] 🛑 Monitoring stopped by user.")

spark.stop()