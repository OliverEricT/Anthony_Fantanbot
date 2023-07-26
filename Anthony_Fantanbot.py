import os
import logging
import datetime
import pytz
import json
from dotenv import load_dotenv
from functools import wraps
from telegram import (
	Update
)
from telegram.ext import (
	ApplicationBuilder,
	ContextTypes,
	CommandHandler,
	CallbackContext,
	JobQueue
)

load_dotenv()

# Enable logging
logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')
LIST_OF_ADMINS = os.getenv('ADMINS').split(',')
MUSIC_CHAT_ID = os.getenv('MUSIC_CHAT_ID')
DEBUG_CHAT_ID = os.getenv('DEBUG_CHAT_ID')

#########################
#   Telegram Commands   #
#########################

def restricted(func):
	"""
	Decorator function to only allow admins to send certain commands
	"""
	@wraps(func)
	def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
		user_id = update.effective_user.id
		if user_id not in LIST_OF_ADMINS:
			update.message.reply_text("ACCESS DENIED!")
			return
		return func(update, context, *args, **kwargs)
	return wrapped

@restricted
async def GetUserID(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	"""
	Restricted. Sends the current users id
	"""
	user_name = update.effective_user.name
	user_id = update.effective_user.id
	await context.bot.send_message(chat_id=DEBUG_CHAT_ID, text="User \"{0}\": {1}".format(user_name, user_id))

@restricted
async def GetGroupID(update: Update,context: ContextTypes.DEFAULT_TYPE) -> None:
	"""
	Restricted. Sends the current users id
	"""
	chat_name = update.effective_chat.effective_name
	chat_id = update.effective_chat.id
	await context.bot.send_message(chat_id=DEBUG_CHAT_ID, text="Group \"{0}\": {1}".format(chat_name, chat_id))

async def SendThicc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	await PhotoSender(update, context, 'Media/THICC.mp4')

async def SendTest(context: ContextTypes.DEFAULT_TYPE) -> None:
	await context.bot.send_message(chat_id=DEBUG_CHAT_ID, text='**Hello**!!!', parse_mode='Markdown')

async def SendNut(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	await PhotoSender(update, context, 'Media/Nutt.mp4')

async def SendJuicy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	await PhotoSender(update, context, 'Media/Grapefruit.mp4')

async def PhotoSender(update: Update, context: ContextTypes.DEFAULT_TYPE, imagePath: str) -> None:
	"""
	Helper function to send a photo by path
	"""
	photo = open(file=imagePath,mode='rb')
	await context.bot.sendAnimation(chat_id=update.message.chat_id, animation=photo)

async def ParseQueue(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	"""
	Function to parse the queue. Should move this to another class or db logic
	"""
	countChanged = 0
	lstChangedToZero = []
	lstChangedToNOne = []

	#TODO: Fix the parser to not do anything
	with open('Queue.json','r') as file:
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

	with open('Queue.json','w') as file:
		json.dump(queue,file,indent=2)

	context.bot.send_message(chat_id=DEBUG_CHAT_ID, text=msgText, parse_mode='Markdown')

@restricted
async def SendReview(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	reviewJson = GetNextInQueue()

	photo = open(file=reviewJson["AlbumArt"],mode='rb')

	count = GetNumCompleted()
	reviewJson["ID"] = count

	genreTxt = FormatGenreBlock(reviewJson)
	TrackList = FormatTrackList(reviewJson)
	rating = FormatRatingBlock(reviewJson)

	#TODO: Change this up
	idText = "#AlbumReview No. {0}".format(count + 1)
	msgBody = "{0}\n\n*Album Title*\n{1}\n\n*Album Artist*\n{2}\n\n*Genre*\n{3}\n\n*Thoughts*\n{4}\n\n*Track Ratings*\n{5}\n\n*Overall Rating*\n{6}\n\n{7}".format(idText,reviewJson["Title"],reviewJson["Artist"],genreTxt,reviewJson["ReviewBody"],TrackList,rating,reviewJson["NextUpText"])

	await context.bot.sendPhoto(chat_id=MUSIC_CHAT_ID, photo=photo)
	await context.bot.send_message(chat_id=MUSIC_CHAT_ID, text=msgBody, parse_mode='Markdown')

	UpdateCompleted(reviewJson)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	"""Log Errors caused by Updates."""

	errorMsg = "Update\n `{0}`\n\n caused error\n `{1}`".format(update, context.error)

	await context.bot.send_message(chat_id=DEBUG_CHAT_ID, text=errorMsg)
	logger.warning('Update "%s" caused error "%s"', update, context.error) 

#####################
#   Get Functions   #
#####################

def GeNextUpText(reviewLst: json) -> str:
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
    
def GetNextInQueue() -> json:
	with open('Queue.json','r') as file:
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

	with open('Queue.json','w') as file:
		json.dump(queue,file,indent=2)

	return review

def GetNumCompleted() -> int:
	with open('Posted_Reviews.json','r') as file:
		completed = json.load(file)

	count = len(completed["Completed"])

	return count

########################
#   Format Functions   #
########################

def FormatTrackList(reviewJson: json) -> str:
	trackList = reviewJson["TrackList"]

	tList = ""

	for i in range(0,(len(trackList)-1),2):
		tList += "{TrackNo:02d} - {TrackTitle} - {Rating}/5\n".format(TrackNo = int((i/2)+1), TrackTitle = trackList[i], Rating = trackList[i+1])

	return tList

def FormatNextUp(review: json) -> str:
	return "NEXT UP:\n\n{0} by {1}\n\n{2}".format(review["Title"],review["Artist"],review["Blurb"])

def FormatRatingBlock(json: json) -> str:
	txt = "(personal rating + Songs avg) / 2 = Rating\n"

	txt += "( {0} + {1} ) / 2 = {2}".format(json["AlbumFeelingRating"],json["SongAvg"],json["AlbumRating"])

	return txt

def FormatGenreBlock(json: json) -> str:
	genres = json["Genre"]

	genreTxt = ""

	for i in genres:
		genreTxt += "{0}, ".format(i)

	return genreTxt[:-2]

def CheckReviewForValue(queue: json,equalTo: any) -> bool:
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

def UpdateCompleted(review: json) -> None:
	with open('Posted_Reviews.json','r') as file:
		completed = json.load(file)
	
	review["DatePosted"] = datetime.datetime.now().isoformat()
	completed["Completed"].append(review)

	with open('Posted_Reviews.json','w') as file:
		json.dump(completed,file,indent=2)

def Main() -> None:
	application = ApplicationBuilder().token(BOT_TOKEN).build()
	job_queue = application.job_queue

	application.add_handler(CommandHandler('getuserid',GetUserID))
	application.add_handler(CommandHandler('getgroupid',GetGroupID))
	application.add_handler(CommandHandler('sendreview',SendReview))
	application.add_handler(CommandHandler('thicc',SendThicc))
	application.add_handler(CommandHandler('ParseQueue',ParseQueue))
	application.add_handler(CommandHandler('Nut',SendNut))
	application.add_handler(CommandHandler('Juicy',SendJuicy))

	application.add_error_handler(error)

	# Sends the review at 10 am every monday
	tenAm = datetime.time(hour=10, tzinfo=pytz.timezone('America/Chicago'))
	job_queue.run_daily(SendReview,tenAm,days=(1,1))

	try:
		application.run_polling()
	except:
		print('An Error has occurred.')
	print('Stopped')

if __name__ == '__main__':
	Main()