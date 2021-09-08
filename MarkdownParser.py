import json
import os
import re
import Objects

__OpenMediaVault__ = '//OpenMediaVault/Media/Music'
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
__Queue__ = os.path.join(__location__,'Queue.json')
__Posted__ = os.path.join(__location__,'Posted_Reviews.json')

def ParseIndex():
    file = open(os.path.join(__OpenMediaVault__,'index.md'),'r')

    lines = file.readlines()

    start = False

    artists = []
    artist = None
    album = None

    for line in lines:

        if line[0:8] == '## Index':
            start = True

        if start:
            if line[0] == '-':
                if artist != None:
                    artists.append(artist)

                tup = ParseMdLink(line)
                artist = Objects.Artist(tup[0],os.path.join(__OpenMediaVault__,tup[1]),[])
                print('\n\nArtist Name: {0}\nArtist Location: {1}\n'.format(artist.name,artist.fileLocation))
            elif line[0:3] == '  -':
                tup = ParseMdLink(line)
                album = Objects.Album(tup[0],os.path.join(__OpenMediaVault__,tup[1]))
                print('Album Name: {0}\nAlbum Location: {1}'.format(album.name,album.fileLocation))
                artist.albums.append(album)

    return artists

def ParseMdLink(mdLink):
    text = []
    link = []

    p1 = ''
    p2 = ''

    for i in range(0,len(mdLink)):
        if mdLink[i] == '[':
            j = i + 1
            while mdLink[j] != ']':
                text.append(mdLink[j])
                j += 1

        if mdLink[i] == '(':
            j = i + 1
            while mdLink[j] != ')':
                link.append(mdLink[j])
                j += 1

    p1 = p1.join(text)
    p2 = p2.join(link)

    p2 = p2.replace('%20',' ')

    return p1, p2

def CreateAlbumReviewMDFromJson(album):
    lines = []

    lines.append('# {0} Album Review\n'.format(album.Title))
    lines.append('\n')

    cover = re.search(r'//.*/(.*)',album.AlbumArt).group(1)

    lines.append('![]({0})\n'.format(cover))
    lines.append('\n')
    lines.append('## Thoughts\n')
    lines.append('\n')
    lines.append(album.ReviewBody)
    lines.append('\n')
    lines.append('## Track Ratings\n')
    lines.append('\n')
    lines.append('| Track Number | Track Title | Rating |\n')
    lines.append('| ------------ | ----------- | ------ |\n')
    
    counter = 1
    for i in range(0,len(album.TrackList),2):
        lines.append('| {0:02d} | {1} | {2}\\5 |\n'.format(counter,album.TrackList[i],album.TrackList[i+1]))
        counter += 1
    lines.append('\n')

    lines.append('## Genre\n')
    lines.append('\n')

    lineTemp = ''
    for i in range(0,len(album.Genre)):
        lineTemp += album.genre[i] + ', '
        counter += 1
    lines.append(lineTemp[:-2] + '\n')
    lines.append('\n')

    lines.append('## Overall Rating\n')
    lines.append('\n')
    lines.append('(personal rating + Songs avg) / 2 = Rating\n')
    lines.append('\n')

    sAvg = (int(album.AlbumFeelingRating) + float(album.SongAvg)) / 2

    lines.append('({0} + {1}) / 2 = {2} = {3}\n'.format(album.AlbumFeelingRating,album.SongAvg,sAvg,album.AlbumRating))
    lines.append('\n')

    lines.append('## Dates\n')
    lines.append('\n')
    lines.append('| Listen # | Date |\n')
    lines.append('| -------- | ---- |\n')
    lines.append('| 1 | {0} |\n'.format(album.Listen1))
    lines.append('| 2 | {0} |\n'.format(album.Listen2))
    lines.append('| 3 | {0} |\n'.format(album.Listen3))
    lines.append('\n')

    lines.append("## Blurb\n")
    lines.append('\n')
    lines.append('{0}\n'.format(album.Blurb))
    lines.append('\n')

    lines.append('[Return to Artist](../{0}_Artist_review.md)\n'.format(album.Artist.replace(' ','_')))
    lines.append('[Return to Index](../../Index.md)\n')

    return lines

def ParseAlbumReview(rev,albumObj):

    revObj = Objects.AlbumJson()
    
    for i in range(0,len(rev)):
        line = rev[i]
        if line[-13:-1] == 'Album Review':
            revObj.Title = line[2:-14]

            cover = re.findall(r'\(.*\)',rev[i+2])[0]
            cover = cover[1:len(cover)-1]

            artistAlbum = os.path.dirname(albumObj.fileLocation)

            revObj.AlbumArt = os.path.join(artistAlbum,cover)
        
        elif line[:-1] == '## Thoughts':
            revObj.ReviewBody = rev[i+2].replace('\n','')

        elif line[:-1] == '## Track Ratings':
            end = False
            j = i + 4
            tracklist = []
            while not end:
                if re.match(r'^\| \d\d \| (.*) \| (\d)(\\|/)\d \|$',rev[j]):
                    track = re.search(r'^\| \d\d \| (.*) \| (\d)(\\|/)\d \|$',rev[j])
                    trackName = "{0}".format(track.group(1))
                    trackRating = int(track.group(2))
                    tracklist.append(trackName)
                    tracklist.append(trackRating)
                    j += 1
                else:
                    end = True
            
            revObj.TrackList = tracklist

        elif line[:-1] == '## Genre':
            genres = []
            genreRaw = rev[i+2]

            groups = re.split(r', |; ',genreRaw)

            for group in groups:
                    genres.append(group.replace('\n',''))

            revObj.Genre = genres


        elif line[:-1] == '## Overall Rating':
            temp = rev[i+4].replace(' ','')

            if temp != '(+)/2=\n':

                ratings = re.search(r'\((\d)\+(\d(|\.\d+))\)/2=(.*)',temp)

                revObj.AlbumFeelingRating = ratings.group(1)
                revObj.SongAvg = ratings.group(2)

                revObj.AlbumRating = re.findall(r'\d$',ratings.group(4))[0]


        elif line[:-1] == '## Dates':
            end = False
            j = i + 4
            datelist = []
            while not end:
                if re.match(r'\| \d \| (.*) \|$',rev[j]):
                    date = re.search(r'\| \d \| (.*) \|$',rev[j])
                    date = date.group(1)
                    datelist.append(date)
                    j += 1
                else:
                    end = True

            revObj.Listen1 = datelist[0]
            revObj.Listen2 = datelist[1]
            revObj.Listen3 = datelist[2]

        elif line[:-1] == '## Blurb':
            revObj.Blurb = rev[i+2].replace('\n','')

        elif re.match(r'\[.*Artist\]\(.*\)',line):
            tup = ParseMdLink(line)
            a = re.search(r'../(.*)_(A|a)rtist_(R|r)eview.md',tup[1])
            a = a.group(1)
            a = a.replace('_',' ')

            if a == 'Depeche Mode':
                artist = os.path.dirname(os.path.dirname(albumObj.fileLocation))
                pathToRemove = os.path.dirname(artist)
                a = artist.replace(pathToRemove,'')
                a = a.replace('\\','')
                a = a.replace('/','')

            revObj.Artist = a

    return revObj

def GetAllAlbumReviews():
    pass

def PopulateIndex():
    pass

def PopulateQueue():
    pass

def GetAllMDFiles():
    mdFiles = []

    for pathName, dirs, files in os.walk(__OpenMediaVault__):
        for f in files:
            if 'Album_Review.md' in f:
                mdFiles.append(os.path.join(pathName,f))

    return mdFiles

def GetAllMDFilesNotInJson():
    mdFiles = []

    for pathName, dirs, files in os.walk(__OpenMediaVault__):
        for f in files:
            if 'Album_Review.md' in f:
                if not CheckIfInQueue(pathName) and not CheckIfInPosted(pathName):
                    pName = FormatName(f)
                    fileLoc = os.path.join(pathName,f)
                    mdFiles.append(Objects.Album(f,fileLoc,pName))

    return mdFiles

def CheckIfInQueue(path):
    queueF = open(__Queue__,'r')
    queueRaw = json.load(queueF)
    queue = queueRaw["Queue"]
    
    for j in queue:
        jPath = os.path.dirname(j["AlbumArt"])
        jPath = jPath.lower().replace('\\','/')
        tPath = path.lower().replace('\\','/')
        if jPath == tPath:
            return True

    return False

def CheckIfInPosted(path):
    postedF = open(__Posted__,'r')
    postedRaw = json.load(postedF)
    posted = postedRaw["Completed"]
    
    for j in posted:
        jPath = os.path.dirname(j["AlbumArt"])
        jPath = jPath.lower().replace('\\','/')
        tPath = path.lower().replace('\\','/')
        if jPath == tPath:
            return True

    return False

def FormatName(str):
    tmp = str.lower()
    tmp = tmp.replace('_album_review.md','')
    tmp = tmp.replace('_',' ')

    if re.match(r'^the ',tmp):
        tmp = re.split(r'^the ',tmp)[1]

    return tmp

def StringNoArticle(str):
    if re.match(r'^the ',str.lower()):
        newStr = re.split(r'^the ',str.lower())[1]
    else:
        newStr = str
    return newStr

def AlbumListToJson(lst):
    jsons = []
    for item in lst:
        jsons.append(AlbumToJson(item))

    return jsons

def AlbumToJson(album):
    file = open(album.fileLocation,'r')
    lines = file.readlines()
    rev = ParseAlbumReview(lines,album)
    return rev

def AddListToQueue(lst):
    with open(__Queue__,'r') as file:
        queue = json.load(file)

    for item in lst:
        queue["Queue"].append(item.ToJson())

    with open(__Queue__,'w') as file:
        json.dump(queue,file,indent=2)

def AddToQueue(review):
    with open(__Queue__,'r') as file:
        queue = json.load(file)

    queue["Queue"].append(review)

    with open(__Queue,'w') as file:
        json.dump(queue,file,indent=2)

def Main():

    #fileLoc = 'Various%20Artists/Aqua%20Teen%20Hunger%20Force%20Colon%20Movie%20Film%20for%20Theaters%20Colon%20the%20Soundtrack/Aqua_Teen_Album_Review.md'

    #fileLoc = fileLoc.replace('%20',' ')

    #file = open(os.path.join(__OpenMediaVault__,fileLoc),'r')

    #lines = file.readlines()

    #rev = ParseAlbumReview(lines,fileLoc)

    #artist = Objects.Artist('Various Artists','Various%20Artists',[])

    #rev.Artist = artist.name

    #lines = CreateAlbumReviewMDFromJson(rev)

    #file2 = open(os.path.join(__OpenMediaVault__,'test.md'),'w')

    #for line in lines:
    #    file2.write(line)

    #mdFiles = GetAllMDFilesNotInJson()

    #mdFiles.sort(key=lambda x: x.prettyName)

    #rev = AlbumToJson(mdFiles[0])

    #jsons = AlbumListToJson(mdFiles)

    #AddListToQueue(jsons)

    fileLoc = '\\\\OPENMEDIAVAULT\\Media\\Music\\SonicPicnic\\Awesomenauts Original Soundtrack\\Awesomenauts_OST_Album_Review.md'

    albFile = Objects.Album('',fileLoc,'')

    file = open(albFile.fileLocation,'r')

    lines = file.readlines()

    rev = ParseAlbumReview(lines,albFile)

    albFile = rev

    with open(os.path.join(__Queue__),'r') as file:
        queue = json.load(file)
        queueShort = queue["Queue"]

    albQ = Objects.AlbumJson(queueShort[2])

    rev.Merge(albQ)

    print('')

    #ParseIndex()


Main()