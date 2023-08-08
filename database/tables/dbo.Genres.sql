USE [Music]

DROP TABLE IF EXISTS [dbo].[Genres]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

/*######################
    - Debug Commands
        SELECT * FROM [Music].[dbo].[Genres]

######################*/

CREATE TABLE [dbo].[Genres](
     GenreId INT NOT NULL PRIMARY KEY IDENTITY(1,1)
    ,ParentId INT
    ,[Name] VARCHAR(100)
)
GO
