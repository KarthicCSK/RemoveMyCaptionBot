# Remove My Caption Bot - Forward files to admin + resend without caption
import telebot
import time

API_TOKEN = "7996377375:AAEsqOIBz5_dZgLhwvX9BgeI5Bke6-SPsA4"
ADMIN_ID = 683202471    # Updated Admin ID

bot = telebot.TeleBot(API_TOKEN, parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message,
        "👋 வணக்கம்!\nஎனக்கு Photo / Video / Document அனுப்புங்கள்.\n"
        "நான் caption-ஐ remove செய்து clean copy உங்களுக்கு அனுப்புவேன்.\n\n"
        "Send Any Files"
    )


@bot.message_handler(content_types=['photo', 'video', 'document', 'audio', 'voice'])
def handle_media(message):
    chat_id = message.chat.id

    # Forward to ADMIN
    try:
        bot.forward_message(ADMIN_ID, chat_id, message.message_id)
    except Exception as e:
        print("❌ Forward failed:", e)

    # Resend clean file
    try:
        if message.photo:
            file_id = message.photo[-1].file_id
            bot.send_photo(chat_id, file_id)

        elif message.video:
            file_id = message.video.file_id
            bot.send_video(chat_id, file_id)

        elif message.document:
            file_id = message.document.file_id
            bot.send_document(chat_id, file_id)

        elif message.audio:
            file_id = message.audio.file_id
            bot.send_audio(chat_id, file_id)

        elif message.voice:
            file_id = message.voice.file_id
            bot.send_voice(chat_id, file_id)

    except Exception as e:
        print("❌ Resend failed:", e)
        bot.send_message(chat_id, "Error: " + str(e))


print("✅ Bot Running on Railway...")
bot.infinity_polling(skip_pending=True)
