import logging
import json
from functools import wraps
from telegram import (
  ReplyKeyboardMarkup,
  ReplyKeyboardRemove
)
from telegram.ext import (
	Updater,
	CommandHandler,
	MessageHandler,
	Filters,
	ConversationHandler,
	CallbackContext
)
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

#########################
#   Telegram Commands   #
#########################

def restricted(func):
	"""
	Decorator function to only allow admins to send certain commands
	"""
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
	"""
	Restricted. Sends the current users id
	"""
	user_id = update.effective_user.id
	update.message.reply_text(str(user_id) + ": Your user ID")

def SendThicc(update,context):
	PhotoSender(update, context, 'Media\\THICC.mp4')

def SendNut(update,context):
	PhotoSender(update, context, 'Media\\Nutt.mp4')

def SendJuicy(update,context):
	PhotoSender(update, context, 'Media\\Grapefruit.mp4')

def PhotoSender(update, context, imagePath: str) -> None:
	"""
	Helper function to send a photo by path
	"""
	photo = open(file=os.path.join(__location__,imagePath),mode='rb')
	context.bot.sendAnimation(chat_id=update.message.chat_id, animation=photo)

def ParseQueue(update, context):
	countChanged = 0
	lstChangedToZero = []
	lstChangedToNOne = []

	with open(os.path.join(__location__,'Queue.json'),'r') as file:
		queue = json.load(file)
		queueShort = queue["Queue"]

	if len(queueShort) == 0:
		return None

	for review in queueShort:
		if review["ID"] == 0:
			if CheckReviewForValue(review,""):
				review["ID"] = -1
				countChanged += 1
				lstChangedToNOne.append(review["Title"])
		elif review["ID"] == -1:
			if not CheckReviewForValue(review,""):
				review["ID"] = 0
				countChanged += 1
				lstChangedToZero.append(review["Title"])

	msgText = "*Parse Results*\n\nTotal Changed: {0}".format(countChanged)

	msgText += "\n\nItems Changed to `Not Queue Ready`: "
	for item in lstChangedToNOne:
		msgText += "\n\t" + item

	msgText += "\n\nItems Changed to `Queue Ready`: "
	for item in lstChangedToZero:
		msgText += "\n\t" + item

	queue["Queue"] = queueShort

	with open(os.path.join(__location__,'Queue.json'),'w') as file:
		json.dump(queue,file,indent=2)

	context.bot.send_message(chat_id=vars["SELFID"], text=msgText, parse_mode='Markdown')

@restricted
def SendReview(update,context):
	MusicChatID = vars["CHATID"]
	#MusicChatID = vars["SELFID"]
	reviewJson = GetNextInQueue()

	photo = open(file=reviewJson["AlbumArt"],mode='rb')

	count = GetNumCompleted()
	reviewJson["ID"] = count

	genreTxt = FormatGenreBlock(reviewJson)
	TrackList = FormatTracklist(reviewJson)
	rating = FormatRatingBlock(reviewJson)

	idText = "#AlbumReview No. {0}".format(count + 1)
	msgBody = "{0}\n\n*Album Title*\n{1}\n\n*Album Artist*\n{2}\n\n*Genre*\n{3}\n\n*Thoughts*\n{4}\n\n*Track Ratings*\n{5}\n\n*Overall Rating*\n{6}\n\n{7}".format(idText,reviewJson["Title"],reviewJson["Artist"],genreTxt,reviewJson["ReviewBody"],TrackList,rating,reviewJson["NextUpText"])

	context.bot.sendPhoto(chat_id=MusicChatID, photo=photo)
	context.bot.send_message(chat_id=MusicChatID, text=msgBody, parse_mode='Markdown')

	UpdateCompleted(reviewJson)

def error(update, context):
	"""Log Errors caused by Updates."""

	errorMsg = "Update\n `{0}`\n\n caused error\n `{1}`".format(update,context.error)

	context.bot.send_message(chat_id=vars["SELFID"], text=errorMsg)
	logger.warning('Update "%s" caused error "%s"', update, context.error) 

#####################
#   Get Functions   #
#####################

def GeNextUpText(reviewLst):
	end = False
	index = 0

	while not end:
		if reviewLst[index]["ID"] != -1:
			if len(reviewLst) == 1 or index == len(reviewLst):
				NextUpText = "NEXT UP:\n\nQueue is Empty"
				end = True
			else:
				NextUpText = FormatNextUp(reviewLst[index])
				reviewLst[index]["ID"] = 1
				end = True
		else:
			index += 1

	return NextUpText
    
def GetNextInQueue():
	with open(os.path.join(__location__,'Queue.json'),'r') as file:
		queue = json.load(file)
		queueShort = queue["Queue"]

	if len(queueShort) == 0:
		return None

	end = False
	index = 0

	while not end:
		if queueShort[index]["ID"] == 1:
			end = True
		else:
			index += 1

	review = queueShort.pop(index)
	review["NextUpText"] = GeNextUpText(queueShort)

	queue["Queue"] = queueShort

	with open(os.path.join(__location__,'Queue.json'),'w') as file:
		json.dump(queue,file,indent=2)

	return review

def GetNumCompleted():
	with open(os.path.join(__location__,'Posted_Reviews.json'),'r') as file:
		completed = json.load(file)

	count = len(completed["Completed"])

	return count

########################
#   Format Functions   #
########################

def FormatTracklist(reviewJson):
	trackList = reviewJson["TrackList"]

	tList = ""

	for i in range(0,(len(trackList)-1),2):
		tList += "{TrackNo:02d} - {TrackTitle} - {Rating}/5\n".format(TrackNo = int((i/2)+1), TrackTitle = trackList[i], Rating = trackList[i+1])

	return tList

def FormatNextUp(review):
	return "NEXT UP:\n\n{0} by {1}\n\n{2}".format(review["Title"],review["Artist"],review["Blurb"])

def FormatRatingBlock(json):
	txt = "(personal rating + Songs avg) / 2 = Rating\n"

	txt += "( {0} + {1} ) / 2 = {2}".format(json["AlbumFeelingRating"],json["SongAvg"],json["AlbumRating"])

	return txt

def FormatGenreBlock(json):
	genres = json["Genre"]

	gtxt = ""

	for i in genres:
		gtxt += "{0}, ".format(i)

	gtxt = gtxt[:-2]

	return gtxt

def CheckReviewForValue(queue,equalTo):
	if queue["Title"] == equalTo:
		return True

	if queue["Artist"] == equalTo:
		return True

	if queue["ReviewBody"] == equalTo:
		return True

	if queue["AlbumRating"] == equalTo:
		return True

	if queue["AlbumFeelingRating"] == equalTo:
		return True

	if queue["SongAvg"] == equalTo:
		return True

	if queue["TrackList"] == equalTo:
		return True

	if queue["AlbumArt"] == equalTo:
		return True

	if queue["Genre"] == equalTo:
		return True

	if queue["Blurb"] == equalTo:
		return True
	return False

def UpdateCompleted(review):
	with open(os.path.join(__location__,'Posted_Reviews.json'),'r') as file:
		completed = json.load(file)
	
	review["DatePosted"] = datetime.datetime.now().isoformat()
	completed["Completed"].append(review)

	with open(os.path.join(__location__,'Posted_Reviews.json'),'w') as file:
		json.dump(completed,file,indent=2)

def SendTimedReview(context):
	#MusicChatID = vars["CHATID"]
	MusicChatID = vars["SELFID"]
	reviewJson = GetNextInQueue()

	photo = open(file=reviewJson["AlbumArt"],mode='rb')

	TrackList = FormatTracklist(reviewJson)
	rating = FormatRatingBlock(reviewJson)

	msgBody = "*Thoughts*\n{0}\n\n*Track Ratings*\n{1}\n\n*Overall Rating*\n{2}".format(reviewJson["ReviewBody"],TrackList,rating)

	context.bot.send_message(chat_id=MusicChatID, text="#AlbumReview")
	context.bot.sendPhoto(chat_id=MusicChatID, photo=photo)
	#context.bot.send_message(chat_id=MusicChatID, text=reviewJson["ReviewBody"], parse_mode='Markdown')
	#context.bot.send_message(chat_id=MusicChatID, text=TrackList)
	#context.bot.send_message(chat_id=MusicChatID, text=reviewJson["NextUpText"], parse_mode='Markdown')
	context.bot.send_message(chat_id=MusicChatID, text=msgBody, parse_mode='Markdown')
	context.bot.send_message(chat_id=MusicChatID, text=reviewJson["NextUpText"], parse_mode='Markdown')

	UpdateCompleted(reviewJson)

def callback_Review(context: CallbackContext):
	SendTimedReview(context)

def TestSend(update, context):
	context.bot.send_message(chat_id=vars["SELFID"], text="Henlo", parse_mode='Markdown')

def Main():

	updater = Updater(vars["TOKEN"], use_context=True)
	job_queue = updater.job_queue

	dispatcher = updater.dispatcher

	dispatcher.add_handler(CommandHandler('getuserid',GetUserID))
	dispatcher.add_handler(CommandHandler('sendreview',SendReview))
	dispatcher.add_handler(CommandHandler('thicc',SendThicc))
	dispatcher.add_handler(CommandHandler('ParseQueue',ParseQueue))
	dispatcher.add_handler(CommandHandler('Nut',SendNut))
	dispatcher.add_handler(CommandHandler('Juicy',SendJuicy))

	dispatcher.add_error_handler(error)

	updater.start_polling()
	updater.idle()
	print('Stopped')

if __name__ == '__main__':
	Main()
