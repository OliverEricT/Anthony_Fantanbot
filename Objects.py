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

    def __init__(self,*argv):
        if type(argv[0]) is Album:
            album = argv[0]
            self.name = album.name
            self.fileLocation = album.fileLocation
        else:
            self.name = argv[0]
            self.fileLocation = argv[1]

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
        if type(argv[0]) is AlbumJson:
            rev = argv[0]
            self.id = rev.ID
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
            
        else:
            self.id = argv[0]
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
            "id": self.ID,
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
