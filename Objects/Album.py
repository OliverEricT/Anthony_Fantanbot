import os

class Album:
    
	@property
	def name(self) -> str:
		return self._name
	
	@name.setter
	def name(self,val: str) -> None:
		self._name = val
                
	@property
	def fileLocation(self) -> str:
		return self._fileLocation
	
	@fileLocation.setter
	def fileLocation(self,val: str) -> None:
		self._fileLocation = val
                
	@property
	def prettyName(self) -> str:
		return self._prettyName
	
	@prettyName.setter
	def prettyName(self,val: str) -> None:
		self._prettyName = val

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