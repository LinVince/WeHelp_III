import mysql.connector
import bcrypt
import jwt
import datetime


# Create the database object
class Database:

	def __init__(self,user,password,database):
		self.user = user        
		self.password = password
		self.database = database

	def __repr__(self):
		return f'<Database: {self.database}>'


	def commit_query(self, query, *arguments):
		# Connect to the database 
		connection = mysql.connector.connect(user=self.user, 
                                        password=self.password,
                                        host='127.0.0.1',
                                        database=self.database
                                        )
		try:
			print (connection.is_connected())
			db_Info = connection.get_server_info()
			print("Connected to MySQL Server version ", db_Info)
			cursor = connection.cursor(buffered=True)
		except:
			return 'Connection Error'
		
		try:
			print (query)
			arguments_tuple = tuple(arguments)
			cursor.execute(query, arguments_tuple)
			connection.commit()
			print (cursor)
			record = cursor.fetchall()
			print (record)
			print("You're connected to database: ", record)
			return record

		except:
			return "Commitment Error"


	def getAttractionInfo(self, attraction_id):
		#Get information from db given attraction_id 
		attraction_id = attraction_id
		query = """SELECT id, name , address, images
						FROM spot
						WHERE id = %s """
		entry = self.commit_query(query, attraction_id)[0]	
		try:
			response = {"attraction_id":entry[0],
						"name":entry[1],
						"address":entry[2],
						"image":"https://" + entry[3].split('https://')[1]}
			return response

		except:
			return "Wrong attraction_id"

	def getBookingInfo(self, email):
		#Get information from db given email
		email = email
		response = {"attraction_id":None,"date":None,"time":None, "price":None}
		try:
			query = """SELECT attraction_id, date_ , time_, price
						FROM booking
						WHERE email = %s """
			entry = self.commit_query(query, email)[0]
			response = {"attraction_id":entry[0],"date":entry[1],"time":entry[2], "price":entry[3]}
			return response

		except:
			return response


	def getUserdbInfo(self, email):
		#Get information from db given email
		email = email
		query = """SELECT id, name, email
						FROM member
						WHERE email = %s """
		
		entry = self.commit_query(query, email)[0]
		response = {"id":entry[0],"name":entry[1],"email":entry[2]}
		return response