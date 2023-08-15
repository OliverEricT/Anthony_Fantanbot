USE [Music]

DROP PROCEDURE IF EXISTS [dbo].[Select_RatingPercentages]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

/*######################
    - Debug Commands
        EXEC [Music].[dbo].[Select_RatingPercentages]
        EXEC [Music].[dbo].[Select_RatingPercentages] @OnlyPosted = 0

######################*/

CREATE PROCEDURE [dbo].[Select_RatingPercentages](
    @OnlyPosted BIT = 1
)
AS

    DECLARE @TotalAlbums int

    DROP TABLE IF EXISTS #ReviewFilter

    CREATE TABLE #ReviewFilter (
        ReviewID int
    )

    IF @OnlyPosted = 1 BEGIN
        INSERT INTO #ReviewFilter(
            ReviewId
        )
        SELECT
            ReviewId
        FROM [Music].[dbo].[Reviews]
        WHERE NumberPosted IS NOT NULL
    END
    ELSE BEGIN
        INSERT INTO #ReviewFilter(
            ReviewId
        )
        SELECT
            ReviewId
        FROM [Music].[dbo].[Reviews]
    END

    DROP TABLE IF EXISTS #RatedAlbums

    ;WITH SongAvgs AS (
        SELECT
            s.ReviewId
            ,ROUND(CAST(SUM(s.Rating) AS FLOAT) / CAST(COUNT(s.SongId) AS FLOAT),0) AS SongAvg
        FROM [Music].[dbo].[Songs] s
        GROUP BY s.ReviewId
    )
    SELECT
        r.ReviewId
        ,ROUND((r.FeelingRating + s.SongAvg) / 2,0) AS AlbumRating
    INTO #RatedAlbums
    FROM [Music].[dbo].[Reviews] r
    INNER JOIN #ReviewFilter f ON r.ReviewId = f.ReviewId
    INNER JOIN SongAvgs s ON r.ReviewId = s.ReviewId

    SELECT @TotalAlbums = COUNT(ReviewId) FROM #RatedAlbums

    DROP TABLE IF EXISTS #NumberOfAlbumsByScore

    SELECT
        AlbumRating
        ,COUNT(AlbumRating) AS NumberOfAlbums
    INTO #NumberOfAlbumsByScore
    FROM #RatedAlbums
    GROUP BY AlbumRating

    SELECT
        AlbumRating
        ,ROUND((CAST(NumberOfAlbums AS FLOAT) / CAST(@TotalAlbums AS FLOAT)) * 100,2) AS PercentageOfAlbums
    FROM #NumberOfAlbumsByScore

    DROP TABLE IF EXISTS #RatedAlbums
    DROP TABLE IF EXISTS #NumberOfAlbumsByScore
    DROP TABLE IF EXISTS #ReviewFilter

GO
