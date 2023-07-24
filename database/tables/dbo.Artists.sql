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

######################*/

CREATE TABLE [dbo].[Artists](
     ArtistId int PRIMARY KEY NOT NULL IDENTITY(1,1)
    ,[Name] varchar(100) NOT NULL
)
GO
