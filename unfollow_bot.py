from instagrapi import Client
import json, os, sys, random, time
from utils import log_action, setup_logger

# ---------------- 기본 설정 ----------------
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"
logfile = setup_logger("test" if TEST_MODE else "routine")
sys.stdout = logfile

print("\n========== 🚫 UNFOLLOW BOT START ==========")
print(f"Mode: {'TEST' if TEST_MODE else 'NORMAL'}")
sys.stdout.flush()

# 로그인 정보 로드
with open("config/settings.json", "r", encoding="utf-8") as f:
    config = json.load(f)
USERNAME = config["username"]
PASSWORD = config["password"]

cl = Client()
try:
    cl.load_settings("config/session.json")
    cl.login(USERNAME, PASSWORD)
    log_action("✅ Login success", USERNAME)
except Exception as e:
    log_action("❌ Login failed", e)
    sys.exit(1)

# ---------------- TEST용 실행 ----------------
to_unfollow = ["testuser1", "testuser2", "testuser3"] if TEST_MODE else []

for username in to_unfollow:
    if TEST_MODE:
        log_action("🧪 TEST: would unfollow", username)
        sys.stdout.flush()
        time.sleep(random.uniform(1, 2))
    else:
        try:
            user = cl.user_info_by_username(username)
            cl.user_unfollow(user.pk)
            log_action("🚫 Unfollowed", username)
        except Exception as e:
            log_action("❌ Error", f"{username} - {e}")
        sys.stdout.flush()

print("✅ Finished unfollow test.")
print("========== 🚫 UNFOLLOW BOT DONE ==========\n")
sys.stdout.flush()
logfile.close()
