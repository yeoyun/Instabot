from instagrapi import Client
import json, random, os, csv, sys, time
from datetime import datetime
from utils import human_delay, rest_break, log_action, setup_logger

# ---------------- 기본 설정 ----------------
with open("config/settings.json", "r", encoding="utf-8") as f:
    config = json.load(f)

USERNAME = config["username"]
PASSWORD = config["password"]
HASHTAGS = config.get("hashtags", ["dailylook"])
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"

FOLLOW_PER_TAG = 3 if TEST_MODE else random.randint(10, 20)
logfile = setup_logger("test" if TEST_MODE else "routine")
sys.stdout = logfile

print("\n========== 🤝 FOLLOW BOT START ==========")
print(f"Mode: {'TEST' if TEST_MODE else 'NORMAL'}")
print(f"Target hashtags: {HASHTAGS}\n")
sys.stdout.flush()

cl = Client()
try:
    cl.load_settings("config/session.json")
    cl.login(USERNAME, PASSWORD)
    log_action("✅ Login success", USERNAME)
except Exception as e:
    log_action("❌ Login failed", e)
    sys.exit(1)

total_followed = 0

# ---------------- 해시태그 루프 ----------------
for tag in HASHTAGS:
    print(f"\n#️⃣ Searching #{tag} ...")
    sys.stdout.flush()
    try:
        # 🔹 API 불안정 시 대비 예외 처리
        try:
            medias = cl.hashtag_medias_recent(tag, amount=FOLLOW_PER_TAG * 2)
        except Exception as e:
            log_action("⚠️ hashtag_medias_recent failed", f"#{tag} - {e}")
            medias = []

        random.shuffle(medias)

        for media in medias[:FOLLOW_PER_TAG]:
            try:
                username = getattr(media.user, "username", None)
                if not username:
                    continue

                if TEST_MODE:
                    log_action("🧪 TEST: would follow", f"{username} (#{tag})")
                    sys.stdout.flush()
                    time.sleep(random.uniform(1, 2))
                else:
                    cl.user_follow(media.user.pk)
                    total_followed += 1
                    log_action("✅ Followed", f"{username} (#{tag})")

                    # 팔로우 기록 저장
                    os.makedirs("config", exist_ok=True)
                    with open("config/follow_log.csv", "a", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow([username, datetime.now().strftime("%Y-%m-%d")])

                    human_delay(60, 180)
                    rest_break(0.2)
            except Exception as e:
                log_action("⚠️ Media skipped", f"#{tag} - {e}")
                continue
    except Exception as e:
        log_action("❌ Error", f"{tag} - {e}")

print(f"\n🎯 Finished: {total_followed} users followed.")
print("========== 🤝 FOLLOW BOT DONE ==========\n")
sys.stdout.flush()
logfile.close()
