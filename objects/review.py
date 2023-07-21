import datetime
import json
import os

class Review:

	@property
	def id(self) -> int:
		return self._id
	
	@id.setter
	def id(self,val: int) -> None:
		self._id = val

	@property
	def title(self) -> str:
		return self._title
	
	@title.setter
	def title(self,val: str) -> None:
		self._title = val

	@property
	def artist(self) -> str:
		return self._artist
	
	@artist.setter
	def artist(self,val: str) -> None:
		self._artist = val

	@property
	def body(self) -> str:
		return self._body
	
	@body.setter
	def body(self,val: str) -> None:
		self._body = val

	@property
	def feelingRating(self) -> float:
		return self._feelingRating
	
	@feelingRating.setter
	def feelingRating(self,val: float) -> None:
		self._feelingRating = val

	@property
	def songAvg(self) -> float:
		return self._songAvg
	
	@songAvg.setter
	def songAvg(self,val: float) -> None:
		self._songAvg = val

	@property
	def OverralRating(self) -> float:
		return (self._feelingRating * self._songAvg) / 2
	
	@property
	def trackList(self) -> list(str):
		return self._trackList
	
	@trackList.setter
	def trackList(self,val: list(str)) -> None:
		self._trackList = val

	@property
	def albumArt(self) -> str:
		return os.path.join("\\\\Deepthought\\Media\\Music\\",self._albumArt,"Cover.jpg") 
	
	@albumArt.setter
	def albumArt(self,val: str) -> None:
		self._albumArt = val

	@property
	def genre(self) -> list(str):
		return self._genre
	
	@genre.setter
	def genre(self,val: list(str)) -> None:
		self._genre = val

	@property
	def blurb(self) -> str:
		return self._blurb
	
	@blurb.setter
	def blurb(self,val: str) -> None:
		self._blurb = val

	@property
	def nextUp(self) -> str:
		return self._nextUp
	
	@nextUp.setter
	def nextUp(self,val: str) -> None:
		self._nextUp = val

	@property
	def posted(self) -> datetime:
		return self._posted
	
	@posted.setter
	def postedDate(self,val: datetime) -> None:
		self._posted = val

	@property
	def listenDate1(self) -> datetime:
		return self._listenDate1
	
	@listenDate1.setter
	def listenDate1(self,val: datetime) -> None:
		self._listenDate1 = val

	@property
	def listenDate2(self) -> datetime:
		return self._listenDate2
	
	@listenDate2.setter
	def listenDate2(self,val: datetime) -> None:
		self._listenDate2 = val

	@property
	def listenDate3(self) -> datetime:
		return self._listenDate3
	
	@listenDate3.setter
	def listenDate3(self,val: datetime) -> None:
		self._listenDate3 = val

	def __init__(self,*argv) -> None:
		if len(argv) == 0:
			self.id = -1
			self.title = ""
			self.artist = ""
			self.body = ""
			self.feelingRating = 0
			self.songAvg = 0
			self.trackList = []
			self.albumArt = ""
			self.genre = []
			self.blurb = ""
			self.nextUp = ""
			self.datePosted = datetime.now()
			self.listenDate1 = ""
			self.listenDate2 = ""
			self.listenDate3 = ""

		elif type(argv[0]) is Review:
			rev = argv[0]
			self.id = rev.id
			self.title = rev.title
			self.artist = rev.artist
			self.body = rev.body
			self.feelingRating = rev.feelingRating
			self.songAvg = rev.songAvg
			self.trackList = rev.trackList
			self.albumArt = rev.albumArt
			self.genre = rev.genre
			self.blurb = rev.blurb
			self.nextUp = rev.nextUp
			self.datePosted = rev.datePosted
			self.listenDate1 = rev.listenDate1
			self.listenDate2 = rev.listenDate2
			self.listenDate3 = rev.listenDate3

		elif type(argv[0]) is json:
			rev = argv[0]
			self.id = rev['id']
			self.title = rev['title']
			self.artist = rev['artist']
			self.body = rev['body']
			self.feelingRating = rev['feelingRating']
			self.songAvg = rev['songAvg']
			self.trackList = rev['trackList']
			self.albumArt = rev['albumArt']
			self.genre = rev['genre']
			self.blurb = rev['blurb']
			self.nextUp = rev['nextUp']
			self.datePosted = rev['datePosted']
			self.listenDate1 = rev['listenDate1']
			self.listenDate2 = rev['listenDate2']
			self.listenDate3 = rev['listenDate3']
					
		else:
		self.id = argv[0]
		self.title = argv[1]
		self.artist = argv[2]
		self.body = argv[3]
		self.feelingRating = argv[4]
		self.songAvg = argv[5]
		self.trackList = argv[6]
		self.albumArt = argv[7]
		self.genre = argv[8]
		self.blurb = argv[9]
		self.nextUp = argv[10]
		self.datePosted = argv[11]
		self.listenDate1 = argv[12]
		self.listenDate2 = argv[13]
		self.listenDate3 = argv[14]

	def ToJson(self) -> json:
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)

	def __eq__(self,other) -> bool:
		return self.__dict__ == other.__dict__

	def __gt__(self,other) -> bool:
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

	def Merge(self,other: Review) -> Review:
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
