import os
import requests
import time

TOKEN = os.environ.get("TOKEN")
# እዚህ ላይ የእርስዎን (የአድሚኑን) የቴሌግራም ቻት መለያ ቁጥር (Admin Chat ID) ያስገቡ
ADMIN_CHAT_ID = "YOUR_ADMIN_CHAT_ID" 

BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

def get_updates(offset=None):
    url = f"{BASE_URL}/getUpdates?timeout=30"
    if offset:
        url += f"&offset={offset}"
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print(e)
        return None

def send_message(chat_id, text, reply_markup=None):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    requests.post(url, json=payload)

def forward_message(chat_id, from_chat_id, message_id):
    url = f"{BASE_URL}/forwardMessage"
    payload = {
        "chat_id": chat_id,
        "from_chat_id": from_chat_id,
        "message_id": message_id
    }
    requests.post(url, json=payload)

def main():
    print("Keber Ekub Bot with Group Forwarding is running...")
    offset = None
    while True:
        updates = get_updates(offset)
        if updates and "result" in updates:
            for update in updates["result"]:
                offset = update["update_id"] + 1
                
                # መልእክቱ ከግሩፕ ወይም ከግል ቻት ሊመጣ ስለሚችል 'message' ወይም 'channel_post' እንይ
                message = update.get("message") or update.get("channel_post")
                
                if message:
                    chat_id = message["chat"]["id"]
                    user = message.get("from", {})
                    user_name = user.get("first_name", "አባል")
                    message_id = message["message_id"]
                    text = message.get("text", "")
                    photo = message.get("photo")
                    
                    if text == "/start":
                        welcome_msg = (
                            "ሰላም! እንኳን ወደ ኬበር (Keber) ዕቁብ አስተዳደር ቦት በሰላም መጡ! 🚀\n\n"
                            "አባላት የክፍያ ደረሰኝዎን በዚህ ግሩፕ ውስጥ ፎቶ በማንሳት መላክ ይችላሉ።"
                        )
                        send_message(chat_id, welcome_msg)
                        
                    elif photo:
                        # አባሉ ግሩፕ ውስጥ ፎቶ ሲልክ (የባንክ ደረሰኝ)
                        if ADMIN_CHAT_ID != "YOUR_ADMIN_CHAT_ID":
                            # ፎቶውን ለአድሚን ፕራይቬት ቻት ያስተላልፋል
                            forward_message(ADMIN_CHAT_ID, chat_id, message_id)
                            send_message(chat_id, f"✅ከ {user_name} የተላከው የክፍያ ደረሰኝ ለአድሚን ተልኳል! ተረጋግጦ ይመዝገበታል።")
                        else:
                            send_message(chat_id, "⚠️ የአድሚን መለያ ቁጥር (Admin Chat ID) በኮዱ ውስጥ አልተካተተም።")
                            
        time.sleep(1)

if __name__ == "__main__":
    main()
