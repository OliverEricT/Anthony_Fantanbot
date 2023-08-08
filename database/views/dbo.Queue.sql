USE [Music]

DROP VIEW IF EXISTS [dbo].[Queue]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

/*######################
    - Debug Commands
        SELECT * FROM [Music].[dbo].[Queue]

######################*/

CREATE VIEW [dbo].[Queue]
AS
    
    WITH FilteredReviews AS (
        SELECT
            r.ReviewId
        FROM [Music].[dbo].[Reviews] r
        WHERE r.NumberPosted IS NULL
    ),
    SongScores AS (
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
    SortedFilteredReviews AS (
        SELECT
             m.MaxNum - 1 + ROW_NUMBER() OVER(ORDER BY r.SortTitle) AS ReviewNumber
            ,r.ReviewId
            ,r.Title
            ,r.ArtistId
            ,r.Blurb
        FROM [Music].[dbo].[Reviews] r
        INNER JOIN FilteredReviews fr ON r.ReviewId = fr.ReviewId
        LEFT JOIN MaxNumPosted m ON m.MaxNum > 0
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
         sf.ReviewNumber AS ReviewNumber
        ,r.ReviewId AS ReviewId
        ,r.Title AS AlbumTitle
        ,a.Name AS ArtistName
        ,g.Genres AS Genres
        ,r.Body AS Body
        ,r.FeelingRating AS FeelingRating
        ,s.TotalRatings / s.NumberTracks AS SongAvg
        ,sf2.Title + ' by ' + a2.Name + '\n\n' + sf2.Blurb AS NextUp
        ,ROW_NUMBER() OVER(ORDER BY r.SortTitle) AS ForcedSort
    FROM [Music].[dbo].[Reviews] r
    INNER JOIN SortedFilteredReviews sf ON r.ReviewId = sf.ReviewId
    LEFT JOIN ConcatedGenres g ON r.ReviewId = g.ReviewId
    LEFT JOIN SortedFilteredReviews sf2 ON sf.ReviewNumber + 1 = sf2.ReviewNumber
    INNER JOIN [Music].[dbo].[Artists] a ON r.ArtistId = a.ArtistId
    INNER JOIN [Music].[dbo].[Artists] a2 ON sf2.ArtistId = a2.ArtistId
    LEFT JOIN SongScores s ON r.ReviewId = s.ReviewId
