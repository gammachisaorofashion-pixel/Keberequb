import os
import requests
import time

TOKEN = os.environ.get("TOKEN")
ADMIN_CHAT_ID = "1672674682"  # የእርስዎን የአድሚን ቻት አይዲ ያስገቡ
GROUP_CHAT_ID = "7689521092"  # የቴሌግራም ግሩፕዎን አይዲ እዚህ ያስገቡ

BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

# የማስታወሻ መዝገብ (Database ምትክ)
users_db = {}
payments_db = {}

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
    print("Keber Ekub Advanced Bot is running...")
    offset = None
    while True:
        updates = requests.get(f"{BASE_URL}/getUpdates?offset={offset}&timeout=30").json()
        if updates and "result" in updates:
            for update in updates["result"]:
                offset = update["update_id"] + 1
                message = update.get("message") or update.get("channel_post")
                
                if message:
                    chat_id = message["chat"]["id"]
                    user = message.get("from", {})
                    user_id = user.get("id")
                    user_name = user.get("first_name", "አባል")
                    text = message.get("text", "")
                    photo = message.get("photo")
                    
                    # 1. /start ትዕዛዝ እና ምዝገባ
                    if text == "/start":
                        welcome_msg = (
                            "ሰላም! እንኳን ወደ ኬበር (Keber) ዕቁብ አስተዳደር ቦት በሰላም መጡ! 🚀\n\n"
                            "እባክዎ ለመመዝገብ ስልክ ቁጥርዎን በዚህ መልኩ ይላኩ (ምሳሌ: /register 0911223344)"
                        )
                        send_message(chat_id, welcome_msg)
                        
                    elif text.startswith("/register"):
                        parts = text.split(" ")
                        if len(parts) > 1:
                            phone = parts[1]
                            users_db[user_id] = {"name": user_name, "phone": phone, "registered": True}
                            send_message(chat_id, f"✅ አመሰግናለሁ {user_name}! ምዝገባዎ ተጠናቋል። አሁን ወደ ዕቁብ ግሩፕ መቀላቀል ይችላሉ።")
                        else:
                            send_message(chat_id, "⚠️ እባክዎ ስልክ ቁጥርዎን በትክክል ያስገቡ። ምሳሌ: /register 0911223344")

                    # 2. ስለ ዕቁቡ ማብራሪያ
                    elif text == "/about":
                        about_msg = (
                            "ℹ️ **ስለ ኬበር (Keber) ዕቁብ ማብራሪያ**\n\n"
                            "• አጠቃላይ አባላት ብዛት: 11\n"
                            "• የዕቁብ ክፍያ መጠን: በየቀኑ/በየጊዜው 1100 ብር\n"
                            "• ድርብ ክፍያ: አንድ ቀን አציሎ ለሁለተኛው ቀን ሲከፍል 2200 ብር ገቢ ይደረጋል።\n"
                            "• ዓላማ: የህብረት ልማት እና የገንዘብ ቁጠባ።"
                        )
                        send_message(chat_id, about_msg)

                    # 3. የክፍያ ሁኔታ (Status)
                    elif text == "/status":
                        paid_amount = payments_db.get(user_id, 0)
                        status_msg = (
                            f"📊 **የእርስዎ የክፍያ ሁኔታ**\n\n"
                            f"• ስም: {user_name}\n"
                            f"• የገባው አጠቃላይ ገንዘብ: {paid_amount} ብር\n"
                            f"• ሁኔታ: {'ክፍያፈጽሟል' if paid_amount > 0 else 'ክፍያ አልተመዘገበም'}"
                        )
                        send_message(chat_id, status_msg)

                    # 4. የክፍያ ደረሰኝ ፎቶ ሲላክ (ድርብ ክፍያን ጨምሮ)
                    elif photo:
                        if user_id in users_db:
                            # ለአድሚን ማስተላለፍ
                            if ADMIN_CHAT_ID != "YOUR_ADMIN_CHAT_ID":
                                forward_message(ADMIN_CHAT_ID, chat_id, message["message_id"])
                                send_message(chat_id, f"✅ {user_name} የላኩት የክፍያ ደረሰኝ ለአድሚን ተልኳል።")
                            else:
                                send_message(chat_id, "✅ ደረሰኝዎ ደርሶናል፣ ተረጋግጦ ይመዝገባል።")
                        else:
                            send_message(chat_id, "⚠️ እባክዎ ከመላክዎ በፊት በ /register ትዕዛዝ ይመዝገቡ።")

                    elif text == "/pay":
                        send_message(chat_id, "💳 የባንክ ደረሰኝዎን ፎቶ (Screenshot) ይላኩ። (ለምሳሌ: 1100 ወይም 2200 ብር ክፍያ ሲያደርጉ)")

        time.sleep(1)

if __name__ == "__main__":
    main()
