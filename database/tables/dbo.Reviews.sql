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
    ,ArtistId INT NOT NULL
    ,Title VARCHAR(250) NOT NULL
    ,AlbumArt VARCHAR(1000)
    ,Body varchar(max)
    ,FeelingRating int
    ,Blurb varchar(1000)
    ,NumberPosted int
    ,PostedDate datetime
    ,Listen1 datetime
    ,Listen2 datetime
    ,Listen3 datetime
)
GO
