class Artist:

	@property
	def name(self) -> str:
		return self._name
	
	@name.setter
	def name(self,val: str) -> None:
		self._name = val

	@property
	def sortName(self) -> str:
		return self._sortName
	
	@sortName.setter
	def sortName(self,val: str) -> None:
		self._sortName = val

	@property
	def fileLocation(self) -> str:
		return self._fileLocation
	
	@fileLocation.setter
	def fileLocation(self,val: str) -> None:
		self._fileLocation = val

	@property
	def albums(self) -> list:
		return self._albums
	
	@albums.setter
	def albums(self,val: list) -> None:
		self._albums = val

	def __init__(self,*argv):
		if type(argv[0]) is Artist:
			artist = argv[0]
			self.name = artist.name
			self.sortName = artist.sortName
			self.fileLocation = artist.fileLocation
			self.albums = artist.albums
		else:
			self.name = argv[0]
			self.sortName = argv[1]
			self.fileLocation = argv[2]
			self.albums = argv[3]

	def __str__(self):
		return self.name 
