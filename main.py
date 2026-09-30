import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("No se ha encontrado la variable BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=["photo"])
def recibir_foto(message):
    file_id = message.photo[-1].file_id

    bot.reply_to(
        message,
        f"🆔 <code>{file_id}</code>",
        parse_mode="HTML"
    )


@bot.message_handler(content_types=["sticker"])
def recibir_sticker(message):
    file_id = message.sticker.file_id

    bot.reply_to(
        message,
        f"🆔 <code>{file_id}</code>",
        parse_mode="HTML"
    )


print("🤖 Bot iniciado correctamente.")
bot.infinity_polling(skip_pending=True)
