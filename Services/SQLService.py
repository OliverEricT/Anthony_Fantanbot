import pyodbc
import sys
import os

sys.path.append(os.path.dirname(sys.path[0]))
from Objects import (
	Review
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
EXEC Insert_Review
	@value = ?
"""
		cursor: pyodbc.Cursor = self.Connection.cursor()
		cursor.execute(queryStr)

		row: pyodbc.Row = cursor.fetchone()
		while row:
			print(row)
			row = cursor.fetchone()

	def InsertArtist(self, artistName: str) -> bool:
		queryStr: str = """
EXEC Insert_Artist
	@ArtistName = ?
"""
		cursor: pyodbc.Cursor = self.Connection.cursor()
		cursor.execute(queryStr, artistName)

		return True

	def SaveReview(self, review: Review.Review) -> None:
		queryStr: str = """
EXEC [Music].[dbo].[Save_Review]
	 @ReviewId = ?
	,@AlbumTitle = ?
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
		
		cursor: pyodbc.Cursor = self.Connection.cursor()
		tuples = review.Tupleize()
		cursor.execute(queryStr, tuples)

		# for row in cursor.fetchall():
		# 	print(row)
		
		pass

	def __init__(self, *argv):
		self.Connection = pyodbc.connect(argv[0], autocommit=True)