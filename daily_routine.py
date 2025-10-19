import os, random, time, sys
from utils import setup_logger, log_action

logfile = setup_logger("routine")
sys.stdout = logfile

ROUTINE = [
    ("unfollow_bot.py", "🚫 UNFOLLOW STAGE"),
    ("follow_bot.py", "🤝 FOLLOW STAGE"),
    ("like_feed_bot.py", "❤️ LIKE STAGE")
]

def random_wait(min_sec=300, max_sec=900):
    sec = random.randint(min_sec, max_sec)
    print(f"⏳ Waiting {sec//60} min before next stage...")
    time.sleep(sec)

def run_routine():
    print("\n========== 🌅 DAILY ROUTINE START ==========")
    for script, name in ROUTINE:
        log_action("▶ START", name)
        os.system(f"python {script}")
        log_action("✅ DONE", name)
        random_wait(300, 900)
    print("========== 🌙 DAILY ROUTINE END ==========\n")
    logfile.close()

if __name__ == "__main__":
    delay = random.randint(0, 7200)
    print(f"🕐 Starting routine after {delay//60} minutes...")
    time.sleep(delay)
    run_routine()
