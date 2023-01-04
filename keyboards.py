from telegram import KeyboardButton, ReplyKeyboardMarkup

schedule_btn = KeyboardButton("Расписание")
sign_up_for_class_btn = KeyboardButton("Записаться на пробное")
payment_btn = KeyboardButton("Оплата")
cost_btn = KeyboardButton("Стоимость")
ask_question_btn = KeyboardButton("Задать вопрос")
reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                     keyboard=[[schedule_btn], [sign_up_for_class_btn], [payment_btn, cost_btn],
                                               [ask_question_btn]])
