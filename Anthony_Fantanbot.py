import logging
import json
from functools import wraps
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackContext)
import schedule
from threading import Thread
from time import sleep
import os
import datetime

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

vars = json.load(open(os.path.join(__location__,'Telegram.json'),'r'))
LIST_OF_ADMINS = vars["ADMINS"]

def restricted(func):
    @wraps(func)
    def wrapped(update,context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            update.message.reply_text("ACCESS DENIED!")
            return
        return func(update,context, *args, **kwargs)
    return wrapped

@restricted
def CustomeQuery(update,context):
    pass

@restricted
def GetUserID(update,context):
    user_id = update.effective_user.id
    update.message.reply_text(str(user_id) + ": Your user ID")

def SendThicc(update,context):
    photo = open(file=os.path.join(__location__,'THICC.mp4'),mode='rb')
    context.bot.sendAnimation(chat_id=vars["CHATID"], animation=photo)

def GetNextInQueue():
    with open(os.path.join(__location__,'Queue.json'),'r') as file:
        queue = json.load(file)

    if len(queue["Queue"]) == 0:
        review = None
    elif len(queue["Queue"]) == 1:
        review = queue["Queue"].pop(0)
        review["NextUpText"] = "NEXT UP:\n\nQueue is Empty"
    else:
        review = queue["Queue"].pop(0)
        nextUpText = FormatNextUp(queue["Queue"][0])
        review["NextUpText"] = nextUpText

    with open(os.path.join(__location__,'Queue.json'),'w') as file:
        json.dump(queue,file,indent=2)

    return review

def UpdateCompleted(review):
    with open(os.path.join(__location__,'Posted_Reviews.json'),'r') as file:
        completed = json.load(file)
    
    review["DatePosted"] = datetime.datetime.now().isoformat()
    completed["Completed"].append(review)

    with open(os.path.join(__location__,'Posted_Reviews.json'),'w') as file:
        json.dump(completed,file,indent=2)

def FormatTracklist(reviewJson):
    trackList = reviewJson["TrackList"]

    tList = ""

    for i in range(0,(len(trackList)-1),2):
        tList += "{TrackNo:02d} - {TrackTitle} - {Rating}/5\n".format(TrackNo = int((i/2)+1), TrackTitle = trackList[i], Rating = trackList[i+1])

    return tList

def FormatNextUp(review):
    return "NEXT UP:\n\n{0} by {1}\n\n{2}".format(review["Title"],review["Artist"],review["Blurb"])

@restricted
def SendReview(update,context):
    MusicChatID = vars["CHATID"]
    #MusicChatID = vars["SELFID"]
    reviewJson = GetNextInQueue()

    photo = open(file=reviewJson["AlbumArt"],mode='rb')

    TrackList = FormatTracklist(reviewJson)

    context.bot.send_message(chat_id=MusicChatID, text="#AlbumReview")
    context.bot.sendPhoto(chat_id=MusicChatID, photo=photo)
    context.bot.send_message(chat_id=MusicChatID, text=reviewJson["ReviewBody"], parse_mode='Markdown')
    context.bot.send_message(chat_id=MusicChatID, text=TrackList)
    context.bot.send_message(chat_id=MusicChatID, text=reviewJson["NextUpText"], parse_mode='Markdown')

    UpdateCompleted(reviewJson)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def callback_minute(context: CallbackContext):
    context.bot.send_message(chat_id=vars["SELFID"], 
                             text='One message every minute')

def callback_Review(context: CallbackContext):
    SendReview(update,context)

def Main():

    updater = Updater(vars["TOKEN"], use_context=True)
    job_queue = updater.job_queue

    dispatcher = updater.dispatcher

    UserID_handler = CommandHandler('getuserid',GetUserID)
    Review_handler = CommandHandler('sendreview',SendReview)
    Thicc_handler = CommandHandler('thicc',SendThicc)

    dispatcher.add_handler(UserID_handler)
    dispatcher.add_handler(Review_handler)
    dispatcher.add_handler(Thicc_handler)

    dispatcher.add_error_handler(error)

    job_review = job_queue.run_daily(callback=callback_Review,time=datetime.time(hour = 10, minute = 0, second = 0),days=(0,4))

    #if datetime.date.today().isoweekday() == 1 or datetime.date.today().isoweekday() == 5:
    #    job_review.Enabled = True
    #else:
    #    job_review.Enabled = False

    updater.start_polling()
    updater.idle()
    print('Stopped')

if __name__ == '__main__':
    Main()
    #GetNextInQueue()
