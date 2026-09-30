import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configuración de logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    await update.message.reply_text(
        "¡Hola! Mándame cualquier foto, sticker, GIF (animación) o video en privado y te responderé con su file_id exacto."
    )

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja foto, sticker, GIF y video"""
    message = update.message
    file_id = None
    media_type = ""

    # 1. Foto (Telegram envía una lista de tamaños, tomamos la de mayor resolución)
    if message.photo:
        file_id = message.photo[-1].file_id
        media_type = "Foto"

    # 2. Sticker
    elif message.sticker:
        file_id = message.sticker.file_id
        media_type = "Sticker"

    # 3. GIF / Animación
    elif message.animation:
        file_id = message.animation.file_id
        media_type = "GIF / Animación"

    # 4. Video
    elif message.video:
        file_id = message.video.file_id
        media_type = "Video"

    # 5. Documento (a veces los videos/GIFs se mandan como archivo sin compresión)
    elif message.document:
        file_id = message.document.file_id
        media_type = f"Documento ({message.document.mime_type or 'desconocido'})"

    if file_id:
        response_text = f"📌 **Tipo:** {media_type}\n🆔 **File ID:**\n`{file_id}`"
        await message.reply_text(response_text, parse_mode="Markdown")

def main():
    # AQUÍ ESTÁ LA VARIABLE DE RAILWAY: BOT_TOKEN
    TOKEN = os.getenv("BOT_TOKEN")

    if not TOKEN:
        logger.error("Error: La variable de entorno BOT_TOKEN no está configurada en Railway.")
        return

    # Crear aplicación de Telegram
    app = Application.builder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    
    # Filtro para contenido multimedia en chat privado
    media_filter = (
        filters.PHOTO | 
        filters.STICKER | 
        filters.ANIMATION | 
        filters.VIDEO | 
        filters.Document.ALL
    ) & filters.ChatType.PRIVATE

    app.add_handler(MessageHandler(media_filter, handle_media))

    logger.info("Bot iniciado correctamente...")
    app.run_polling()

if __name__ == "__main__":
    main()
