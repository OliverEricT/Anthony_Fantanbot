import os
import time
import base64
from dotenv import load_dotenv
from Services import (
	SQLService,
	ReviewParserService
)
from Objects import (
	Review
)

load_dotenv()

CONNECTION_STRING = os.getenv('CONNECTION_STRING')
REVIEWS_FOLDER = os.getenv('REVIEWS_FOLDER')

for path, subdirs, files in os.walk(REVIEWS_FOLDER):
	for name in files:
		
		fullName = os.path.join(path,name)
		if name[-16:].lower() == 'album_review2.md':
			os.remove(fullName)
		if name[-15:].lower() == 'album_review.md':
			reviewFile = open(file=fullName,mode='r')
			try:
				lines = reviewFile.readlines()
			except:
				continue
			part = lines[0][-3:-1]
			reviewFile.close()
			if part == "IP":
				continue
			os.remove(fullName)
			#review: Review.Review = ReviewParserService.ParseReviewMd(fullName)

service = SQLService.SQLService(CONNECTION_STRING)

# reviews = [review for review in reviews if review.artist]

# reviewId: int = 0
# for review in reviews:
# 	service.InsertArtist(review.artist)
# 	reviewId = service.SaveReview(review)
# 	for song in review.trackList:
# 		success = service.InsertSong(reviewId,song)
# 	for genre in review.genre:
# 		success = service.InsertGenre(reviewId,genre)

reviews = service.GetAllReviews()

for review in reviews:
	parentPath = os.path.dirname(review.albumArt)
	formattedTitle = review \
		.title \
		.replace(' ','_') \
		.replace('*','') \
		.replace(':','_') \
		.replace('?','') \
		.replace('/','_') \
		.replace('...','')
	newReviewPath = os.path.join(parentPath,f'{formattedTitle}_Album_Review.md')
	reviewStr = ReviewParserService.ParseReviewObj(review)

	try:
		file = open(newReviewPath,'w')
		file.writelines(reviewStr)
	except:
		print('Fucking Halley Labs and Special Chars:' + newReviewPath)

#service.TestQuery()
