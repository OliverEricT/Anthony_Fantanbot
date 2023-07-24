USE [Music]

DROP TABLE IF EXISTS [dbo].[AlbumGenres]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

/*######################
    - Debug Commands
        SELECT * FROM [Music].[dbo].[AlbumGenres]

######################*/

CREATE TABLE [dbo].[AlbumGenres](
     AlbumId int NOT NULL
    ,Genre varchar(100) NOT NULL
)
GO
