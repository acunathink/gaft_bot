import logging
import os
import random

import g4f
# from time import sleep
from telegram import Message
from telegram.chat import Chat
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
from telegram.update import Update
from dotenv import load_dotenv


# Включить логирование
# logging.basicConfig(level=logging.INFO)
def set_logger():
    """Установка параметров логгирования."""
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] '
        '%(message)s -- %(filename)s:%(lineno)s'
    )
    # handler = logging.StreamHandler(stream=stdout)
    handler = logging.FileHandler('log_gpt.txt', 'a')
    handler.setFormatter(formatter)

    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
RETRY_PERIOD = 60  # in seconds
SOME_WAIT = [
    'Ща как отвечу...',
    'Погодь...',
    'Минуточку...'
]
MODELS_TRY = [
    g4f.models.default,
    g4f.models.gpt_35_long,
    g4f.models.gpt_35_turbo,
    g4f.models.gpt_4,
    g4f.models.llama2_70b,
]
LIMIT = '. Ответь коротко, будто сообщением мессенджере'
SOME_BUSY = [
    'сорян, что-то я туплю...',
    'бутте даабры ппамедление, я записсую...',
    'оставь меня, старушка, я в печали...',
    'напомни потом тебе на это ответить, сейчас мне некогда.'
]
HTML = "<!DOCTYPE html>"

# Словарь для хранения истории разговоров
conversation_history = {}


def start_say(update, context):
    update.message.reply_text("Чего удумали?")


def ask_gpt(chat_history):
    # print(f'GPT4: "{random.choice(SOME_WAIT)}"')
    try_count = len(MODELS_TRY)
    response = None
    while response is None and try_count > 0:
        model_choise = random.choice(MODELS_TRY)
        logger.info(f'{model_choise.name}: "{random.choice(SOME_WAIT)}"')
        try:
            response = g4f.ChatCompletion.create(
                model=model_choise,
                messages=chat_history,
                stream=False
            )
        except Exception as reason:
            logger.error(f'Сбой в работе модели {model_choise.name}: {reason}')
            response = None
        try_count -= 1
    if response[:len(HTML)] == HTML:
        logger.warning(f'{model_choise.name}: {model_choise}')
    logger.info(f'{model_choise.name}: "{response}"')
    return response


# Функция для обрезки истории разговора
def trim_history(history, max_length=4096):
    current_length = sum(len(message["content"]) for message in history)
    while len(history) > 1 and current_length > max_length:
        removed_message = history.pop(0)
        current_length -= len(removed_message["content"])
    return history


def get_answer(message: Message, name):
    msg = message.text[0].upper() + message.text[1:] + LIMIT
    user_id = message.from_user.id
    if user_id not in conversation_history:
        conversation_history[user_id] = []
        conversation_history[user_id].append(
            {"role": "user", "content": f'Меня называют {name}.'}
        )
    # print(f'{name}: "{msg}"')
    # with open('log_gpt.txt', 'w') as fl:
    #     print(f'{name}: "{msg}"', file=fl)
    conversation_history[user_id].append({"role": "user", "content": msg})
    conversation_history[user_id] = trim_history(conversation_history[user_id])
    chat_history: list[dict[str: str]] = conversation_history[user_id]
    logger.info(f'{name}: "{msg}"')
    res = ask_gpt(chat_history)
    last = chat_history.pop()
    last["content"] = last["content"][:(0 - len(LIMIT))]
    chat_history.append(last)
    # print(f'{conversation_history[user_id]}', end='\n - - - \n')
    return res


def say_back(update: Update, context):
    # print(f' reply.message: {update.message}')
    reply = update.message.reply_to_message
    chat = update.message.chat
    name = update.message.from_user.first_name
    # print(f"reply.from_user.username = {name}")
    if reply.from_user.username == 'acunasfirsttry_bot':
        answer = get_answer(update.message, name)
        if answer:
            context.bot.send_message(chat_id=chat.id, text=answer)
        else:
            answer = random.choice(SOME_BUSY)
            context.bot.send_message(chat_id=chat.id, text=answer)
        conversation_history[update.message.from_user.id].append(
            {"role": "assistant", "content": answer}
        )
    else:
        # ответ на ответ своему сообщению прописать
        print('GPT4: А мне плевать, кто там что думает...')


def say_hi(update: Update, context):
    # Получаем информацию о чате, из которого пришло сообщение
    # print(f'update: {update}')
    # print(f'context: {context}')
    # print(f'update.message: {update.message}')
    chat: Chat = update.message.chat
    # print(f"chat.first_name = {chat.first_name}")
    if chat.type == 'private':
        answer = get_answer(update.message, chat.first_name)
        if not answer:
            answer = random.choice(SOME_BUSY)
        try:
            context.bot.send_message(chat_id=chat.id, text=answer)
            conversation_history[update.message.from_user.id].append(
                {"role": "assistant", "content": answer}
            )
        except Exception as reason:
            error = f'Ошибка при отправке сообщения: {reason}'
            logger.error(error)
    else:
        print("--> redirect to sayback -->")
        say_back(update, context)


def tg_bot():
    updater = Updater(token=TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start_say))
    dispatcher.add_handler(CommandHandler("gpt", start_say))
    dispatcher.add_handler(MessageHandler(Filters.reply, say_back))
    dispatcher.add_handler(MessageHandler(Filters.text, say_hi))

    # Метод start_polling() запускает процесс polling,
    updater.start_polling(poll_interval=11.5)
    # Бот будет работать до тех пор, пока не нажмете Ctrl-C
    updater.idle()


def main():
    """Основная логика работы бота."""
    if not TELEGRAM_TOKEN:
        logger.critical('Не найден TELEGRAM_TOKEN в файле .env')
        exit('Провеьте наличие файла .env')
    try:
        tg_bot()
    except Exception as reason:
        error = f'Сбой в работе программы: {reason}'
        logger.error(error)


logger = set_logger()
if __name__ == '__main__':
    main()
