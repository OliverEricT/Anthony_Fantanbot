USE [Music]

DROP TABLE IF EXISTS [dbo].[Reviews]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

/*######################
    - Debug Commands
        SELECT * FROM [Music].[dbo].[Reviews]
        
        SELECT 
             r.NumberPosted
            ,*
        FROM [Music].[dbo].[Reviews] r
        WHERE r.NumberPosted IS NOT NULL
        ORDER BY r.NumberPosted

        SELECT * FROM [Music].[dbo].[Reviews] WHERE ISNULL(Blurb,'') = '' ORDER BY NumberPosted

        SELECT * FROM [Music].[dbo].[Reviews] WHERE Title LIKE 'Acid%'

        SELECT * FROM [Music].[dbo].[Reviews] WHERE FeelingRating < 1

######################*/

CREATE TABLE [dbo].[Reviews](
     ReviewId int PRIMARY KEY NOT NULL IDENTITY(1,1)
    ,ArtistId INT NOT NULL
    ,Title VARCHAR(250) NOT NULL
    ,SortTitle VARCHAR(250)
    ,AlbumArt VARCHAR(1000)
    ,Body varchar(max)
    ,FeelingRating int
    ,Blurb varchar(1000) NOT NULL DEFAULT ''
    ,NumberPosted int
    ,PostedDate datetime
    ,Listen1 datetime
    ,Listen2 datetime
    ,Listen3 datetime
)
GO
