USE [Music]

DROP TABLE IF EXISTS [dbo].[ReviewGenres]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

/*######################
    - Debug Commands
        SELECT * FROM [Music].[dbo].[ReviewGenres]

######################*/

CREATE TABLE [dbo].[ReviewGenres](
     ReviewId INT NOT NULL
    ,GenreId INT NOT NULL
)
GO
