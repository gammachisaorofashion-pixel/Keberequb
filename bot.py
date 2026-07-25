import os
import requests
import time

TOKEN = os.environ.get("TOKEN")
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

def main():
    print("Keber Ekub Bot is running...")
    offset = None
    while True:
        updates = get_updates(offset)
        if updates and "result" in updates:
            for update in updates["result"]:
                offset = update["update_id"] + 1
                if "message" in update:
                    chat_id = update["message"]["chat"]["id"]
                    text = update["message"].get("text", "")
                    photo = update["message"].get("photo")
                    
                    if text == "/start":
                        welcome_msg = (
                            "ሰላም! እንኳን ወደ ኬበር (Keber) ዕቁብ አስተዳደር ቦት በሰላም መጡ! 🚀\n\n"
                            "ይህ ቦት የ 11 አባላትን የዕቁብ አስተዋጽኦ እና ክፍያዎች በሥርዓት ለመከታተል ይጠቅማል።\n\n"
                            "የሚከተሉትን ትዕዛዞች መጠቀም ይችላሉ፦\n"
                            "/pay - ክፍያ ለመመዝገብ (የባንክ ደረሰኝ ፎቶ ወይም ጽሁፍ መላክ)\n"
                            "/status - የዕቁቡን አጠቃላይ ሁኔታ ለማየት"
                        )
                        send_message(chat_id, welcome_msg)
                        
                    elif text == "/pay":
                        send_message(chat_id, "እባክዎ የባንክ የክፍያ ደረሰኝዎን (Screenshot) ወይም የትራንዛክሽን ቁጥር ይላኩ።")
                        
                    elif text == "/status":
                        status_msg = (
                            "📊 **የኬበር ዕቁብ ሁኔታ**\n\n"
                            "• አጠቃላይ አባላት: 11\n"
                            "• የድርጅት ሁኔታ: በስራ ላይ ይገኛል\n"
                            "• ወቅታዊ ዑደት: 1ኛ ወር"
                        )
                        send_message(chat_id, status_msg)
                        
                    elif photo:
                        # አባሉ የክፍያ ፎቶ ሲልክ የሚሰጥ ምላሽ
                        send_message(chat_id, "✅ የክፍያ ደረሰኝዎ ፎቶ ደርሶናል! አስተዳዳሪው እስኪረጋገጥ ድረስ ተመዝግቧል። እናመሰግናለን!")
                        
                    elif text:
                        # ሌሎች የተለመዱ መልእክቶች ሲመጡ
                        send_message(chat_id, f"መልእክትዎ ደርሶኛል: {text}\nለተጨማሪ መረጃ /start ይጠቀሙ።")
                        
        time.sleep(1)

if __name__ == "__main__":
    main()
