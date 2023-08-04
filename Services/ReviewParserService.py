import json
import os
import re
import datetime
import sys

sys.path.append(os.path.dirname(sys.path[0]))
from Objects import (
  Artist,
  Album,
  Review,
  Song
)

SQL_MIN_DATE: datetime.datetime = datetime.datetime.strptime('1753-01-01','%Y-%m-%d')

def ParseReviewMd(path: str) -> Review.Review:
	"""
	Takes a link and then tries to parse the result into a
	Review object
	"""
	title: str = ''
	sortTitle: str | None = None
	artist: Artist.Artist = None
	body: str = ''
	feelingRating: int = 0
	songAvg: float = 0
	trackList: list[Song.Song] = []
	albumArt: str = ''
	genre: list[str] = []
	blurb: str = ''
	listenDate1: datetime.datetime | None = None
	listenDate2: datetime.datetime | None = None
	listenDate3: datetime.datetime | None = None

	bodyFlag: bool = False
	trackFlag: bool = False
	genreFlag: bool = False
	blurbFlag: bool = False

	file = open(path,encoding='utf-8', mode='r')
	lines = file.readlines()

	for line in lines:
		# If the line is empty, skip it
		if line == '' or line == '\n':
			continue
		
		# Grab the album title
		if line[-13:-1] == 'Album Review':
			title = line[2:-14]
			sortTitle = _Sortify(title)
			continue

		# Grab the album art
		if re.match(r'!\[\]\((.*)\)', line):
			cover = re.search(r'!\[\]\((.*)\)',line).group(1)

			artistAlbum = os.path.dirname(path)

			albumArt = os.path.join(artistAlbum,cover)
			continue
		
		# notify that we are in a thoughts block and the next
		# few lines are for it. Also clear the previous flag
		if line[:-1] == '## Thoughts':
			bodyFlag = True
			continue

		# notify that we are in a tack block and the next
		# few lines are for it. Also clear the previous flag
		if line[:-1] == '## Track Ratings':
			bodyFlag = False
			trackFlag = True
			continue

		if trackFlag and re.match(r'^\| (\d+) \| (.*) \| (\d)\\.*',line):
			trackParts = re.search(r'^\| (\d+) \| (.*) \| (\d)\\.*', line)

			song = Song.Song(trackParts.group(1),trackParts.group(2),trackParts.group(3))
			trackList.append(song)
			continue

		# notify that we are in a genre block and the next
		# few lines are for it
		if line[:-1] == '## Genre':
			trackFlag = False
			genreFlag = True
			continue

		if genreFlag:
			
			genre = line[:-1].replace(',',';').split('; ')
			genreFlag = False
			continue

		# Grab the ratings
		if re.match(r'\((\d)\+(\d.*)\)/2.*',line.replace(' ', '')):
			ratings = re.search(r'\((\d)\+(\d.*)\)/2.*',line.replace(' ', ''))

			feelingRating = int(ratings.group(1))
			songAvg = float(ratings.group(2))
			continue

		# Match the dates
		if re.match(r'^\| (\d+) \| (\d+-\d+-\d+) \|',line):
			groups = re.search(r'^\| (\d+) \| (\d+-\d+-\d+) \|',line)
			date: datetime.datetime = datetime.datetime.strptime(groups.group(2),'%Y-%m-%d')

			if groups.group(1) == '1':
				listenDate1 = date
			elif groups.group(1) == '2':
				listenDate2 = date
			elif groups.group(1) == '3':
				listenDate3 = date
			continue

		if line[:-1] == "## Blurb":
			blurbFlag = True
			continue

		if blurbFlag:
			blurb = line[:-1]
			blurbFlag = False
			continue

		# Grab the artist
		if re.match(r'\[.*Artist\]\(.*\)',line):
			link: str = _ParseMdLink(line)[1]
			sortArtist = \
				re.search(r'(.*)_(A|a)rtist_(R|r)eview.md',link).group(1).replace('_', ' ')

			if sortArtist == 'Depeche Mode':
				artistPath: str = os.path.dirname(os.path.dirname(path))
				pathToRemove: str = os.path.dirname(artistPath)
				sortArtist = artistPath.replace(pathToRemove,'').replace('\\','').replace('/','')

			artistName = _UnSortify(sortArtist)

			artist = Artist.Artist(
				artistName,
				sortArtist,
				'',
				[]
			)

			continue

		if bodyFlag:
			body = body + '\n' + line if body else line
			continue

	return Review.Review(
		0,
		artist,
		title,
		sortTitle,
		albumArt,
		body,
		feelingRating,
		songAvg,
		trackList,
		genre,
		blurb,
		'',
		None,
		None,
		listenDate1,
		listenDate2,
		listenDate3
	)

def ParseReviewObj(review: Review.Review) -> list[str]:
	"""
	Takes a review object and then writes it to a markdown file
	"""
	lines: list[str] = []
	parsedTracks: list[str] = []
	parsedDates: list[str] = []

	for track in review.trackList:
		parsedTracks.append(f'| {track.TrackNo} | {track.Name} | {track.Rating}\\5 |\n')

	parsedDates.append(f'| 1 | {review.listenDate1.strftime("%Y-%m-%d")} |\n')
	parsedDates.append(f'| 2 | {review.listenDate2.strftime("%Y-%m-%d")} |\n')
	parsedDates.append(f'| 3 | {review.listenDate3.strftime("%Y-%m-%d") if review.listenDate3 != None else ""} |\n')
	
	lines.append(f'# {review.title} Album Review\n')
	lines.append('\n')
	lines.append('![](Cover.jpg)\n')
	lines.append('\n')
	lines.append('## Thoughts\n')
	lines.append('\n')
	lines.append(f'{review.body}\n')
	lines.append('\n')
	lines.append('## Track Ratings\n')
	lines.append('\n')
	lines.append('| Track Number | Track Title | Rating |\n')
	lines.append('| ------------ | ----------- | ------ |\n')
	lines.append(f'{"".join(parsedTracks)}\n')
	lines.append('## Genre\n')
	lines.append('\n')
	lines.append(f'{"; ".join(review.genre)}')
	lines.append('\n')
	lines.append('## Overall Rating\n')
	lines.append('\n')
	lines.append('(personal rating + Songs avg) / 2 = Rating\n')
	lines.append('\n')
	lines.append(f'({review.feelingRating} + {review.songAvg}) / 2 = {review.OverallRating}\n')
	lines.append('\n')
	lines.append('## Dates\n')
	lines.append('\n')
	lines.append('| Listen # | Date |\n')
	lines.append('|----------|------|\n')
	lines.append(f'{"".join(parsedDates)}\n')
	lines.append('## Blurb\n')
	lines.append('\n')
	lines.append(f'{review.blurb}')
	lines.append('\n')
	lines.append(f'[Return to Artist](../{review.artist.replace(" ", "_")}_Artist_review.md)\n')
	lines.append('\n')
	lines.append('[Return to Index](../../Index.md)\n')
	lines.append('\n')

	return lines

def _ParseMdLink(mdLink: str) -> tuple[str, str]:
	"""
	Takes in a string and then tries to parse it into
	a tuple of the link text and link itself
	"""
	text: str = ''
	link: str = ''

	groups = re.search(r'\[(.*)\]\(\.\./(.*)\)',mdLink)

	if groups:
		text = groups.group(1)
		link = groups.group(2)

	link = link.replace('%20', ' ')

	return text, link

def _Sortify(string: str) -> str:
	"""
	Takes any string and then attempts to normalize it for sorting
	
	ie. The Black Keys -> Black Keys, The
	"""
	if not re.match(r'^(the|an) ',string, re.IGNORECASE):
		return string
	
	article = re.search(r'^(the|an) ',string, re.IGNORECASE).group(1)
	temp = string[len(article)+1:]
	return f'{temp}, {article}'

def _UnSortify(string: str) -> str:
	"""
	Takes any string and then tries to recombine it into normal english

	ie. Black Keys, The -> The Black Keys
	"""
	groups = re.search(r', (the|an)$',string, re.IGNORECASE)
	if not groups:
		return string
	
	article = groups.group(1)
	endlen = len(f', {article}')
	temp = string[:-endlen]
	return f'{article} {temp}'

def Main() -> None:

	filePath: str = '//DEEPTHOUGHT/Media/Music/Bassnectar/Cozza Frenzy/Cozz_Frenzy_Album_Review.md'

	review: Review.Review = ParseReviewMd(filePath)

	reviewStr = ParseReviewObj(review)

	filePath2: str = '//DEEPTHOUGHT/Media/Music/Bassnectar/Cozza Frenzy/Cozz_Frenzy_Album_Review2.md'

	file = open(filePath2,'w')
	file.writelines(reviewStr)

	print('')

if __name__ == '__main__':
	Main()
