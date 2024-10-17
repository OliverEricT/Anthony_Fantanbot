USE [Music]

DROP PROCEDURE IF EXISTS [dbo].[Select_ReviewById]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

/*######################
    - Debug Commands
        SELECT * FROM Reviews

        EXEC [Music].[dbo].[Select_ReviewById]
            @ReviewId = 265

######################*/

CREATE PROCEDURE [dbo].[Select_ReviewById](
    @ReviewId int = NULL
)
AS
    
    DROP TABLE IF EXISTS #ReviewsWithProposedNumbers
    
    CREATE TABLE #ReviewsWithProposedNumbers(
         ReviewId INT
        ,NumberPosted INT
        ,Title varchar(2500)
        ,Blurb varchar(1000)
        ,ArtistName varchar(100)
    )

    INSERT INTO #ReviewsWithProposedNumbers(
         ReviewId
        ,NumberPosted
        ,Title
        ,Blurb
        ,ArtistName
    )
    SELECT
         ReviewId
        ,NumberPosted
        ,Title
        ,Blurb
        ,a.[Name] AS ArtistName
    FROM [Music].[dbo].[Reviews] r
    INNER JOIN [Music].[dbo].[Artists] a ON r.ArtistId = a.ArtistId

    UPDATE p
    SET NumberPosted = q.ReviewNumber
    FROM #ReviewsWithProposedNumbers p
    INNER JOIN [Music].[dbo].[Queue] q ON p.ReviewId = q.ReviewId
    WHERE p.NumberPosted IS NULL



    ;WITH SongScores AS (
        SELECT
             s.ReviewId
            ,CAST(SUM(s.Rating) AS FLOAT) AS TotalRatings
            ,CAST(COUNT(s.Rating) AS FLOAT) AS NumberTracks
        FROM [Music].[dbo].[Songs] s
        GROUP BY s.ReviewId
    ),
    MaxNumPosted AS (
        SELECT MAX(r.NumberPosted) + 1 AS MaxNum
        FROM [Music].[dbo].[Reviews] r
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
         ISNULL(r.NumberPosted,p.NumberPosted) AS NumberPosted
        ,r.ReviewId AS Id
        ,r.Title AS Title
        ,a.Name AS Artist
        ,r.AlbumArt AS AlbumArt
        ,g.Genres AS Genre
        ,r.Body AS Body
        ,r.FeelingRating AS FeelingRating
        ,ISNULL(s.TotalRatings / s.NumberTracks,0) AS SongAvg
        ,p2.Title + ' by ' + p2.ArtistName + '\n\n' + p2.Blurb AS NextUp
    FROM [Music].[dbo].[Reviews] r
    INNER JOIN #ReviewsWithProposedNumbers p ON r.ReviewId = p.ReviewId
    INNER JOIN #ReviewsWithProposedNumbers p2 ON p.NumberPosted + 1 = p2.NumberPosted
    --INNER JOIN [Music].[dbo].[AlbumArt] aa ON r.ReviewId = aa.ReviewId
    LEFT JOIN ConcatedGenres g ON r.ReviewId = g.ReviewId
    INNER JOIN [Music].[dbo].[Artists] a ON r.ArtistId = a.ArtistId
    LEFT JOIN SongScores s ON r.ReviewId = s.ReviewId
    WHERE r.ReviewId = @ReviewId

    SELECT
         TrackNo AS TrackNo
        ,SongName AS [Name]
        ,Rating AS Rating
    FROM [Music].[dbo].[Songs]
    WHERE ReviewId = @ReviewId

GO
