USE [Music]

DROP TABLE IF EXISTS [dbo].[Songs]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

/*######################
    - Debug Commands
        SELECT * FROM [Music].[dbo].[Songs] WHERE ReviewId = 298

######################*/

CREATE TABLE [dbo].[Songs](
     SongId int PRIMARY KEY NOT NULL IDENTITY(1,1)
    ,ReviewId int NOT NULL
    ,TrackNo int
    ,SongName varchar(100) NOT NULL
    ,Rating int NOT NULL
)
GO
