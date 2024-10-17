import datetime
import json
import os
from . import (
  Artist,
	Song
)

class Review:
	"""
	Class to handle the review object.
	"""

	@property
	def id(self) -> int:
		"""
		The integer key for the review
		"""
		return self._id
	
	@id.setter
	def id(self,val: int) -> None:
		self._id = val

	@property
	def artist(self) -> Artist.Artist:
		"""
		the artist name. Potentially change this to a key
		"""
		return self._artist
	
	@artist.setter
	def artist(self,val: Artist.Artist) -> None:
		self._artist = val

	@property
	def title(self) -> str:
		"""
		The album title
		"""
		return self._title
	
	@title.setter
	def title(self,val: str) -> None:
		self._title = val

	@property
	def sortTitle(self) -> str | None:
		return self._sortTitle
	
	@sortTitle.setter
	def sortTitle(self,val: str | None) -> None:
		self._sortTitle = val

	@property
	def albumArt(self) -> str:
		"""
		The link to the album art
		"""
		return self._albumArt
	
	@albumArt.setter
	def albumArt(self,val: str) -> None:
		self._albumArt = val

	@property
	def body(self) -> str:
		"""
		The body of the review
		"""
		return self._body
	
	@body.setter
	def body(self,val: str) -> None:
		self._body = val

	@property
	def feelingRating(self) -> float:
		"""
		The first half of the rating system; in which a score, out of five, is given
		based on the overall feeling the album gives you.
		"""
		return self._feelingRating
	
	@feelingRating.setter
	def feelingRating(self,val: float) -> None:
		self._feelingRating = val

	@property
	def songAvg(self) -> float:
		"""
		The second half of the rating system; in which a score, out of 5, is given for
		each song and then that total is averaged
		"""
		return self._songAvg
	
	@songAvg.setter
	def songAvg(self,val: float) -> None:
		self._songAvg = val

	@property
	def OverallRating(self) -> float:
		"""
		The final review for the album; in which the the average of the
		feeling and song avgs is taken
		"""
		return (self._feelingRating + self._songAvg) / 2
	
	@property
	def blurb(self) -> str:
		"""
		The fun little blurb that gets added to the next up text
		"""
		return self._blurb
	
	@blurb.setter
	def blurb(self,val: str) -> None:
		self._blurb = val

	@property
	def trackList(self) -> list[Song.Song]:
		"""
		The array of song names and ratings that comprise the album
		"""
		return self._trackList
	
	@trackList.setter
	def trackList(self,val: list[Song.Song]) -> None:
		self._trackList = val

	@property
	def genre(self) -> list[str]:
		"""
		The list of genres that comprise the album
		"""
		return self._genre
	
	@genre.setter
	def genre(self,val: list[str]) -> None:
		self._genre = val

	@property
	def nextUp(self) -> str:
		"""
		The fully computed text that get's displayed at the end of the
		previous review.
		"""
		return self._nextUp
	
	@nextUp.setter
	def nextUp(self, val: str) -> None:
		self._nextUp = val

	@property
	def numberPosted(self) -> int | None:
		return self._numberPosted
	
	@numberPosted.setter
	def numberPosted(self,val: int | None) -> None:
		self._numberPosted = val

	@property
	def postedDate(self) -> datetime.datetime | None:
		"""
		The date the review was posted
		"""
		return self._postedDate
	
	@postedDate.setter
	def postedDate(self,val: datetime.datetime | None) -> None:
		self._postedDate = val

	@property
	def listenDate1(self) -> datetime.datetime | None:
		"""
		The date of the first listen
		"""
		return self._listenDate1
	
	@listenDate1.setter
	def listenDate1(self,val: datetime.datetime | None) -> None:
		self._listenDate1 = val

	@property
	def listenDate2(self) -> datetime.datetime | None:
		"""
		The date of the second listen
		"""
		return self._listenDate2
	
	@listenDate2.setter
	def listenDate2(self,val: datetime.datetime | None) -> None:
		self._listenDate2 = val

	@property
	def listenDate3(self) -> datetime.datetime | None:
		"""
		The date of the third listen
		"""
		return self._listenDate3
	
	@listenDate3.setter
	def listenDate3(self,val: datetime.datetime | None) -> None:
		self._listenDate3 = val

	def __init__(self,*argv) -> None:
		"""
		The constructor for the review class. There are three cases for object creation.add()

		1. a Review object is passed in and then copied.

		2. a json is passed in and then parsed into a review

		3. The argv is read and then attempted to parse into the object
		"""
		if len(argv) == 0:
			self.id = 0
			self.artist = None
			self.title = ''
			self.sortTitle = ''
			self.albumArt = ''
			self.body = ''
			self.feelingRating = 0
			self.songAvg = 0
			self.trackList = []
			self.genre = []
			self.blurb = ''
			self.nextUp = ''
			self.numberPosted = 0
			self.postedDate = None
			self.listenDate1 = None
			self.listenDate2 = None
			self.listenDate3 = None

		elif type(argv[0]) is Review:
			rev = argv[0]
			self.id = rev.id
			self.artist = rev.artist
			self.title = rev.title
			self.sortTitle = rev.sortTitle
			self.albumArt = rev.albumArt
			self.body = rev.body
			self.feelingRating = rev.feelingRating
			self.songAvg = rev.songAvg
			self.trackList = rev.trackList
			self.genre = rev.genre
			self.blurb = rev.blurb
			self.nextUp = rev.nextUp
			self.numberPosted = rev.numberPosted
			self.postedDate = rev.postedDate
			self.listenDate1 = rev.listenDate1
			self.listenDate2 = rev.listenDate2
			self.listenDate3 = rev.listenDate3
					
		else:
			self.id = argv[0]
			self.artist = argv[1]
			self.title = argv[2]
			self.sortTitle = argv[3]
			self.albumArt = argv[4]
			self.body = argv[5]
			self.feelingRating = argv[6]
			self.songAvg = argv[7]
			self.trackList = argv[8]
			self.genre = argv[9]
			self.blurb = argv[10]
			self.nextUp = argv[11]
			self.numberPosted = argv[12]
			self.postedDate = argv[13]
			self.listenDate1 = argv[14]
			self.listenDate2 = argv[15]
			self.listenDate3 = argv[16]

	def ToJson(self) -> json:
		"""
		Helper function to change the object into a json
		"""
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)

	def Tupleize(self) -> tuple[int, str, str, str, str,float,str,str,datetime.datetime,datetime.datetime,datetime.datetime]:
		return (
			self.id,
			self.title,
			self.sortTitle,
			self.artist.name,
			self.body,
			self.feelingRating,
			self.albumArt,
			self.blurb,
			self.postedDate,
			self.listenDate1,
			self.listenDate2,
			self.listenDate3
		)

	def __eq__(self,other) -> bool:
		"""
		The equality operator overload for the object
		"""
		return self.__dict__ == other.__dict__

	def __gt__(self,other) -> bool:
		"""
		Helper function to check if a review is greater than the other.
		TBH I have no idea why I have this.
		"""
		if int(self.ID) <= int(other.ID):
				return False
		if (self.Title == '' and other.Title != '') or (self.Title != other.Title):
				return False
		if (self.Artist == '' and other.Artist != '') or (self.Artist != other.Artist):
			return False
		if (self.ReviewBody == '' and other.ReviewBody != '') or (self.ReviewBody != other.ReviewBody):
			return False
		if int(self.AlbumRating) <= int(other.AlbumRating):
			return False
		if int(self.AlbumFeelingRating) <= int(other.AlbumFeelingRating):
			return False
		if float(self.SongAvg) <= float(other.SongAvg):
			return False
		if len(self.TrackList) <= len(other.TrackList):
			return False
		if (self.AlbumArt == '' and other.AlbumArt != '') or (self.AlbumArt != other.AlbumArt):
			return False
		if len(self.Genre) <= len(other.Genre):
			return False
		if (self.Blurb == '' and other.Blurb != '') or (self.Blurb != other.Blurb):
			return False
		if (self.NextUpText == '' and other.NextUpText != '') or (self.NextUpText != other.NextUpText):
			return False
		if (self.DatePosted == '' and other.DatePosted != '') or (self.DatePosted != other.DatePosted):
			return False
		if (self.Listen1 == '' and other.Listen1 != '') or (self.Listen1 != other.Listen1):
			return False
		if (self.Listen2 == '' and other.Listen2 != '') or (self.Listen2 != other.Listen2):
			return False
		if (self.Listen3 == '' and other.Listen3 != '') or (self.Listen3 != other.Listen3):
			return False

		return True

	def __str__(self) -> str:
		"""
		To String overload for the review object
		"""
		genreText = self.genre.join(", ")

		trackList: str = ""
		for pair in self.trackList:
			trackList += "{0} - {1} - {2}/5\n".format(0,pair[0],pair[1])

		text = """
#AlbumReview No. {0}

*Album Title*
{1}

*Album Artist*
{2}

*Genre*
{3}

*Thoughts*
{4}

*Track Ratings*
{5}

*Overall Rating*
({6} + {7}) / 2 = {8}

*NEXT UP*:
{9}"
"""
		return text.format(
			self.id,
			self.title,
			self.artist,
			genreText,
			self.body,
			trackList,
			self.feelingRating,
			self.songAvg,
			self.OverallRating,
			self.nextUp)

	def Merge(self,other):
		"""
		Takes two Review objects and then fills in any null slots in the
		right object with the values in the left.
		"""
		return Review(
			self.id if self.id >= other.id else other.id,
			self.title or other.title or '',
			self.artist or other.artist or '',
			self.body or other.body or '',
			self.feelingRating or other.feelingRating or 0.0,
			self.songAvg or other.songAvg or 0.0,
			self.trackList, # fix this
			self.albumArt, # fix this
			self.genre, # fix this
			self.blurb or other.blurb or '',
			self.nextUp or other.nextUp or '',
			self.datePosted or other.datePosted, # add datetime default
			self.listenDate1 or other.listenDate1,
			self.listenDate2 or other.listenDate2,
			self.listenDate3 or other.listenDate3
		)
