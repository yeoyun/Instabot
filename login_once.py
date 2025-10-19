from instagrapi import Client
import json
import os

CONFIG_PATH = "config/settings.json"
SESSION_PATH = "config/session.json"

# 📁 config 폴더 없으면 생성
os.makedirs("config", exist_ok=True)

# 📖 로그인 정보 불러오기
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

USERNAME = config["username"]
PASSWORD = config["password"]

cl = Client()

try:
    print("🔐 Instagram 로그인 시도 중...")
    cl.login(USERNAME, PASSWORD)
    cl.dump_settings(SESSION_PATH)
    print(f"✅ 로그인 성공! 세션이 저장되었습니다: {SESSION_PATH}")

except Exception as e:
    # challenge_required (2FA 또는 보안코드 요청)
    if "challenge_required" in str(e):
        print("⚠️ 보안 인증이 필요합니다. 인증 코드를 입력해주세요.")
        try:
            cl.get_timeline_feed()  # 세션 초기화용
            challenge = cl.challenge_resolve(e)
            print(f"➡️ 인증 경로: {challenge}")

            # 이메일 혹은 문자로 전송된 코드 입력받기
            code = input("📩 전송된 6자리 인증 코드를 입력하세요: ").strip()

            result = cl.challenge_code(code)
            if result:
                print("✅ 인증 성공! 세션을 저장합니다...")
                cl.dump_settings(SESSION_PATH)
            else:
                print("❌ 인증 실패. 코드를 다시 확인해주세요.")
        except Exception as err:
            print(f"❌ 인증 중 오류 발생: {err}")
    else:
        print(f"❌ 로그인 실패: {e}")
