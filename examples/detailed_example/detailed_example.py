"""
This is a detailed example using almost every command of the API
"""

import time
# import datetime
import telebot
from telebot import types
from telegram import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardRemove
import logging
import requests
from logging import Handler, Formatter
from telegram.ext import Updater
from telegram.ext import  CallbackQueryHandler
from telegram.ext import  CommandHandler
from telegram import  ReplyKeyboardRemove
from datetime import datetime
from threading import Timer

import telegramcalendar
import calendar


TOKEN = '628970389:AAEcf7VJtq-RpYnSR02sbd6REmDY1e0Unuc'

knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

commands = {  # command description used in the "help" command
    'start'       : 'Get used to the bot',
    'help'        : 'Gives you information about the available commands',
    'sendLongText': 'A test using the \'send_chat_action\' command',
    'getImage'    : 'A test using multi-stage messages, custom keyboard, and media sending'
}

imageSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # create the image selection keyboard
imageSelect.add('cock', 'pussy')

hideBoard = types.ReplyKeyboardRemove()  # if sent as reply_markup, will hide the keyboard

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
# (obsolete once known users are saved to file, because all users
#   had to use the /start command and are therefore known to the bot)
def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print("New user detected, who hasn't used \"/start\" yet")
        return 0


# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)  # register listener


def hello_world():
    print("hello world")

def set_timer():
    """Add a job to the queue."""
    # cid = messages.chat.id
    x = datetime.today()
    y = x.replace(day=x.day, hour=3, minute=33, second=0)
    delta_t=y-x

    secs=delta_t.seconds+1
    print("hello")
    # bot.send_message("testing")
    t = Timer(secs, hello_world)
    t.start()

# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    name = m.chat.username
    # if cid not in knownUsers:  # if user hasn't used the "/start" command yet:
    # knownUsers.append(cid)  # save user id, so you could brodcast messages to all users of this bot later
    # userStep[cid] = 0  # save user id and his current "command level", so he can use the "/getImage" command
    bot.send_message(cid, "Hi @%s ! Welcome to Kronos Daily Attendance helper bot!" %name)

    markup = types.ReplyKeyboardMarkup()
    itembtna = types.KeyboardButton('/Start_working')
    itembtnv = types.KeyboardButton('/Sick_leave')
    itembtnc = types.KeyboardButton('/Business Trip')
    itembtnd = types.KeyboardButton('/Vacation')
    itembtne = types.KeyboardButton('/cancel')
    markup.row(itembtna, itembtnv)
    markup.row(itembtnc, itembtnd, itembtne)
    bot.send_message(cid, "Please choose a command below:", reply_markup=markup)


@bot.message_handler(commands=['Start_working'])
def command_start_working(m):
    cid = m.chat.id
    bot.send_message(cid, "Have a nice day working buddy!")
    now = datetime.now()
    now = now.replace(second=0, microsecond=0)
    # now.strftime('%Y-%m-%dT%H:%M')
    bot.send_message(cid, "@%s" %now)

@bot.message_handler(commands=['Sick_leave'])
def command_sick_leave(m):
    cid = m.chat.id
    bot.send_message(cid, "Oh no, hope you will get well soon.")
    #implement a calendar here
    # bot.send_message(cid, "Please choose the duration of this leave", reply_markup=telegramcalendar.create_calendar())

@bot.message_handler(commands=['Business_trip'])
def command_business_trip(m):
    cid = m.chat.id
    bot.send_message(cid, "All the best!")
    #implement a calendar here

@bot.message_handler(commands=['Vacation'])
def command_vacation(m):
    cid = m.chat.id
    bot.send_message(cid, "So good")
    #implement a calendar here


# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page


# chat_action example (not a good one...)
@bot.message_handler(commands=['sendLongText'])
def command_long_text(m):
    cid = m.chat.id
    bot.send_message(cid, "If you think so...")
    bot.send_chat_action(cid, 'typing')  # show the bot "typing" (max. 5 secs)
    time.sleep(3)
    bot.send_message(cid, ".")


# user can chose an image (multi-stage command example)
@bot.message_handler(commands=['getImage'])
def command_image(m):
    cid = m.chat.id
    bot.send_message(cid, "Please choose your image now", reply_markup=imageSelect)  # show the keyboard
    userStep[cid] = 1  # set the user to the next step (expecting a reply in the listener now)


# if the user has issued the "/getImage" command, process the answer
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def msg_image_select(m):
    cid = m.chat.id
    text = m.text

    # for some reason the 'upload_photo' status isn't quite working (doesn't show at all)
    bot.send_chat_action(cid, 'typing')

    if text == "cock":  # send the appropriate image based on the reply to the "/getImage" command
        bot.send_photo(cid, open('rooster.jpg', 'rb'),
                       reply_markup=hideBoard)  # send file and hide keyboard, after image is sent
        userStep[cid] = 0  # reset the users step back to 0
    elif text == "pussy":
        bot.send_photo(cid, open('kitten.jpg', 'rb'), reply_markup=hideBoard)
        userStep[cid] = 0
    else:
        bot.send_message(cid, "Don't type bullsh*t, if I give you a predefined keyboard!")
        bot.send_message(cid, "Please try again")


# filter on a specific message
@bot.message_handler(func=lambda message: message.text == "hi")
def command_text_hi(m):
    bot.send_message(m.chat.id, "I love you too!")


# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "I don't understand \"" + m.text + "\"\nMaybe try the help page at /help")


set_timer()

bot.polling()
