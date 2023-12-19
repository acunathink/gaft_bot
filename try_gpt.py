import random
import sys
import g4f
# from g4f.Provider import (
#     AItianhu,
#     Aichat,
#     Bard,
#     Bing,
#     ChatBase,
#     ChatgptAi,
#     OpenaiChat,
#     Vercel,
#     You,
#     Yqcloud,
# )
import os
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
from dotenv import load_dotenv
# from telegram import MessageEntity

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
# print(f'TELEGRAM_TOKEN={TELEGRAM_TOKEN}')
SOME_WAIT = [
    'Ща как отвечу...',
    'Погодь...',
    'Минуточку...'
]

def print_to_log(message):
    with open('log_gpt.txt', 'a') as fl:
        print(message, file=fl)


def get_answer(message, name):
    iam = f'Меня называют {name}.'
    msg = message.text
    msg = msg[0].upper() + msg[1:]
    print_to_log(f'{name}: "{msg}"')

    limit = ('Ответь коротко, будто сообщением мессенджере')

    return ask_gpt(f'{iam} {msg}. {limit}', 'bot')


def say_back(update, context):
    reply = update.message.reply_to_message
    chat = update.message.chat
    name = update.message.from_user.first_name
    print_to_log(f' reply.message: {update.message}')
    print_to_log(f"reply.from_user.username = {name}")
    if reply.from_user.username == 'acunasfirsttry_bot':
        answer = get_answer(update.message, name)
        context.bot.send_message(chat_id=chat.id, text=answer)
    # else:
    #     # ответ на ответ своему сообщению прописать
    #     print('GPT4: А мне плевать, кто там что думает...')


def say_hi(update, context):
    # Получаем информацию о чате, из которого пришло сообщение
    # print(f'update: {update}')
    # # print(f'context: {context}')
    # print(f'update.message: {update.message}')

    chat = update.message.chat
    if chat.type == 'private':
        answer = get_answer(update.message, chat.first_name)
        context.bot.send_message(chat_id=chat.id, text=answer)
    # else:
    #     print("--> redirect to sayback -->")
        # say_back(update, context)


# def just_read(update, context):
#     print(f' update: {update}')
#     print(f'context: {context}')


def start_say(update, context):
    update.message.reply_text("Чего удумали?")


def tg_bot():
    # В объекте Updater регистрируется обработчик MessageHandler;
    # из всех полученных сообщений он будет выбирать только текстовые сообщения
    # и передавать их в функцию say_hi()
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


def ask_gpt(msg, mode=''):
    print_to_log(f'GPT4: "{random.choice(SOME_WAIT)}"')
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_35_turbo,
        messages=[{"role": "user", "content": msg}],
    )
    print_to_log(f'GPT4: "{response}"')
    if mode == 'bot':
        return response


def main():
    # name = input('GPT4: Как тебя зовут?\n')
    # if name == 'bot':
    tg_bot()
    # ask_gpt(f'Привет, меня зовут {name}!')
    # ask_gpt(sys.stdin.readline())


if __name__ == '__main__':
    main()
