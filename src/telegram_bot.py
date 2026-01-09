import requests
import threading

class TelegramBot:
    def __init__(self, token=None, chat_id=None):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send_message(self, message):
        if not self.token or not self.chat_id:
            print("[INFO] Telegram token or chat_id not set.")
            return

        def _send():
            try:
                payload = {
                    'chat_id': self.chat_id,
                    'text': message
                }
                requests.post(self.base_url, data=payload)
            except Exception as e:
                print(f"[ERROR] Failed to send Telegram message: {e}")

        # Send in a separate thread to avoid blocking the main video loop
        threading.Thread(target=_send).start()
