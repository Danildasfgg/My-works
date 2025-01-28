from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# Список для хранения наборов цифр
numbers_list = set()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне набор цифр, и я проверю его в списке.")

# Обработка текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    # Проверяем, есть ли набор цифр в списке
    if user_input in numbers_list:
        # Создаем кнопку для удаления
        keyboard = [[InlineKeyboardButton("Удалить из списка", callback_data=f"confirm_delete_{user_input}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Отправляем сообщение с кнопкой удаления
        await update.message.reply_text(
            f"Набор цифр '{user_input}' уже есть в списке. Хотите удалить?",
            reply_markup=reply_markup,
        )
    else:
        # Создаем кнопку для добавления
        keyboard = [[InlineKeyboardButton("Добавить в список", callback_data=f"add_{user_input}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Отправляем сообщение с кнопкой добавления
        await update.message.reply_text(
            f"Набора цифр '{user_input}' нет в списке. Хотите добавить?",
            reply_markup=reply_markup,
        )

# Обработка нажатия на кнопку
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Извлекаем данные из callback_data
    data = query.data.split("_")
    action = data[0]
    number = data[-1]

    if action == "add":
        # Добавляем набор цифр в список
        numbers_list.add(number)
        await query.edit_message_text(f"Набор цифр '{number}' добавлен в список!")
    elif action == "confirm" and data[1] == "delete":
        # Удаляем набор цифр из списка
        numbers_list.discard(number)
        await query.edit_message_text(f"Набор цифр '{number}' удален из списка.")
    elif action == "delete":
        # Подтверждение удаления
        keyboard = [
            [InlineKeyboardButton("Да, удалить", callback_data=f"confirm_delete_{number}")],
            [InlineKeyboardButton("Отмена", callback_data=f"cancel_delete_{number}")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"Точно хотите удалить набор цифр '{number}'?",
            reply_markup=reply_markup,
        )
    elif action == "cancel" and data[1] == "delete":
        # Отмена удаления
        await query.edit_message_text(f"Удаление набора цифр '{number}' отменено.")

# Основная функция
def main():
    # Вставь сюда свой токен
    application = ApplicationBuilder().token("7592446058:AAFPB6az755v19X3B6drlqIjAF5wuxohekM").build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_callback))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()