USE [Music]

DROP TABLE IF EXISTS [dbo].[Albums]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

/*######################
    - Debug Commands
        SELECT * FROM [Music].[dbo].[Albums]

######################*/

CREATE TABLE [dbo].[Albums](
     AlbumId INT PRIMARY KEY NOT NULL IDENTITY(1,1)
    ,ArtistId INT NOT NULL
    ,Title VARCHAR(250) NOT NULL
    ,AlbumArt VARCHAR(MAX)
)
GO
