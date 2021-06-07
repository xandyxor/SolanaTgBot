from telegram.ext import Updater # 更新者
from telegram.ext import CommandHandler, CallbackQueryHandler # 註冊處理 一般用 回答用
from telegram.ext import MessageHandler, Filters # Filters過濾訊息
from telegram import InlineKeyboardMarkup, InlineKeyboardButton # 互動式按鈕
from telegram.ext import CallbackContext,ConversationHandler
from telegram import Update

updater = Updater("")

import random


FIRST, SECOND = range(2)
ONE, TWO, THREE, FOUR = range(4)


def start(update: Update, context: CallbackContext): # 新增指令/start
    message = update.message
    chat = message['chat']
    update.message.reply_text(text='HI  ' + str(chat['id'])) 
    # updater.dispatcher.bot.send_message(chat_id=263495856, text=str(chat['id'])) # 發送訊息
    return FIRST

def buy_btn(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="\n請輸入要"+query.data+"的數量")
    print(update.callback_query.message.message_id)
    print(update.callback_query.message.chat.id)
    return SECOND

def sell_btn(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="\n請輸入要"+query.data+"的數量")
    print(update.callback_query.message.message_id)
    print(update.callback_query.message.chat.id)
    return SECOND

import requests


def inquire(update: Update, context: CallbackContext): # 新增指令/start
    message = update.message
    chat = message['chat']
    currency = message.text.replace('/q ', '').strip().upper()
    keyboard = [
        [
            InlineKeyboardButton("BUY", callback_data='BUY'),
            InlineKeyboardButton("SELL", callback_data='SELL'),
        ],
        [],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    r = requests.get('https://serum-api.bonfida.com/trades/'+currency+'USDC')
    
    if r.status_code == requests.codes.ok:
        update.message.reply_text(text=currency+' : ' + str(r.json()['data'][0]['price']),reply_markup=reply_markup) 
        
    else:
        r = requests.get('https://serum-api.bonfida.com/trades/'+currency+'USDT')
        if r.status_code == requests.codes.ok:
            update.message.reply_text(text=currency+' : ' + str(r.json()['data'][0]['price']),reply_markup=reply_markup) 
        else:
            update.message.reply_text(text='查不到'+str(currency)+'耶')


def main() -> None:
    """Run the bot."""
    dispatcher = updater.dispatcher

    # updater.dispatcher.bot.send_message(chat_id=263495856, text="text") # 發送訊息

    # updater.dispatcher.add_handler(CommandHandler('start', start))
    # updater.dispatcher.add_handler(CommandHandler('rand', rand))
    # updater.dispatcher.add_handler(CommandHandler('q', inquire))
    # updater.dispatcher.add_handler(CallbackQueryHandler(buy_sell_btn,pattern=""))
    # updater.dispatcher.add_handler(CallbackQueryHandler(buy_sell_btn,pattern=""))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [
                CallbackQueryHandler(buy_btn, pattern='^(Buy|buy|BUY)$'),
                CallbackQueryHandler(sell_btn, pattern='^(Sell|sell|SELL)$'),
                CommandHandler('q', inquire),
                # CallbackQueryHandler(two, pattern='^' + str(TWO) + '$'),
                # CallbackQueryHandler(three, pattern='^' + str(THREE) + '$'),
                # CallbackQueryHandler(four, pattern='^' + str(FOUR) + '$'),
            ],
            
            SECOND: [
                CommandHandler('q', inquire),
                # MessageHandler(Filters.text & ~Filters.command, bio)
                # CallbackQueryHandler(start_over, pattern='^' + str(ONE) + '$'),
                # CallbackQueryHandler(end, pattern='^' + str(TWO) + '$'),
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add ConversationHandler to dispatcher that will be used for handling updates
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()
    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()