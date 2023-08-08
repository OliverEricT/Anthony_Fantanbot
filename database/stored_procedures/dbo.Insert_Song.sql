USE [Music]

DROP PROCEDURE IF EXISTS [dbo].[Insert_Song]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

/*######################
    - Debug Commands
        EXEC [Music].[dbo].[Insert_Song]

######################*/

CREATE PROCEDURE [dbo].[Insert_Song](
     @ReviewId int
    ,@TrackNo int = NULL
    ,@SongName varchar(100) = NULL
    ,@Rating int = NULL
)
AS

    IF EXISTS (
        SELECT 1
        FROM [Music].[dbo].[Songs]
        WHERE SongName = @SongName
        AND ReviewId = @ReviewId
    ) BEGIN
        SELECT 0 AS Success
        RETURN
    END

    INSERT INTO [Music].[dbo].[Songs](
         ReviewId
        ,TrackNo
        ,SongName
        ,Rating
    )
    SELECT
         @ReviewID AS ReviewID
        ,@TrackNo AS TrackNo
        ,@SongName AS SongName
        ,@Rating AS Rating

    SELECT 1 AS Success

GO
