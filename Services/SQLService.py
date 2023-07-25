import pyodbc
from Objects import (
	Review
)

class SQLService:
  
	@property
	def Connection(self) -> pyodbc.Connection:
		return self._Connection
	
	@Connection.setter
	def Connection(self,val: pyodbc.Connection) -> None:
		self._Connection = val

	def InsertReview(self, review: Review):
		queryStr: str = """
EXEC Insert_Review
	@value = ?
"""
		cursor: pyodbc.Cursor = self.Connection.cursor()
		cursor.execute(queryStr)

		row: pyodbc.Row = cursor.fetchone()
		while row:
			print(row)
			row = cursor.fetchone()

	def __init__(self, *argv):
		self.Connection = argv[0]