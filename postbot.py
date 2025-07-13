import logging
from telegram import Update, InputMediaPhoto, InputMediaVideo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

user_media = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_media[user_id] = []
    await update.message.reply_text(
        "Отправляйте фото и видео. Когда закончите, введите /stop чтобы получить всё одним сообщением."
    )


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    media_list = user_media.get(user_id, [])

    if not media_list:
        await update.message.reply_text("Вы не отправили ни одного фото или видео.")
        return

    try:

        photos = [m for m in media_list if m.media_type == 'photo']
        videos = [m for m in media_list if m.media_type == 'video']

        if photos:
            media_group = [InputMediaPhoto(media=photo.file_id) for photo in photos]
            await context.bot.send_media_group(chat_id=update.effective_chat.id, media=media_group)

        if videos:
            media_group = [InputMediaVideo(media=video.file_id) for video in videos]
            await context.bot.send_media_group(chat_id=update.effective_chat.id, media=media_group)

        await update.message.reply_text("Вот все ваши медиафайлы!")
    except Exception as e:
        logger.error(f"Ошибка при отправке медиа: {e}")
        await update.message.reply_text("Произошла ошибка при отправке ваших медиафайлов.")
    finally:

        if user_id in user_media:
            del user_media[user_id]


async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id

    if user_id not in user_media:
        return

    if update.message.photo:

        photo = update.message.photo[-1]
        user_media[user_id].append(MediaItem(photo.file_id, 'photo'))
    elif update.message.video:
        video = update.message.video
        user_media[user_id].append(MediaItem(video.file_id, 'video'))


class MediaItem:
    def __init__(self, file_id, media_type):
        self.file_id = file_id
        self.media_type = media_type


def main() -> None:
    application = Application.builder().token("8161638520:AAFtwe14VEEAX0MaaKJLgWr2olVVnZPZiMY").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))

    application.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, handle_media))

    application.run_polling()


if __name__ == '__main__':
    main()
