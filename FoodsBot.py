# encoding: utf-8
"""
FoodsBot

Created by Donzok on 28/07/2017.
Copyright (c) 2017 . All rights reserved.
"""
from telegram.contrib import Botan

import tools.logger as logger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram.ext import CommandHandler
import database.transactions as transactions
import emoji
import json
import ast

NAME = range(1)
__NEW_DISH__ = None


def start(bot, update):
    global __BOTAN__
    __BOTAN__.track(update.message, event_name='start')

    update.message.reply_text("Hola! Soy el bot que necesitas para dejar de pensar en qué comidas hacer. "
                              "Para saber cómo funciono escribe /ayuda")


def help(bot, update):
    global __BOTAN__
    __BOTAN__.track(update.message, event_name='help')

    update.message.reply_text("Los comandos que puedes usar son los siguientes:\n"
                              "/nuevo_plato: Te permite añadir nuevos platos a mi "
                              "lista de platos (te recomiendo usarlo)\n"
                              "/plato: Te daré un plato al azar de cualquier categoría "
                              "(desayuno, almuerzo, merienda o cena)\n"
                              "/desayuno: Te daré un desayuno al azar\n"
                              "/almuerzo: Te daré un almuerzo al azar\n"
                              "/merienda: Te daré una merienda al azar\n"
                              "/cena: Te daré una cena al azar")


def get_dish(bot, update):
    global __BOTAN__
    __BOTAN__.track(update.message, event_name='dish')

    dish = transactions.get_random_dish()

    if dish == -1:
        update.message.reply_text("Parece que no tengo ningún plato, esto es un poco embarazoso... :S "
                                  "¿Por qué no me ayudas añadiendo un plato con /nuevo_plato?")
    else:
        update.message.reply_text(dish)


def get_breakfast(bot, update):
    global __BOTAN__
    __BOTAN__.track(update.message, event_name='breakfast')

    breakfast = transactions.get_random_breakfast()

    if breakfast == -1:
        update.message.reply_text("Parece que no tengo ningún desayuno... "
                                  "¿Por qué no me ayudas añadiendo uno con /nuevo_plato?")
    else:
        update.message.reply_text(breakfast)


def get_lunch(bot, update):
    global __BOTAN__
    __BOTAN__.track(update.message, event_name='lunch')

    lunch = transactions.get_random_lunch()

    if lunch == -1:
        update.message.reply_text("Parece que no tengo ningún almuerzo... "
                                  "¿Por qué no me ayudas añadiendo uno con /nuevo_plato?")
    else:
        update.message.reply_text(lunch)


def get_snack(bot, update):
    global __BOTAN__
    __BOTAN__.track(update.message, event_name='snack')

    snack = transactions.get_random_snack()

    if snack == -1:
        update.message.reply_text("Parece que no tengo ninguna merienda... "
                                  "¿Por qué no me ayudas añadiendo una con /nuevo_plato?")
    else:
        update.message.reply_text(snack)


def get_dinner(bot, update):
    global __BOTAN__
    __BOTAN__.track(update.message, event_name='dinner')

    dinner = transactions.get_random_dinner()

    if dinner == -1:
        update.message.reply_text("Parece que no tengo ninguna cena... "
                                  "¿Por qué no me ayudas añadiendo una con /nuevo_plato?")
    else:
        update.message.reply_text(dinner)


def add_dish(bot, update):
    global __NEW_DISH__
    global __BOTAN__

    __BOTAN__.track(update.message, event_name='add_dish')

    __NEW_DISH__ = None
    update.message.reply_text("Vamos a añadir un plato. Puedes cancelar el proceso en cualquier momento "
                              "enviando /cancel.\nEn primer lugar, ¿cómo se llama el plato?")

    return NAME


def add_dish_name(bot, update):
    global __NEW_DISH__
    global __BOTAN__

    __BOTAN__.track(update.message, event_name='add_dish_name')

    __NEW_DISH__ = [update.message.text, False, False, False, False]

    inline_keyboard = [
        [InlineKeyboardButton(text="Desayuno", callback_data="[0, [0, 0, 0, 0]]")],
        [InlineKeyboardButton(text="Almuerzo", callback_data="[1, [0, 0, 0, 0]]")],
        [InlineKeyboardButton(text="Merienda", callback_data="[2, [0, 0, 0, 0]]")],
        [InlineKeyboardButton(text="Cena", callback_data="[3, [0, 0, 0, 0]]")],
        [InlineKeyboardButton(text="Confirmar", callback_data="[4, [0, 0, 0, 0]]")]
    ]

    update.message.reply_text("¿Qué tipo de plato es? (Selecciona tantos como quieras)",
                              reply_markup=InlineKeyboardMarkup(inline_keyboard=inline_keyboard))


def add_dish_callback(bot, update):
    global __NEW_DISH__
    global __BOTAN__

    __BOTAN__.track(update.message, event_name='add_dish_type')

    callback = update.callback_query
    callback.data = ast.literal_eval(callback.data)

    if callback.data[0] == 4:
        callback.answer()
        callback.edit_message_reply_markup()
        callback.message.reply_text("Muchas gracias por añadir un plato.\n{0}\nDesayuno: {1}\n"
                                    "Almuerzo: {2}\nMerienda: {3},\nCena: {4}".format(
                                                                                    __NEW_DISH__[0], __NEW_DISH__[1],
                                                                                    __NEW_DISH__[2], __NEW_DISH__[3],
                                                                                    __NEW_DISH__[4]))

        transactions.add_dish(__NEW_DISH__)
        __NEW_DISH__ = None
        return ConversationHandler.END
    else:
        inline_keyboard = [
            [InlineKeyboardButton(text="Desayuno", callback_data="[0, [0, 0, 0, 0]]")],
            [InlineKeyboardButton(text="Almuerzo", callback_data="[1, [0, 0, 0, 0]]")],
            [InlineKeyboardButton(text="Merienda", callback_data="[2, [0, 0, 0, 0]]")],
            [InlineKeyboardButton(text="Cena", callback_data="[3, [0, 0, 0, 0]]")],
            [InlineKeyboardButton(text="Confirmar", callback_data="[4, [0, 0, 0, 0]]")]
        ]

        __NEW_DISH__[callback.data[0] + 1] = not __NEW_DISH__[callback.data[0] + 1]

        callback_data = callback.data[-1]
        callback_data[callback.data[0]] = int(not callback_data[callback.data[0]])

        for i in range(len(callback_data)):
            button = inline_keyboard[i][0]
            if callback_data[i] == 1:
                button.text = button.text + emoji.emojize(" :white_check_mark:", use_aliases=True)

            button.callback_data = str([i, callback_data])

        callback.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=inline_keyboard))


def add_dish_cancel(bot, update):
    global __NEW_DISH__
    global __BOTAN__

    __BOTAN__.track(update.message, event_name='add_dish_cancel')

    __NEW_DISH__ = None

    update.message.reply_text("¡Hasta pronto!")

    return ConversationHandler.END


def error(bot, update, error):
    logger.get_logger().warning('Update "%s" caused error "%s"' % (update, error))


if __name__ == "__main__":
    global __BOTAN__

    logger.init_logger()

    transactions.init_db()

    with open('files/security.json') as security_file:
        security = json.load(security_file)

        updater = Updater(security['bot_token'])

        __BOTAN__ = Botan(token=security['botanio_token'])

    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    help_handler = CommandHandler('ayuda', help)
    dispatcher.add_handler(help_handler)

    dish_handler = CommandHandler('plato', get_dish)
    dispatcher.add_handler(dish_handler)

    breakfast_handler = CommandHandler('desayuno', get_breakfast)
    dispatcher.add_handler(breakfast_handler)

    lunch_handler = CommandHandler('almuerzo', get_lunch)
    dispatcher.add_handler(lunch_handler)

    snack_handler = CommandHandler('merienda', get_snack)
    dispatcher.add_handler(snack_handler)

    dinner_handler = CommandHandler('cena', get_dinner)
    dispatcher.add_handler(dinner_handler)

    dish_type__callback_handler = CallbackQueryHandler(add_dish_callback)
    dispatcher.add_handler(dish_type__callback_handler)

    add_dish_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('nuevo_plato', add_dish)],

        states={
            NAME: [MessageHandler(Filters.text, add_dish_name)],
        },

        fallbacks=[CommandHandler('cancel', add_dish_cancel)]
    )
    dispatcher.add_handler(add_dish_conv_handler)

    dispatcher.add_error_handler(error)

    updater.start_polling()
