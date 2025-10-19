import random
import time
from datetime import datetime
import os

def human_delay(min_sec=90, max_sec=180):
    sec = random.uniform(min_sec, max_sec)
    print(f"⏳ Waiting {sec:.1f} seconds...")
    time.sleep(sec)

def rest_break(prob=0.3):
    if random.random() < prob:
        rest_time = random.randint(300, 600)
        print(f"💤 Taking a rest for {rest_time//60} min...")
        time.sleep(rest_time)

def log_action(action, target):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {action}: {target}")

def setup_logger(mode="routine"):
    """자동 로그 파일 생성"""
    os.makedirs("logs", exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"logs/{mode}_{date_str}.log"
    return open(filename, "a", encoding="utf-8")
