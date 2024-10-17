USE [Music]

DROP TABLE IF EXISTS [dbo].[Artists]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

/*######################
    - Debug Commands
        SELECT * FROM [Music].[dbo].[Artists]

        SELECT * FROM [Music].[dbo].[Artists] WHERE ArtistId = 114

######################*/

CREATE TABLE [dbo].[Artists](
     ArtistId int PRIMARY KEY NOT NULL IDENTITY(1,1)
    ,[Name] varchar(100) NOT NULL
    ,SortName varchar(100)
)
GO
