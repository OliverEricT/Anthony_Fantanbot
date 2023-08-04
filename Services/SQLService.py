import pyodbc
import sys
import os

sys.path.append(os.path.dirname(sys.path[0]))
from Objects import (
	Artist,
	Review,
	Song
)

class SQLService:
  
	@property
	def Connection(self) -> pyodbc.Connection:
		return self._Connection
	
	@Connection.setter
	def Connection(self,val: pyodbc.Connection) -> None:
		self._Connection = val

	def TestQuery(self) -> str:
		queryStr: str = """
SET NOCOUNT ON;
SELECT * FROM [Music].[dbo].[Reviews]
"""

		cursor: pyodbc.Cursor = self.Connection.cursor()
		cursor.execute(queryStr)

		row: pyodbc.Row = cursor.fetchone()
		while row:
			print(row)
			row = cursor.fetchone()

		return row

	def InsertReview(self, review: Review):
		queryStr: str = """
SET NOCOUNT ON;
EXEC Insert_Review
	@value = ?
"""
		cursor: pyodbc.Cursor = self.Connection.cursor()
		cursor.execute(queryStr)

		row: pyodbc.Row = cursor.fetchone()
		while row:
			print(row)
			row = cursor.fetchone()

	def InsertArtist(self, artist: Artist.Artist) -> bool:
		queryStr: str = """
SET NOCOUNT ON;
EXEC Insert_Artist
	 @ArtistName = ?
	,@SortArtistName = ?
"""
		cursor: pyodbc.Cursor = self.Connection.cursor()
		cursor.execute(queryStr, artist.name, artist.sortName)

		return True

	def SaveReview(self, review: Review.Review) -> int:
		queryStr: str = """
SET NOCOUNT ON;
EXEC [Music].[dbo].[Save_Review]
	 @ReviewId = ?
	,@AlbumTitle = ?
	,@SortName = ?
	,@ArtistName = ?
	,@Body = ?
	,@FeelingRating = ?
	,@AlbumArt = ?
	,@Blurb = ?
	,@PostedDate = ?
	,@ListenDate1 = ?
	,@ListenDate2 = ?
	,@ListenDate3 = ?
"""
		reviewId: int = 0

		cursor: pyodbc.Cursor = self.Connection.cursor()
		tuples = review.Tupleize()
		cursor.execute(queryStr, tuples)

		for row in cursor.fetchall():
			reviewId = row.ReviewId
		
		return reviewId

	def InsertSong(self, reviewId: int, song: Song.Song) -> bool:
		queryStr: str = """
SET NOCOUNT ON;
EXEC [Music].[dbo].[Insert_Song]
	 @ReviewId = ?
	,@TrackNo = ?
	,@SongName = ?
	,@Rating = ?
"""
		success: bool = False

		cursor: pyodbc.Cursor = self.Connection.cursor()
		tuples = song.Tupleize()
		tuples = (reviewId,) + tuples
		cursor.execute(queryStr, tuples)

		for row in cursor.fetchall():
			success = bool(row.Success)
		
		return success

	def InsertGenre(self, reviewId: int, genreName: str) -> bool:
		queryStr: str = """
SET NOCOUNT ON;
EXEC [Music].[dbo].[Insert_ReviewGenre]
	 @ReviewId = ?
	,@GenreName = ?
"""
		success: bool = False

		cursor: pyodbc.Cursor = self.Connection.cursor()
		cursor.execute(queryStr, (reviewId,genreName))

		for row in cursor.fetchall():
			success = bool(row.Success)
		
		return success

	def __init__(self, *argv):
		self.Connection = pyodbc.connect(argv[0], autocommit=True)