USE [Music]

DROP PROCEDURE IF EXISTS [dbo].[Insert_Artist]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

/*######################
    - Debug Commands
        EXEC [Music].[dbo].[Insert_Artist]

######################*/

CREATE PROCEDURE [dbo].[Insert_Artist](
     @ArtistName varchar(100) = NULL
    ,@SortArtistName varchar(100) = NULL
)
AS

    IF @ArtistName IS NULL BEGIN
        SELECT 0 AS Success
        RETURN
    END

    IF EXISTS (
        SELECT 1
        FROM [Music].[dbo].[Artists]
        WHERE [Name] = @ArtistName
    ) BEGIN
        SELECT 0 AS Success
        RETURN
    END

    INSERT INTO [Music].[dbo].[Artists] (
         [Name]
        ,SortName
    )
    SELECT
         @ArtistName AS [Name]
        ,@SortArtistName AS SortName

    SELECT 1 AS Success

GO
