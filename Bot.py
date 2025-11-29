# ------------------------------------------------------------
# Remove My Caption Bot - Forward to admin + resend without caption
# Updated & Optimized Version
# ------------------------------------------------------------

import telebot
import time
import logging

API_TOKEN = "7996377375:AAEsqOIBz5_dZgLhwvX9BgeI5Bke6-SPsA4"   # Your bot token
ADMIN_ID = 212865124   # Your Telegram User ID

bot = telebot.TeleBot(API_TOKEN)

# Enable logging (debugging purpose)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


# ------------------------------------------------------------
# Start Command
# ------------------------------------------------------------
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message,
                 "👋 வணக்கம் CSK!\n"
                 "எனக்கு Photo / Video / Document / Audio அனுப்புங்கள்.\n"
                 "நான் caption-ஐ remove செய்து clean copy உங்களுக்கு தருவேன்.\n\n"
                 "📩 Send Any Files.")


# ------------------------------------------------------------
# Media Handler
# ------------------------------------------------------------
@bot.message_handler(content_types=[
    'photo', 'video', 'document', 'audio', 'voice', 'animation'
])
def handle_media(message):
    user_chat = message.chat.id

    # ------------------------------
    # 1) Forward original file to admin
    # ------------------------------
    try:
        bot.forward_message(ADMIN_ID, user_chat, message.message_id)
        logging.info(f"Forwarded file from {user_chat} to admin.")
    except Exception as e:
        logging.error(f"Forward failed: {e}")

    # ------------------------------
    # 2) Resend clean file (remove caption)
    # ------------------------------
    try:
        content = message

        if content.photo:
            file_id = content.photo[-1].file_id
            bot.send_photo(user_chat, file_id)

        elif content.video:
            file_id = content.video.file_id
            bot.send_video(user_chat, file_id)

        elif content.document:
            file_id = content.document.file_id
            bot.send_document(user_chat, file_id)

        elif content.audio:
            file_id = content.audio.file_id
            bot.send_audio(user_chat, file_id)

        elif content.voice:
            file_id = content.voice.file_id
            bot.send_voice(user_chat, file_id)

        elif content.animation:      # GIF support
            file_id = content.animation.file_id
            bot.send_animation(user_chat, file_id)

        else:
            bot.send_message(user_chat, "❌ Unsupported file type.")

        logging.info(f"Clean file sent to user {user_chat}")

    except Exception as e:
        logging.error(f"Resend failed: {e}")
        bot.send_message(user_chat, "⚠️ Error while sending clean file.")


# ------------------------------------------------------------
# Bot Runner (Auto Restart Safe)
# ------------------------------------------------------------
print("✅ RemoveMyCaptionBot is Running...")

while True:
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        logging.error(f"Bot crashed: {e}")
        time.sleep(3)
