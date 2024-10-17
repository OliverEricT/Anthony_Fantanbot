import os
import logging
import datetime
import pytz
import base64
from dotenv import load_dotenv
from functools import wraps
from telegram import (
	Update
)
from telegram.ext import (
	ApplicationBuilder,
	ContextTypes,
	CommandHandler
)
from Services import (
	ReviewParserService,
	SQLService
)
from Objects import (
	Review
)

load_dotenv()

# Enable logging
logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.INFO
)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)

BOT_TOKEN = os.getenv('BOT_TOKEN')
LIST_OF_ADMINS = os.getenv('ADMINS').split(',')
MUSIC_CHAT_ID = os.getenv('MUSIC_CHAT_ID')
DEBUG_CHAT_ID = os.getenv('DEBUG_CHAT_ID')
CONNECTION_STRING = os.getenv('CONNECTION_STRING')
REVIEWS_FOLDER = os.getenv('REVIEWS_FOLDER') or '/Music'

service: SQLService.SQLService

#########################
#   Security Commands   #
#########################

def restricted(func):
	"""
	Decorator function to only allow admins to send certain commands
	"""
	@wraps(func)
	async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
		user_id = update.effective_user.id
		if str(user_id) not in LIST_OF_ADMINS:
			await update.message.reply_text("ACCESS DENIED!")
			return
		return await func(update, context, *args, **kwargs)
	return wrapped

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	"""
	Log Errors caused by Updates.
	"""

	errorMsg = "Update\n `{0}`\n\n caused error\n `{1}`".format(update, context.error)

	await context.bot.send_message(chat_id=DEBUG_CHAT_ID, text=errorMsg)
	logger.warning('Update "%s" caused error "%s"', update, context.error) 

#########################
#   Telegram Commands   #
#########################

@restricted
async def GetUserID(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
	Restricted. Sends the current users id
	"""
    logger.warning("Call to GetUserID registered")
    user_name = update.effective_user.name
    user_id = update.effective_user.id
    await context.bot.send_message(chat_id=DEBUG_CHAT_ID, text="User \"{0}\": {1}".format(user_name, user_id))

@restricted
async def GetGroupID(update: Update,context: ContextTypes.DEFAULT_TYPE) -> None:
	"""
	Restricted. Sends the current users id
	"""
	logger.warning("Call to GetGroupID registered")
	chat_name = update.effective_chat.effective_name
	chat_id = update.effective_chat.id
	await context.bot.send_message(chat_id=DEBUG_CHAT_ID, text="Group \"{0}\": {1}".format(chat_name, chat_id))

@restricted
async def ParseQueue(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	"""
	Restricted to Admins

	Function to scrape the provided folder path for reviews and to dump them into
	the database
	"""
	logger.warning("Call to ParseQueue registered")
	await ScrapeReviews(context)

@restricted
async def SendReview(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	"""
	Restricted to Admins

	Function that is callable by telegram command to get another review and post it	
	"""
	logger.warning("Call to SendReview registered")
	global service
	review: Review.Review = service.GetNextInQueue()

	try:
		photo = base64.b64decode(review.albumArt)
		await context.bot.sendPhoto(chat_id=update.message.chat_id, photo=photo)
	except:
		await context.bot.send_message(chat_id=DEBUG_CHAT_ID, text="Uh Oh Can't find the image", parse_mode='Markdown')

	msgBody: str = ParseReviewToMessage(review)
	await context.bot.send_message(chat_id=update.message.chat_id, text=msgBody, parse_mode='Markdown')

@restricted
async def WriteReviewsToFiles(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Restricted to admins

    Function to take all the reviews and then write them to a file
    """
    logger.warning("Call to WriteReviewsToFiles registered")
    global service

    reviews: list[Review.Review] = service.GetAllReviews()

    for review in reviews:
        print(f"Reading review: {review.title} by {review.artist.name}")
        lines = ReviewParserService.ParseReviewObj(review)
        fileName = f"{review.title} album review.md".replace(" ","_").replace("/","")
        sortArtist = ReviewParserService._Sortify(review.artist.name)
        path = f"{REVIEWS_FOLDER}/{sortArtist}/{review.sortTitle}"

        if not os.path.exists(path):
            print("Folder does not exist, placing in root folder")
            path = REVIEWS_FOLDER

        try:
            file = open(f"{path}/{fileName}","w")
            file.write(''.join(lines))
            print(f"Wrote {fileName}")
        except:
            print(f"Could not write {fileName}")

    
    await context.bot.send_message(chat_id=DEBUG_CHAT_ID, text=f"Done!")

@restricted
async def SendReviewById(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	"""
	Restricted to Admins

	Sends a specific review by the review Id
	"""
	logger.warning("Call to SendReviewById registered")
	global service
	review: Review.Review = service.GetReviewById(int(context.args[0]))

	try:
		photo = base64.b64decode(review.albumArt)
		await context.bot.sendPhoto(chat_id=update.message.chat_id, photo=photo)
	except:
		await context.bot.send_message(chat_id=DEBUG_CHAT_ID, text="Uh Oh Can't find the image", parse_mode='Markdown')

	msgBody: str = ParseReviewToMessage(review)
	await context.bot.send_message(chat_id=update.message.chat_id, text=msgBody, parse_mode='Markdown')

async def SendTest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	photo = open(file='//DEEPTHOUGHT/Media/Music/+44/When Your Heart Stops Beating/Cover.jpg',mode='rb')
	encodedString = base64.b64encode(photo.read())

	global service
	service.TestQuery(encodedString)

	review: Review.Review = service.GetReviewById(1)
	retyped = bytes(review.albumArt)
	
	photo2 = base64.b64decode(retyped)
	await context.bot.sendPhoto(chat_id=DEBUG_CHAT_ID, photo=photo2)

async def SendThicc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	logger.warning("Call to SendThicc registered")
	await PhotoSender(update, context, 'Media/THICC.mp4')

async def SendNut(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	logger.warning("Call to SendNut registered")
	await PhotoSender(update, context, 'Media/Nutt.mp4')

async def SendJuicy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	logger.warning("Call to SendJuicy registered")
	await PhotoSender(update, context, 'Media/Grapefruit.mp4')

######################
#   Timer Commands   #
######################

async def ScrapeReviews(context: ContextTypes.DEFAULT_TYPE):
	"""
	Restricted to Admins

	Function to scrape the provided folder path for reviews and to dump them into
	the database
	"""
	global service
	totalReviews: int = 0
	insertedReviews: int = 0
	insertedReviewLines: str = ''

	for path, subdirs, files in os.walk(REVIEWS_FOLDER):
		for name in files:
			fullName = os.path.join(path,name)
			
			if name[-15:].lower() != 'album_review.md':
				continue

			logger.warning(f'Parsing {name}')

			totalReviews += 1
			
			reviewFile = open(file=fullName,mode='r')
			try:
				lines = reviewFile.readlines()
				reviewFile.close()
			except:
				await context.bot.send_message(chat_id=DEBUG_CHAT_ID, text=f'Encountered an issue with: {fullName}')
				continue

			if lines is None or len(lines) < 1:
				logging.warning('File is empty')
				continue
			
			if not ReviewParserService.IsReadyToParse(lines[0]):
				continue

			insertedReviews += 1

			review = ReviewParserService.ParseReviewMd(lines, fullName)
			service.InsertArtist(review.artist)
			reviewId = service.SaveReview(review)
			for song in review.trackList:
				success = service.InsertSong(reviewId,song)
			for genre in review.genre:
				success = service.InsertGenre(reviewId,genre)
			insertedReviewLines = f'{insertedReviewLines}\n{review.title}'

			#if reviewId:
				#os.remove(fullName)

	message: str = f"""
**Scrape Report**

**Found:** {totalReviews}

**Inserted:** {insertedReviews}

**Albums Inserted:**{insertedReviewLines}
"""

	await context.bot.send_message(chat_id=DEBUG_CHAT_ID, text=message, parse_mode='Markdown')

async def SendReviewTimer(context: ContextTypes.DEFAULT_TYPE):
	"""
	Restricted to Admins

	Function that is missing an update since it is called via a timer.
	but this function takes the next review in the queue and then posts it
	"""
	global service
	review: Review.Review = service.GetNextInQueue()

	try:
		photo = base64.b64decode(review.albumArt)
		await context.bot.sendPhoto(chat_id=MUSIC_CHAT_ID, photo=photo)
	except:
		await context.bot.send_message(chat_id=DEBUG_CHAT_ID, text="Uh Oh Can't find the image", parse_mode='Markdown')

	msgBody: str = ParseReviewToMessage(review)
	await context.bot.send_message(chat_id=MUSIC_CHAT_ID, text=msgBody, parse_mode='Markdown')

########################
#   Helper Functions   #
########################

async def PhotoSender(update: Update, context: ContextTypes.DEFAULT_TYPE, imagePath: str) -> None:
	"""
	Helper function to send a photo by path
	"""
	photo = open(file=imagePath,mode='rb')
	await context.bot.sendAnimation(chat_id=update.message.chat_id, animation=photo)

def ParseReviewToMessage(review: Review.Review) -> str:
	trackList: list[str] = []
	for song in review.trackList:
		trackList.append(f'{song.TrackNo:02} - {song.Name} - {song.Rating}/5\n')

	nextSplits = review.nextUp.split('\\n\\n')
	nextAlbum = nextSplits[0]
	nextText = nextSplits[1]

	msgBody: str = f"""
#AlbumReview No. {review.numberPosted}

*Album Title*
{review.title}

*Album Artist*
{review.artist.name}

*Genre*
{review.genre}

*Thoughts*
{review.body}

*Track Ratings*
{"".join(trackList)}

*Overall Rating*
(personal rating + Songs Average) / 2 = Rating
({review.feelingRating} + {round(review.songAvg,1)}) / 2 = {round(review.OverallRating,1)} = {round(review.OverallRating)}

*NEXT UP:*

{nextAlbum}

{nextText}
"""
	return msgBody

############
#   MAIN   #
############

def Main() -> None:
	logger.warning("Due to a change in httpx, warn is the new information level")
	global service
	service = SQLService.SQLService(CONNECTION_STRING)

	# Initialize the bot
	application = ApplicationBuilder().token(BOT_TOKEN).build()
	job_queue = application.job_queue

	application.add_handler(CommandHandler('getuserid',GetUserID))
	application.add_handler(CommandHandler('getgroupid',GetGroupID))
	application.add_handler(CommandHandler('sendreview',SendReview))
	application.add_handler(CommandHandler('sendreviewbyid',SendReviewById))
	application.add_handler(CommandHandler('parsequeue',ParseQueue))
	application.add_handler(CommandHandler('thicc',SendThicc))
	application.add_handler(CommandHandler('Nut',SendNut))
	application.add_handler(CommandHandler('Juicy',SendJuicy))
	application.add_handler(CommandHandler('sendTest',SendTest))
	application.add_handler(CommandHandler('writeReviews',WriteReviewsToFiles))

	#application.add_error_handler(error)

	# Sends the review at 10 am every Monday and Friday
	tenAm = datetime.time(hour=10, tzinfo=pytz.timezone('America/Chicago'))
	reviewJob = job_queue.run_daily(SendReviewTimer,tenAm,days=(1,5))

	# Check the Markdown Files every night
	midnight = datetime.time(hour=00, tzinfo=pytz.timezone('America/Chicago'))
	scrapeJob = job_queue.run_daily(ScrapeReviews,midnight,days=(0,1,2,3,4,5,6))

	# # Run a test job
	# time = datetime.time(hour=13, minute=12, tzinfo=pytz.timezone('America/Chicago'))
	# testJob = job_queue.run_once(ScrapeReviews,30)

	try:
		application.run_polling()
	except:
		logger.warning("An unhandled exception has occured")
	logger.warning("Stopping the application")

if __name__ == '__main__':
	Main()
