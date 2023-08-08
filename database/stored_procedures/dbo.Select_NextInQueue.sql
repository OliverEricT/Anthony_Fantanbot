USE [Music]

DROP PROCEDURE IF EXISTS [dbo].[Select_NextInQueue]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

/*######################
    - Debug Commands
        EXEC [Music].[dbo].[Select_NextInQueue]
            @DebugMode = 1

######################*/

CREATE PROCEDURE [dbo].[Select_NextInQueue](
    @DebugMode bit = 0
)
AS

    DECLARE @ReviewId int
    DECLARE @MinReviewNumber int

    SELECT @MinReviewNumber = MIN(ReviewNumber)
    FROM [Music].[dbo].[Queue]

    SELECT @ReviewId = ReviewId
    FROM [Music].[dbo].[Queue]
    WHERE ReviewNumber = @MinReviewNumber

    SELECT TOP 1
         q.ReviewNumber AS NumberPosted
        ,q.AlbumTitle AS Title
        ,q.ArtistName AS Artist
        ,aa.AlbumArt AS AlbumArt
        ,q.Genres AS Genre
        ,q.Body AS Body
        ,q.FeelingRating AS FeelingRating
        ,q.SongAvg AS SongAvg
        ,q.NextUp AS NextUp
        ,q.ReviewId AS Id
    FROM [Music].[dbo].[Queue] q
    INNER JOIN [Music].[dbo].[AlbumArt] aa ON q.ReviewId = aa.ReviewId

    IF @DebugMode = 0 BEGIN
        UPDATE r
        SET
             r.NumberPosted  = @MinReviewNumber
            ,r.PostedDate = GETDATE()
        FROM [Music].[dbo].[Reviews] r
        WHERE r.ReviewId = @ReviewId
    END

    SELECT
         TrackNo AS TrackNo
        ,SongName AS [Name]
        ,Rating AS Rating
    FROM [Music].[dbo].[Songs]
    WHERE ReviewId = @ReviewId

GO
