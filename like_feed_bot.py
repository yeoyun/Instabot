from instagrapi import Client
import json, random, os, sys, time
from utils import human_delay, log_action, setup_logger

# ---------------- 기본 설정 ----------------
with open("config/settings.json", "r", encoding="utf-8") as f:
    config = json.load(f)

USERNAME = config["username"]
PASSWORD = config["password"]
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"

logfile = setup_logger("test" if TEST_MODE else "routine")
sys.stdout = logfile

print("\n========== ❤️ LIKE BOT START ==========")
print(f"Mode: {'TEST' if TEST_MODE else 'NORMAL'}")
sys.stdout.flush()

cl = Client()
try:
    cl.load_settings("config/session.json")
    cl.login(USERNAME, PASSWORD)
    log_action("✅ Login success", USERNAME)
except Exception as e:
    log_action("❌ Login failed", e)
    sys.exit(1)

# ✅ get_timeline_feed() → dict 반환
try:
    feed_data = cl.get_timeline_feed()
    feed_items = feed_data.get("feed_items", [])
    print(f"📸 Feed items fetched: {len(feed_items)}")
except Exception as e:
    log_action("❌ Feed load error", e)
    feed_items = []

sys.stdout.flush()
liked_count = 0

for item in feed_items[:3 if TEST_MODE else 10]:
    try:
        media = item.get("media_or_ad", {})  # ✅ 실제 미디어 정보
        username = getattr(media.get("user"), "username", None) if isinstance(media, dict) else media.user.username
        if not username:
            continue

        if TEST_MODE:
            log_action("🧪 TEST: would like", username)
            sys.stdout.flush()
            time.sleep(random.uniform(1, 2))
        else:
            cl.media_like(media["pk"] if isinstance(media, dict) else media.pk)
            liked_count += 1
            log_action("❤️ Liked", username)
            human_delay(5, 10)
    except Exception as e:
        log_action("❌ Error", e)
        continue

print(f"\n✅ Finished: {liked_count} posts liked.")
print("========== ❤️ LIKE BOT DONE ==========\n")
sys.stdout.flush()
logfile.close()
