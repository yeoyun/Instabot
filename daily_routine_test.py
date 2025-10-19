import subprocess, sys, os, random, time
from utils import setup_logger

logfile = setup_logger("test")
sys.stdout = logfile

ROUTINE = [
    ("unfollow_bot.py", "🚫 Unfollow test..."),
    ("follow_bot.py", "🤝 Follow test..."),
    ("like_feed_bot.py", "❤️ Like test...")
]

def random_wait(min_sec=2, max_sec=5):
    sec = random.randint(min_sec, max_sec)
    print(f"⏳ Waiting {sec} seconds before next action...")
    sys.stdout.flush()
    time.sleep(sec)

def run_routine():
    print("🧪 Starting Instagram TEST Routine...\n")
    sys.stdout.flush()

    os.environ["TEST_MODE"] = "true"  # ✅ 전체 테스트 모드 활성화

    for script, message in ROUTINE:
        print(message)
        sys.stdout.flush()
        try:
            result = subprocess.run(
                [sys.executable, script],
                check=True,
                text=True,
                capture_output=True
            )
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"❌ {script} failed with error:\n{e.stderr}")
        sys.stdout.flush()
        random_wait(2, 5)

    print("\n✅ TEST completed.")
    sys.stdout.flush()
    logfile.close()

if __name__ == "__main__":
    delay = random.randint(0, 10)
    print(f"🕐 Starting test after {delay} seconds...")
    sys.stdout.flush()
    time.sleep(delay)
    run_routine()
