import os
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, MenuButtonCommands, MenuButton, \
    MenuButtonDefault

from keyboards import reply_keyboard
from settings import *


def start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Это приветственное сообщение",
        reply_markup=reply_keyboard
    )
    context.bot.set_chat_menu_button(chat_id=update.message.chat_id, menu_button=MenuButtonDefault())


GET_QUESTION = 1


def ask_question(update, context):
    update.message.reply_text(ASK_QUESTION_MESSAGE, reply_markup=ReplyKeyboardRemove())

    user_info = update.message.from_user.to_dict()

    context.bot.send_message(
        chat_id=TELEGRAM_SUPPORT_CHAT_ID,
        text=f"""
    📞 Connected {user_info}.
            """,
    )
    return GET_QUESTION


def forward_to_chat(update, context):
    """{
        'message_id': 5,
        'date': 1605106546,
        'chat': {'id': 49820636, 'type': 'private', 'username': 'danokhlopkov', 'first_name': 'Daniil', 'last_name': 'Okhlopkov'},
        'text': 'TEST QOO', 'entities': [], 'caption_entities': [], 'photo': [], 'new_chat_members': [], 'new_chat_photo': [], 'delete_chat_photo': False, 'group_chat_created': False, 'supergroup_chat_created': False, 'channel_chat_created': False,
        'from': {'id': 49820636, 'first_name': 'Daniil', 'is_bot': False, 'last_name': 'Okhlopkov', 'username': 'danokhlopkov', 'language_code': 'en'}
    }"""
    forwarded = update.message.forward(chat_id=TELEGRAM_SUPPORT_CHAT_ID)
    if not forwarded.forward_from:
        context.bot.send_message(
            chat_id=TELEGRAM_SUPPORT_CHAT_ID,
            reply_to_message_id=forwarded.message_id,
            text=f'{update.message.from_user.id}\n{REPLY_TO_THIS_MESSAGE}'
        )
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Ваш вопрос отправлен! В скором времени вы получите ответ.",
                             reply_markup=reply_keyboard)
    return ConversationHandler.END


def forward_to_user(update, context):
    """{
        'message_id': 10, 'date': 1605106662,
        'chat': {'id': -484179205, 'type': 'group', 'title': '☎️ SUPPORT CHAT', 'all_members_are_administrators': True},
        'reply_to_message': {
            'message_id': 9, 'date': 1605106659,
            'chat': {'id': -484179205, 'type': 'group', 'title': '☎️ SUPPORT CHAT', 'all_members_are_administrators': True},
            'forward_from': {'id': 49820636, 'first_name': 'Daniil', 'is_bot': False, 'last_name': 'Okhlopkov', 'danokhlopkov': 'okhlopkov', 'language_code': 'en'},
            'forward_date': 1605106658,
            'text': 'g', 'entities': [], 'caption_entities': [], 'photo': [], 'new_chat_members': [], 'new_chat_photo': [],
            'delete_chat_photo': False, 'group_chat_created': False, 'supergroup_chat_created': False, 'channel_chat_created': False,
            'from': {'id': 1440913096, 'first_name': 'SUPPORT', 'is_bot': True, 'username': 'lolkek'}
        },
        'text': 'ggg', 'entities': [], 'caption_entities': [], 'photo': [], 'new_chat_members': [], 'new_chat_photo': [], 'delete_chat_photo': False,
        'group_chat_created': False, 'supergroup_chat_created': False, 'channel_chat_created': False,
        'from': {'id': 49820636, 'first_name': 'Daniil', 'is_bot': False, 'last_name': 'Okhlopkov', 'username': 'danokhlopkov', 'language_code': 'en'}
    }"""
    user_id = None
    if update.message.reply_to_message.forward_from:
        user_id = update.message.reply_to_message.forward_from.id
    elif REPLY_TO_THIS_MESSAGE in update.message.reply_to_message.text:
        try:
            user_id = int(update.message.reply_to_message.text.split('\n')[0])
        except ValueError:
            user_id = None
    if user_id:
        # context.bot.copy_message(
        #     message_id=update.message.message_id,
        #     chat_id=user_id,
        #     from_chat_id=update.message.chat_id
        # )
        context.bot.send_message(chat_id=user_id, text=f"#ответ\n{update.message.text}")
    else:
        context.bot.send_message(
            chat_id=TELEGRAM_SUPPORT_CHAT_ID,
            text=WRONG_REPLY
        )


def cancel_asking_question(update, _):
    update.message.reply_text("Вы больше не задаете вопрос", reply_markup=reply_keyboard)
    return ConversationHandler.END


def schedule(update, context):
    context.bot.send_photo(chat_id=update.message.chat_id, photo=open("schedule.jpg", "rb"), caption="""🗓 Расписание занятий:
(время казанское)
⠀
Начальный уровень:
👩🏻‍💼Замира - четверг в 19:00;
👩🏻‍💼Римма  - воскресенье в 13:00;
⠀
Средний уровень:
👩🏻‍💼Римма - воскресенье в 20:00;

SkyTat.Балалар 
👩🏻‍💼 Алсу апа:
1) чәкчәкләр төркеме - вторник в 19:00
2) VIP-татарлар төркеме - четверг в 19:00
⠀
🙋🏻‍♂️ Записаться ➡️ @g_ajnetdinova
""")


def setup_dispatcher(dp):
    dp.add_handler(CommandHandler('start', start))
    ask_question_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex("Задать вопрос"), ask_question)],
        states={
            GET_QUESTION: [CommandHandler('cancel', cancel_asking_question),
                           MessageHandler(Filters.chat_type.private & ~Filters.regex(r'/cancel'), forward_to_chat)]},
        fallbacks=[CommandHandler('cancel', cancel_asking_question)])
    dp.add_handler(ask_question_handler)
    # dp.add_handler(MessageHandler(Filters.chat_type.private, commands))
    # dispatcher.add_handler(MessageHandler(Filters.chat_type.private, forward_to_chat))
    dp.add_handler(MessageHandler(Filters.chat(TELEGRAM_SUPPORT_CHAT_ID) & Filters.reply, forward_to_user))
    dp.add_handler(MessageHandler(Filters.regex("Расписание"), callback=schedule))
