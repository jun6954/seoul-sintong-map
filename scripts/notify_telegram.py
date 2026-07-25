#!/usr/bin/env python3
"""Send a sync result to the configured Telegram chat."""
import argparse
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("message")
    args = parser.parse_args()
    config = json.loads((ROOT / "config.json").read_text())
    token, chat_id = config.get("telegram_bot_token"), config.get("telegram_chat_id")
    if not token or not chat_id:
        print("Telegram notification skipped: telegram_chat_id is not configured")
        return 0
    body = urlencode({"chat_id": chat_id, "text": args.message}).encode()
    request = Request(f"{config.get('telegram_api_base', 'https://api.telegram.org')}/bot{token}/sendMessage", data=body)
    with urlopen(request, timeout=30) as response:
        response.read()
    print("Telegram notification sent")

if __name__ == "__main__":
    main()
