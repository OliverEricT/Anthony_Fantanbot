import os

class Artist:

    name = ""
    fileLocation = ""
    albums = []

    def __init__(self,*argv):
        if type(argv[0]) is Artist:
            artist = argv[0]
            self.name = artist.name
            self.fileLocation = artist.fileLocation
            self.albums = artist.albums
        else:
            self.name = argv[0]
            self.fileLocation = argv[1]
            self.albums = argv[2]

class Album:

    name = ""
    fileLocation = ""
    prettyName = ""

    def __init__(self,*argv):
        if type(argv[0]) is Album:
            album = argv[0]
            self.name = album.name
            self.fileLocation = album.fileLocation
            self.prettyName = album.prettyName
        else:
            self.name = argv[0]
            self.fileLocation = argv[1]
            self.prettyName = argv[2]
    
    def __str__(self):
        return os.path.join(self.fileLocation,self.name)

class AlbumJson:
    ID = -1,
    Title = ""
    Artist = ""
    ReviewBody = ""
    AlbumRating = 0
    AlbumFeelingRating = 0
    SongAvg = 0
    TrackList = []
    AlbumArt = "\\\\OPENMEDIAVAULT\\Media\\Music\\ \\Cover.jpg"
    Genre = []
    Blurb = ""
    NextUpText = ""
    DatePosted = ""
    Listen1 = ""
    Listen2 = ""
    Listen3 = ""

    def __init__(self,*argv):
        if len(argv) == 0:
            self.ID = -1
            self.Title = ""
            self.Artist = ""
            self.ReviewBody = ""
            self.AlbumRating = 0
            self.AlbumFeelingRating = 0
            self.SongAvg = 0
            self.TrackList = []
            self.AlbumArt = ""
            self.Genre = []
            self.Blurb = ""
            self.NextUpText = ""
            self.DatePosted = ""
            self.Listen1 = ""
            self.Listen2 = ""
            self.Listen3 = ""

        elif type(argv[0]) is AlbumJson:
            rev = argv[0]
            self.ID = rev.ID
            self.Title = rev.Title
            self.Artist = rev.Artist
            self.ReviewBody = rev.ReviewBody
            self.AlbumRating = rev.AlbumRating
            self.AlbumFeelingRating = rev.AlbumFeelingRating
            self.SongAvg = rev.SongAvg
            self.TrackList = rev.TrackList
            self.AlbumArt = rev.AlbumArt
            self.Genre = rev.Genre
            self.Blurb = rev.Blurb
            self.NextUpText = rev.NextUpText
            self.DatePosted = rev.DatePosted
            self.Listen1 = rev.Listen1
            self.Listen2 = rev.Listen2
            self.Listen3 = rev.Listen3

        elif type(argv[0]) is dict:
            rev = argv[0]
            self.ID = rev["ID"]
            self.Title = rev["Title"]
            self.Artist = rev["Artist"]
            self.ReviewBody = rev["ReviewBody"]
            self.AlbumRating = rev["AlbumRating"]
            self.AlbumFeelingRating = rev["AlbumFeelingRating"]
            self.SongAvg = rev["SongAvg"]
            self.TrackList = rev["TrackList"]
            self.AlbumArt = rev["AlbumArt"]
            self.Genre = rev["Genre"]
            self.Blurb = rev["Blurb"]
            self.NextUpText = rev["NextUpText"]
            self.DatePosted = rev["DatePosted"]
            self.Listen1 = rev["Listen1"]
            self.Listen2 = rev["Listen2"]
            self.Listen3 = rev["Listen3"]
            
        else:
            self.ID = argv[0]
            self.Title = argv[1]
            self.Artist = argv[2]
            self.ReviewBody = argv[3]
            self.AlbumRating = argv[4]
            self.AlbumFeelingRating = argv[5]
            self.SongAvg = argv[6]
            self.TrackList = argv[7]
            self.AlbumArt = argv[8]
            self.Genre = argv[9]
            self.Blurb = argv[10]
            self.NextUpText = argv[11]
            self.DatePosted = argv[12]
            self.Listen1 = argv[13]
            self.Listen2 = argv[14]
            self.Listen3 = argv[15]

    def ToJson(self):
        json = {
            "ID": self.ID,
            "Title": self.Title,
            "Artist": self.Artist,
            "ReviewBody": self.ReviewBody,
            "AlbumRating": self.AlbumRating,
            "AlbumFeelingRating": self.AlbumFeelingRating,
            "SongAvg": self.SongAvg,
            "TrackList": self.TrackList,
            "AlbumArt": self.AlbumArt,
            "Genre": self.Genre,
            "Blurb": self.Blurb,
            "NextUpText": self.NextUpText,
            "DatePosted": self.DatePosted,
            "Listen1": self.Listen1,
            "Listen2": self.Listen2,
            "Listen3": self.Listen3
        }

        return json

    def __eq__(self,other):
        if self.ID != other.ID:
            return False
        if self.Title != other.Title:
            return False
        if self.Artist != other.Artist:
        	return False
        if self.ReviewBody != other.ReviewBody:
        	return False
        if self.AlbumRating != other.AlbumRating:
        	return False
        if self.AlbumFeelingRating != other.AlbumFeelingRating:
        	return False
        if self.SongAvg != other.SongAvg:
        	return False
        if self.TrackList != other.TrackList:
        	return False
        if self.AlbumArt != other.AlbumArt:
        	return False
        if self.Genre != other.Genre:
        	return False
        if self.Blurb != other.Blurb:
        	return False
        if self.NextUpText != other.NextUpText:
        	return False
        if self.DatePosted != other.DatePosted:
        	return False
        if self.Listen1 != other.Listen1:
        	return False
        if self.Listen2 != other.Listen2:
        	return False
        if self.Listen3 != other.Listen3:
        	return False

        return True

    def __gt__(self,other):
        if int(self.ID) <= int(other.ID):
            return False
        if (self.Title == '' and other.Title != '') or (self.Title != other.Title):
            return False
        if (self.Artist == '' and other.Artist != '') or (self.Artist != other.Artist):
        	return False
        if (self.ReviewBody == '' and other.ReviewBody != '') or (self.ReviewBody != other.ReviewBody):
        	return False
        if int(self.AlbumRating) <= int(other.AlbumRating):
        	return False
        if int(self.AlbumFeelingRating) <= int(other.AlbumFeelingRating):
        	return False
        if float(self.SongAvg) <= float(other.SongAvg):
        	return False
        if len(self.TrackList) <= len(other.TrackList):
        	return False
        if (self.AlbumArt == '' and other.AlbumArt != '') or (self.AlbumArt != other.AlbumArt):
        	return False
        if len(self.Genre) <= len(other.Genre):
        	return False
        if (self.Blurb == '' and other.Blurb != '') or (self.Blurb != other.Blurb):
        	return False
        if (self.NextUpText == '' and other.NextUpText != '') or (self.NextUpText != other.NextUpText):
        	return False
        if (self.DatePosted == '' and other.DatePosted != '') or (self.DatePosted != other.DatePosted):
        	return False
        if (self.Listen1 == '' and other.Listen1 != '') or (self.Listen1 != other.Listen1):
        	return False
        if (self.Listen2 == '' and other.Listen2 != '') or (self.Listen2 != other.Listen2):
        	return False
        if (self.Listen3 == '' and other.Listen3 != '') or (self.Listen3 != other.Listen3):
        	return False

        return True

    def Merge(self,other):
        merged = AlbumJson()

        if int(self.ID) >= int(other.ID):
            merged.ID = self.ID
        else:
            merged.ID = other.ID

        if self.Title == other.Title or other.Title == '' or other.Title is None:
            merged.Title = self.Title
        else:
            merged.Title = other.Title

        if self.Artist == other.Artist or other.Artist == '' or other.Artist is None:
        	merged.Artist = self.Artist
        else:
            merged.Artist = other.Artist

        if self.ReviewBody == other.ReviewBody or other.ReviewBody == '' or other.ReviewBody is None:
        	merged.ReviewBody = self.ReviewBody
        else:
            merged.ReviewBody = other.ReviewBody

        if int(self.AlbumRating) >= int(other.AlbumRating):
        	merged.AlbumRating = self.AlbumRating
        else:
            merged.AlbumRating = other.AlbumRating

        if int(self.AlbumFeelingRating) >= int(other.AlbumFeelingRating):
        	merged.AlbumFeelingRating = self.AlbumFeelingRating
        else:
            merged.AlbumFeelingRating = other.AlbumFeelingRating

        if float(self.SongAvg) >= float(other.SongAvg):
        	merged.SongAvg = self.SongAvg
        else:
            merged.SongAvg = other.SongAvg

        if len(self.TrackList) >= len(other.TrackList):
        	merged.TrackList = self.TrackList
        else:
            merged.TrackList = other.TrackList

        if self.AlbumArt == other.AlbumArt or other.AlbumArt == '' or other.AlbumArt is None:
        	merged.AlbumArt = self.AlbumArt
        else:
            merged.AlbumArt = other.AlbumArt

        if len(self.Genre) >= len(other.Genre):
        	merged.Genre = self.Genre
        else:
            merged.Genre = other.Genre
        
        if self.Blurb == other.Blurb or other.Blurb == '' or other.Blurb is None:
        	merged.Blurb = self.Blurb
        else:
            merged.Blurb = other.Blurb

        if self.NextUpText == other.NextUpText or other.NextUpText == '' or other.NextUpText is None:
        	merged.NextUpText = self.NextUpText
        else:
            merged.NextUpText = other.NextUpText

        if self.DatePosted == other.DatePosted or other.DatePosted == '' or other.DatePosted is None:
        	merged.DatePosted = self.DatePosted
        else:
            merged.DatePosted = other.DatePosted

        if self.Listen1 == other.Listen1 or other.Listen1 == '' or other.Listen1 is None:
        	merged.Listen1 = self.Listen1
        else:
            merged.Listen1 = other.Listen1
        
        if self.Listen2 == other.Listen2 or other.Listen2 == '' or other.Listen2 is None:
        	merged.Listen2 = self.Listen2
        else:
            merged.Listen2 = other.Listen2

        if self.Listen3 == other.Listen3 or other.Listen3 == '' or other.Listen3 is None:
        	merged.Listen3 = self.Listen3
        else:
            merged.Listen3 = other.Listen3

        return merged
