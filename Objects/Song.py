class Song:
	"""
	Class to handle the song object
	"""
    
	@property
	def TrackNo(self) -> int:
		return self._TrackNo
	
	@TrackNo.setter
	def TrackNo(self,val: int) -> None:
		self._TrackNo = val

	@property
	def Name(self) -> str:
		return self._Name
	
	@Name.setter
	def Name(self,val: str) -> None:
		self._Name = val

	@property
	def Rating(self) -> int:
		return self._Rating
	
	@Rating.setter
	def Rating(self,val: int) -> None:
		self._Rating = val

	def __init__(self,*argv) -> None:
		if len(argv) == 0:
			self.TrackNo = 0
			self.Name = ''
			self.Rating = 0
		
		elif type(argv[0]) is Song:
			song: Song = argv[0]
			self.TrackNo = song.TrackNo
			self.Name = song.Name
			self.Rating = song.Rating

		else:
			self.TrackNo = argv[0]
			self.Name = argv[1]
			self.Rating = argv[2]

	def __iter__(self):
		return self

	def Tupleize(self) -> tuple[int, str, int]:
		return (
			self.TrackNo,
			self.Name,
			self.Rating
		)

		