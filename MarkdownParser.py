import json
import os
import re
import Objects

__OpenMediaVault__ = '//OpenMediaVault/Media/Music'

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

def ParseAlbumReview(rev):
    pass

def GetAllAlbumReviews():
    pass


def Main():

    #file = 'Various%20Artists/Aqua%20Teen%20Hunger%20Force%20Colon%20Movie%20Film%20for%20Theaters%20Colon%20the%20Soundtrack/Aqua_Teen_Album_Review.md'

    #file = file.replace('%20',' ')

    #file = open(os.path.join(__OpenMediaVault__,'index.md'),'r')
#
    #lines = file.readlines()
#
    #for line in lines:
    #    print(line.strip())

    ParseIndex()


Main()