USE [Music]

DROP PROCEDURE IF EXISTS [dbo].[Save_Review]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

/*######################
	- Debug Commands
		SELECT * FROM [Music].[dbo].[Reviews]

		EXEC [Music].[dbo].[Save_Review]

		EXEC [Music].[dbo].[Save_Review]
			 @ReviewId = NULL
			,@AlbumTitle = 'Test'
			,@ArtistName = 'Test'
			,@Body = ''
			,@FeelingRating = 3
			,@AlbumArt = 'test'
			,@Blurb = 'test'
			,@PostedDate = NULL
			,@ListenDate1 = NULL
			,@ListenDate2 = NULL
			,@ListenDate3 = NULL

######################*/

CREATE PROCEDURE [dbo].[Save_Review](
	 @ReviewId int = NULL
	,@AlbumTitle varchar(250)
	,@ArtistName varchar(100) = NULL
	,@Body varchar(max) = NULL
	,@FeelingRating int = NULL
	,@AlbumArt varchar(max) = NULL
	,@Blurb varchar(1000) = NULL
	,@PostedDate datetime = NULL
	,@ListenDate1 datetime = NULL
	,@ListenDate2 datetime = NULL
	,@ListenDate3 datetime = NULL
)
AS

	DECLARE @ArtistId int = NULL

	SELECT @ArtistId = ArtistId
	FROM [Music].[dbo].[Artists] a
	WHERE a.Name = @ArtistName
			
	IF EXISTS (
		SELECT 1
		FROM [Music].[dbo].[Reviews]
		WHERE ReviewId = @ReviewId
		OR Title = @AlbumTitle
	) BEGIN
		-- Update
		UPDATE r
		SET
			 r.Title = @AlbumTitle
			,r.ArtistId = @ArtistId
			,r.AlbumArt = @AlbumArt
			,r.Body = @Body
			,r.FeelingRating = @FeelingRating
			,r.Blurb = @Blurb
			,r.PostedDate = @PostedDate
			,r.Listen1 = @ListenDate1
			,r.Listen2 = @ListenDate2
			,r.Listen3 = @ListenDate3
		FROM [Music].[dbo].[Reviews] r
		WHERE r.ReviewId = @ReviewId
	END
	ELSE BEGIN
		--Insert
		INSERT INTO [Music].[dbo].[Reviews] (
			 ArtistId
			,Title
			,AlbumArt
			,Body
			,FeelingRating
			,Blurb
			--,NumberPosted
			,PostedDate
			,Listen1
			,Listen2
			,Listen3
		)
		SELECT
			 @ArtistId AS ArtistId
			,@AlbumTitle AS Title
			,@AlbumArt AS AlbumArt
			,@Body AS Body
			,@FeelingRating AS FeelingRating
			,@Blurb AS Blurb
			--,@NumberPosted
			,@PostedDate AS PostedDate
			,@ListenDate1 AS Listen1
			,@ListenDate2 AS Listen2
			,@ListenDate3 AS Listen3
	END

	SELECT ReviewId
	FROM [Music].[dbo].[Reviews]
	WHERE Title = @AlbumTitle
	OR ReviewId = @ReviewId

GO
