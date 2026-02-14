import schedule, time, subprocess
from datetime import datetime

LOG_FILE = "pipeline.log"

def run_pipeline():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log:
        log.write(f"\n[{timestamp}] Starting pipeline...\n")
        try:
            subprocess.run(["python", "run_pipeline.py"], check=True, stdout=log, stderr=log)
            log.write(f"[{timestamp}] Pipeline finished successfully.\n")
        except subprocess.CalledProcessError as e:
            log.write(f"[{timestamp}] ERROR: {e}\n")
    print(f"[{timestamp}] Pipeline run complete. See {LOG_FILE}")

# Run hourly (adjustable)
schedule.every().hour.at(":00").do(run_pipeline)

print("Scheduler started. Pipeline will run hourly (new articles only).")

while True:
    schedule.run_pending()
    time.sleep(60)
