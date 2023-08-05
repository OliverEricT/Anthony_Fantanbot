import pyodbc
import sys
import os
import datetime

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
	
	def GetNextInQueue(self) -> Review.Review:
		queryStr: str = """
SET NOCOUNT ON;
EXEC [Music].[dbo].[Select_NextInQueue]
"""
		review: Review.Review

		cursor: pyodbc.Cursor = self.Connection.cursor()
		cursor.execute(queryStr)

		for row in cursor.fetchall():
			review = Review.Review(
				row.Id,
				Artist.Artist(row.Artist,'','',[]),
				row.Title,
				'',
				row.AlbumArt,
				row.Body,
				row.FeelingRating,
				row.SongAvg,
				[],
				row.Genre,
				'',
				row.NextUp,
				row.NumberPosted,
				None,
				None,
				None,
				None
			)
		
		cursor.nextset()

		for row in cursor.fetchall():
			review.trackList.append(Song.Song(
				row.TrackNo,
				row.Name,
				row.Rating
			))

		return review
	
	def GetAllReviews(self) -> list[Review.Review]:
		queryStr: str = """
SET NOCOUNT ON;
;WITH TrackAgg AS (
    SELECT
         r.ReviewId
        ,CAST(s.TrackNo AS varchar) + '|' + s.[SongName] + '|' + CAST(s.Rating AS varchar) AS Track
    FROM [Music].[dbo].[Songs] s
    INNER JOIN [Music].[dbo].[Reviews] r ON s.ReviewId = r.ReviewId
    GROUP BY
         r.ReviewId
        ,s.TrackNo
        ,s.SongName
        ,s.Rating
),
ConcatedTracks AS (
    SELECT
         t.ReviewId
        ,STRING_AGG(t.Track,'; ') AS Tracks
    FROM TrackAgg t
    GROUP BY t.ReviewId
),
SongScores AS (
    SELECT
         s.ReviewId
        ,CAST(SUM(s.Rating) AS FLOAT) AS TotalRatings
        ,CAST(COUNT(s.Rating) AS FLOAT) AS NumberTracks
    FROM [Music].[dbo].[Songs] s
    GROUP BY s.ReviewId
),
ConcatedGenres AS (
    SELECT
         r.ReviewId
        ,STRING_AGG(g.Name,'; ') AS Genres
    FROM [Music].[dbo].[Reviews] r
    INNER JOIN [Music].[dbo].[ReviewGenres] rg ON rg.ReviewId = r.ReviewId
    INNER JOIN [Music].[dbo].[Genres] g ON rg.GenreId = g.GenreId
    GROUP BY r.ReviewId
)
SELECT
     r.ReviewId
    ,a.Name AS ArtistName
    ,r.Title
    ,r.SortTitle
    ,r.AlbumArt
    ,r.Body
    ,r.FeelingRating
    ,s.TotalRatings / s.NumberTracks AS SongAvg
    ,t.Tracks
    ,g.Genres
    ,r.Blurb
    ,r.NumberPosted
    ,r.PostedDate
    ,r.Listen1
    ,r.Listen2
    ,r.Listen3
FROM [Music].[dbo].[Reviews] r
INNER JOIN [Music].[dbo].[Artists] a ON r.ArtistId = a.ArtistId
INNER JOIN ConcatedTracks t ON r.ReviewId = t.ReviewId
INNER JOIN ConcatedGenres g ON r.ReviewId = g.ReviewId
INNER JOIN SongScores s ON r.ReviewId = s.ReviewId
"""

		reviews: list[Review.Review] = []

		cursor: pyodbc.Cursor = self.Connection.cursor()
		cursor.execute(queryStr)

		for row in cursor.fetchall():
			genres = row.Genres.split('; ')
			tracks = row.Tracks.split('; ')
			songs: list[Song.Song] = []
			
			for track in tracks:
				splits = track.split('|')
				songs.append(Song.Song(
					splits[0],
					splits[1],
					splits[2]
				))

			reviews.append(Review.Review(
				row.ReviewId,
				Artist.Artist(row.ArtistName,'','',[]),
				row.Title,
				row.SortTitle,
				row.AlbumArt,
				row.Body,
				row.FeelingRating,
				row.SongAvg,
				songs,
				genres,
				row.Blurb,
				'',
				row.NumberPosted,
				row.PostedDate,
				row.Listen1,
				row.Listen2,
				row.Listen3
			))

		return reviews

	def __init__(self, *argv):
		self.Connection = pyodbc.connect(argv[0], autocommit=True)