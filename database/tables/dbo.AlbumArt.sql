USE [Music]

DROP TABLE IF EXISTS [dbo].[AlbumArt]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

/*######################
    - Debug Commands
        SELECT * FROM [Music].[dbo].[AlbumArt]

######################*/

CREATE TABLE [dbo].[AlbumArt](
     ReviewId INT NOT NULL
    ,AlbumArt VARBINARY(MAX)
)
GO
