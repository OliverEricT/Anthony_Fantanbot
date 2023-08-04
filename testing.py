import os
import pathlib
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

reviews: list[str] = []

for path, subdirs, files in os.walk(REVIEWS_FOLDER):
	for name in files:
		if name[-15:].lower() == 'album_review.md':
			review: Review.Review = ReviewParserService.ParseReviewMd(os.path.join(path,name))
			reviews.append(review)

service = SQLService.SQLService(CONNECTION_STRING)

reviewId: int = 0
for review in reviews:
	service.InsertArtist(review.artist)
	reviewId = service.SaveReview(review)
	for song in review.trackList:
		success = service.InsertSong(reviewId,song)
	for genre in review.genre:
		success = service.InsertGenre(reviewId,genre)

#service.TestQuery()
