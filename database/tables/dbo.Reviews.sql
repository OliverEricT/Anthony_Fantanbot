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

######################*/

CREATE TABLE [dbo].[Reviews](
     ReviewId int PRIMARY KEY NOT NULL IDENTITY(1,1)
    ,Title varchar(100) NOT NULL
    ,ArtistId int NOT NULL
    ,Body varchar(max)
    ,FeelingRating int
    ,SongAvg int
    ,AlbumArt varchar(2000)
    ,Blurb varchar(100)
    ,PostedDate datetime
    ,Listen1 datetime
    ,Listen2 datetime
    ,Listen3 datetime
)
GO
