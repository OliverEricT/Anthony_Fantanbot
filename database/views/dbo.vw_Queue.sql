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
    
    WITH SongScores AS (
        SELECT
             s.ReviewId
            ,SUM(s.Rating) AS TotalRatings
            ,COUNT(s.Rating) AS NumberTracks
        FROM [Music].[dbo].[Songs] s
        GROUP BY s.ReviewId
    ),
    MaxNumPosted AS (
        SELECT MAX(r.NumberPosted) + 1 AS MaxNum
        FROM [Music].[dbo].[Reviews] r
    )
    SELECT
         m.MaxNum AS ReviewNumber
        ,r.Title AS AlbumTitle
        ,a.Name AS ArtistName
        ,r.AlbumArt AS AlbumArt
        ,r.Body AS Body
        ,r.FeelingRating AS FeelingRating
        ,s.TotalRatings / s.NumberTracks AS SongAvg
        ,r2.Title + ' by ' + a2.Name + '\n\n' + r2.Blurb AS NextUp
    FROM [Music].[dbo].[Reviews] r
    LEFT JOIN  MaxNumPosted m ON m.MaxNum > 0
    LEFT JOIN [Music].[dbo].[Reviews] r2 ON r.ReviewId + 1 = r2.ReviewId
    INNER JOIN [Music].[dbo].[Artists] a ON r.ArtistId = a.ArtistId
    INNER JOIN [Music].[dbo].[Artists] a2 ON r2.ArtistId = a2.ArtistId
    LEFT JOIN SongScores s ON r.ReviewId = s.ReviewId
    WHERE r.NumberPosted IS NULL
