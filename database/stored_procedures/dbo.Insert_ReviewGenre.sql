USE [Music]

DROP PROCEDURE IF EXISTS [dbo].[Insert_ReviewGenre]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

/*######################
    - Debug Commands
        EXEC [Music].[dbo].[Insert_ReviewGenre]

######################*/

CREATE PROCEDURE [dbo].[Insert_ReviewGenre](
     @ReviewId INT
    ,@GenreName varchar(100)
)
AS

    DECLARE @GenreId INT

    IF NOT EXISTS (
        SELECT 1
        FROM [Music].[dbo].[Genres]
        WHERE [Name] = @GenreName
    ) BEGIN
       INSERT INTO [Music].[dbo].[Genres] (
            [Name]
        )
        SELECT
            @GenreName AS [Name] 
    END

    SELECT @GenreId = GenreId
    FROM [Music].[dbo].[Genres]
    WHERE [Name] = @GenreName

    IF EXISTS (
        SELECT 1
        FROM [Music].[dbo].[ReviewGenres]
        WHERE ReviewId = @ReviewId
        AND GenreId = @GenreId
    ) BEGIN
        SELECT 0 AS Success
        RETURN
    END

    INSERT INTO [Music].[dbo].[ReviewGenres](
         ReviewId
        ,GenreId
    )
    SELECT
         @ReviewId AS ReviewID
        ,@GenreId AS GenreId

    SELECT 1 AS Success

GO
