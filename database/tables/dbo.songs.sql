USE [Music]

DROP TABLE IF EXISTS [dbo].[Songs]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

/*######################
    - Debug Commands
        SELECT * FROM [Music].[dbo].[Songs]

######################*/

CREATE TABLE [dbo].[Songs](
     SongId int PRIMARY KEY NOT NULL IDENTITY(1,1)
    ,AlbumId int NOT NULL
    ,SongName varchar(100) NOT NULL
    ,SongRating int NOT NULL
)
GO
