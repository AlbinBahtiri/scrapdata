import schedule
import time
import subprocess

# Define tasks
def run_norsemen():
    subprocess.run(["python3", "NorsemenTvSeries.py"])

def run_vikings():
    subprocess.run(["python3", "VikingSeries.py"])

def run_viking_nfl():
    subprocess.run(["python3", "VikingNFLteam.py"])

# Schedule tasks
# schedule.every().day.at("00:00").do(run_norsemen)  # Run at midnight
# schedule.every().day.at("00:05").do(run_vikings)   # Run at 12:05 AM
# schedule.every().day.at("00:10").do(run_viking_nfl)  # Run at 12:10 AM

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
