from flask import *
import mysql.connector
import bcrypt
import jwt
import datetime

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.secret_key = "Thisismysecretkey000000111111"

# Create the database object
class Database:

    def __init__(self,user,password,database):
        self.user = user        
        self.password = password
        self.database = database

    def __repr__(self):
        return f'<Database: {self.database}>'

mydb = Database('root','811223','taipei_tour')

def getUserdbInfo(email):
	# Connect to the database 
	connection = mysql.connector.connect(user=mydb.user, 
                                        password=mydb.password,
                                        host='127.0.0.1',
                                        database=mydb.database
                                        )
	try:    
	    print (connection.is_connected())
	    db_Info = connection.get_server_info()
	    print("Connected to MySQL Server version ", db_Info)
	    cursor = connection.cursor(buffered=True)
	    cursor.execute("select database();")
	    record = cursor.fetchone()
	    print("You're connected to database: ", record)

	except:
		error['message'] = '資料庫連接錯誤'
		return (error)

	#Get information from db given email
	email = email
	query = """SELECT id, name, email
					FROM member
					WHERE email = %s """
	cursor.execute(query, (email,))
	entry = cursor.fetchone()
	response = {"id":entry[0],"name":entry[1],"email":entry[2]}
	return response


def getBookingInfo(email):
	# Connect to the database 
	connection = mysql.connector.connect(user=mydb.user, 
                                        password=mydb.password,
                                        host='127.0.0.1',
                                        database=mydb.database
                                        )
	try:    
	    print (connection.is_connected())
	    db_Info = connection.get_server_info()
	    print("Connected to MySQL Server version ", db_Info)
	    cursor = connection.cursor(buffered=True)
	    cursor.execute("select database();")
	    record = cursor.fetchone()
	    print("You're connected to database: ", record)

	except:
		error['message'] = '資料庫連接錯誤'
		return (error)

	#Get information from db given email
	email = email
	response = {"attraction_id":None,"date":None,"time":None, "price":None}
	try:
		query = """SELECT attraction_id, date_ , time_, price
						FROM booking
						WHERE email = %s """
		cursor.execute(query, (email,))
		entry = cursor.fetchall()[0]
		response = {"attraction_id":entry[0],"date":entry[1],"time":entry[2], "price":entry[3]}
		return response

	except:
		return response

def getAttractionInfo(attraction_id):
	# Connect to the database 
	connection = mysql.connector.connect(user=mydb.user, 
                                        password=mydb.password,
                                        host='127.0.0.1',
                                        database=mydb.database
                                        )
	try:    
	    print (connection.is_connected())
	    db_Info = connection.get_server_info()
	    print("Connected to MySQL Server version ", db_Info)
	    cursor = connection.cursor(buffered=True)
	    cursor.execute("select database();")
	    record = cursor.fetchone()
	    print("You're connected to database: ", record)

	except:
		error['message'] = '資料庫連接錯誤'
		return (error)

	#Get information from db given attraction_id 
	attraction_id = attraction_id
	query = """SELECT id, name , address, images
					FROM spot
					WHERE id = %s """
	cursor.execute(query, (attraction_id,))
	entry = cursor.fetchone()
	print (entry)
	try:
		response = {"attraction_id":entry[0],
					"name":entry[1],
					"address":entry[2],
					"image":"https://" + entry[3].split('https://')[1]}
		return response

	except:
		return "Wrong given attraction_id"


"""
Database member data structure (id, name, email, hased_password, salt)
"""

# Tourist attractions search with GET method (page,keyword)
@app.route("/api/attractions", methods=["GET"])
def attractions():

	# Set the data structure of the response
	response = {"next_page":int(), "data":[]}
	error = {"error":True, "message":""}
	attraction = {'id':int(),
				'name':str(),
				'category':str(),
				'description':str(),
				'address':str(),
				'transport':str(),
				'mrt':str(),
				'lat':float(),
				'lng':float(),
				'images':[]
				}

	# Connect to the database 
	connection = mysql.connector.connect(user=mydb.user, 
                                        password=mydb.password,
                                        host='127.0.0.1',
                                        database=mydb.database
                                        )
	try:    
	    print (connection.is_connected())
	    db_Info = connection.get_server_info()
	    print("Connected to MySQL Server version ", db_Info)
	    cursor = connection.cursor(buffered=True)
	    cursor.execute("select database();")
	    record = cursor.fetchone()
	    print("You're connected to database: ", record)

	except:
		error['message'] = '資料庫連接錯誤'
		return (error)
	

	# Get information from the database (with or without keyword)
    # Data structure => tuple list [(id, name.....), (id, name.....), ...]
    # See the number of pages and if there is a next page
	keyword = request.args.get('keyword')
	page = request.args.get('page')
	page = int(page)
	row_num = int()
	if  keyword != None:
		keyword_name = '%' + request.args.get('keyword') + '%'
		keyword_cat = request.args.get('keyword')
		print (keyword)
		query = """SELECT id, name, category, description, address,
						direction, mrt, longitude, latitude, images
					FROM spot
					WHERE name LIKE %s 
						OR category = %s
					LIMIT %s, %s
						"""
		cursor.execute(query, (keyword_name, keyword_cat, page * 12, 12))
		entry = cursor.fetchall()
		
		# Get the value (row_num)
		query = """SELECT COUNT(*)
					FROM spot
					WHERE name LIKE %s 
						OR category = %s
					
						"""
		cursor.execute(query, (keyword_name, keyword_cat))
		row_num = cursor.fetchone()[0]
		
		
	
	else:
		query = """SELECT id, name, category, description, address,
						  direction, mrt, longitude, latitude, images
				   FROM spot
				   LIMIT %s, %s"""
		cursor.execute(query, (page *12, 12))
		entry = cursor.fetchall()

		# Get the value (row_num)
		query = """SELECT COUNT(*)
					FROM spot					
						"""
		cursor.execute(query)
		row_num = cursor.fetchone()[0]


	# Check if there is any information
	if len(entry) == 0:
		error['message'] = '無法取得任何資料'
		return (error)

	# Assign the value (next_page)
	page_num = row_num // 12 + 1

	if page + 1 < page_num:
		response['next_page'] = page + 1
	elif page + 1 == page_num:
		response['next_page'] = None

	# Combine the information from the database with the response
	for i in entry:
		attraction = {'id':int(),
				'name':str(),
				'category':str(),
				'description':str(),
				'address':str(),
				'transport':str(),
				'mrt':str(),
				'lat':float(),
				'lng':float(),
				'images':[]
				}

		count = 0
		for p in attraction.keys():
			
			# Make the images' values a list
			if p == 'images':
				for x in i[count].split('https')[1:]:
					attraction[p].append('https' + x)
			
			else:
				attraction[p] = i[count]

			count += 1

		response['data'].append(attraction)

	return jsonify(response)


@app.route("/api/attraction/<attraction_id>")
def attraction_api(attraction_id):

	# Set the data structure of the response
	response = {"data": dict()}
	error = {"error":True, "message":""}
	attraction = {'id':int(),
				'name':str(),
				'category':str(),
				'description':str(),
				'address':str(),
				'transport':str(),
				'mrt':str(),
				'lat':float(),
				'lng':float(),
				'images':[]
				}

	# Connect to the database 
	connection = mysql.connector.connect(user=mydb.user, 
                                        password=mydb.password,
                                        host='127.0.0.1',
                                        database=mydb.database
                                        )
	try:    
	    print (connection.is_connected())
	    db_Info = connection.get_server_info()
	    print("Connected to MySQL Server version ", db_Info)
	    cursor = connection.cursor(buffered=True)
	    cursor.execute("select database();")
	    record = cursor.fetchone()
	    print("You're connected to database: ", record)

	except:
		error['message'] = '資料庫無法連線'
		return (error)


	# Get the information from the database
	attraction_id = int(attraction_id)

	query = """SELECT id, name, category, description, address,
						  direction, mrt, longitude, latitude, images
				   FROM spot
				   WHERE id = %s"""

	try:
		cursor.execute(query, (attraction_id,))
		entry = cursor.fetchone()

	except:
		error['message'] = '景點編號不正確'
		return (error)

	count = 0	
	for i in attraction.keys():
		if i == 'images':
			for s in entry[count].split('https')[1:]:
				attraction[i].append('https' + s)

		else:
			attraction[i] = entry[count]
			count += 1
		
	response['data'] = attraction


	return jsonify(response)
	

# Return all the attraction categories 
@app.route("/api/categories")
def categories():

	# Set the data structure of the response
	response = {"data": []}
	error = {"error":True, "message":""}

	# Connect to the database 
	connection = mysql.connector.connect(user=mydb.user, 
                                        password=mydb.password,
                                        host='127.0.0.1',
                                        database=mydb.database
                                        )
	try:    
	    print (connection.is_connected())
	    db_Info = connection.get_server_info()
	    print("Connected to MySQL Server version ", db_Info)
	    cursor = connection.cursor(buffered=True)
	    cursor.execute("select database();")
	    record = cursor.fetchone()
	    print("You're connected to database: ", record)

	except:
		error['message'] = '資料庫無法連線'
		return (error)


	# Get all the attractions from the database
	query = """SELECT category FROM spot"""
	cursor.execute(query)
	entry = cursor.fetchall()	

	# Append the category into the list
	cat_list = []
	for i in entry:
		if i[0] not in cat_list:
			cat_list.append(i[0])

	# Combine the cat_list with response
	response['data'] = cat_list

	return jsonify(response)


#Registration of an account
@app.route("/api/user", methods = ["POST"])
def registration():

	# Set the data structure of the request and response
	response = {"ok": True}
	error = {"error":True, "message":""}

	# Connect to the database 
	connection = mysql.connector.connect(user=mydb.user, 
                                        password=mydb.password,
                                        host='127.0.0.1',
                                        database=mydb.database
                                        )
	try:    
	    print (connection.is_connected())
	    db_Info = connection.get_server_info()
	    print("Connected to MySQL Server version ", db_Info)
	    cursor = connection.cursor(buffered=True)
	    cursor.execute("select database();")
	    record = cursor.fetchone()
	    print("You're connected to database: ", record)

	except:
		error['message'] = '資料庫無法連線'
		return error


	#Define and get the form request (nm/ac/pw)
	name = request.get_json()['name']
	email = request.get_json()['email']
	password = request.get_json()['password']

	#Give error message if left blank
	if name == '' or email == '' or password == '':
		error['message'] = '請勿留空白'
		return error

	password = password.encode('utf-8')
	salt = bcrypt.gensalt()
	password = bcrypt.hashpw(password,salt)
	salt = salt.decode('utf-8')
	password = password.decode('utf-8')

    #Check if the email has been registered
	mycursor = connection.cursor(buffered=True)
	query = """Select email FROM member WHERE email = %s"""
	mycursor.execute(query, (email,))
	result = mycursor.fetchall()

	if len(result) != 0:
		error['message'] = "帳號已經存在"
		return error

	else:
		query = """INSERT INTO member (name, email, password, salt) VALUES (%s, %s, %s, %s)"""
		mycursor.execute(query, (name, email, password, salt))
		connection.commit()
		return response




@app.route("/api/user/auth", methods = ["GET", "PUT", "DELETE"])
def user_info():
	# Connect to the database 
	connection = mysql.connector.connect(user=mydb.user, 
                                        password=mydb.password,
                                        host='127.0.0.1',
                                        database=mydb.database
                                        )
	try:    
	    print (connection.is_connected())
	    db_Info = connection.get_server_info()
	    print("Connected to MySQL Server version ", db_Info)
	    cursor = connection.cursor(buffered=True)
	    cursor.execute("select database();")
	    record = cursor.fetchone()
	    print("You're connected to database: ", record)

	except:
		error['message'] = '資料庫連接錯誤'
		return (error)

	#Get the information of the user who has been logged into
	if request.method == "GET":
		response = {"data":{"id":None, "name":None, "email":None}}
		
		# Check login status
		try:	
			cookie = request.cookies.get('access_token')
			cookie_decoded = jwt.decode(cookie,'secret',algorithms="HS256")
		except:
			return response

		if cookie_decoded:
			email = jwt.decode(cookie,'secret',algorithms="HS256")['email']
			print ("this is the decoded", email)
			response['data']['id'] = getUserdbInfo(email)['id']
			response['data']['name'] = getUserdbInfo(email)['name']
			response['data']['email'] = getUserdbInfo(email)['email']
			return jsonify (response)
		else:
			return jsonify (response)

	#User login
	elif request.method == "PUT":
		error = {"error":True, "message":""}
		email = request.get_json()['email']
		password = request.get_json()['password']
		if email == '' or password == '':
			error['message'] = "請勿留空白"
			return error
		
		password = password.encode('utf-8')

		query = "SELECT * FROM member WHERE email =  %s"
		#Avoid "unread result error"
		mycursor = connection.cursor(buffered=True)

		#Process the password and the salt
		mycursor.execute(query, (email,))
		connection.commit()
		myresult = mycursor.fetchall()

		if len(myresult) == 1:
			salt = myresult[0][4]
			salt = salt.encode('utf-8')
			hashed_pw = bcrypt.hashpw(password,salt)
			hashed_pw = hashed_pw.decode('utf-8')

			if hashed_pw == myresult[0][3]: 
				#second let's do something with the cookie
				response = make_response({'msg': 'successfully logged in!'})
				access_token = jwt.encode({"email":email}, "secret", algorithm="HS256")
				response.headers['Access-Control-Allow-Credentials'] = True
				expire = datetime.datetime.now() + datetime.timedelta(days=7)
				response.set_cookie('access_token', value=access_token, expires = expire)
				print ('Great')
				return response
               
			else:
				error['message'] = "帳號密碼錯誤"
				return error

		else:
			error['message'] = "帳號密碼錯誤"
			return error


	#User logout
	elif request.method == "DELETE":	
		response = make_response({'msg': 'Logging you out!'})
		response.set_cookie('access_token', value='')
		return response
 

@app.route("/api/booking", methods = ["GET", "POST", "DELETE"])
def booking_api():
	# Connect to the database  
	connection = mysql.connector.connect(user=mydb.user, 
                                        password=mydb.password,
                                        host='127.0.0.1',
                                        database=mydb.database
                                        )
	try:    
	    print (connection.is_connected())
	    db_Info = connection.get_server_info()
	    print("Connected to MySQL Server version ", db_Info)
	    cursor = connection.cursor(buffered=True)
	    cursor.execute("select database();")
	    record = cursor.fetchone()
	    print("You're connected to database: ", record)

	except:
		error['message'] = '資料庫連接錯誤'
		return (error)

	#Get the information of booking not yet billed
	if request.method == "GET":
		response = {"data":{"attraction":{"id":None, "name":None, "address":None, "image":None}, 
							"date":None, "time":None, "price":None}}
		error = {"error":True, "message":""}

		# Check login status
		try:	
			cookie = request.cookies.get('access_token')
			cookie_decoded = jwt.decode(cookie,'secret',algorithms="HS256")
		except:
			error['message'] = '尚未登入'
			return jsonify (error)
		# Check login validity
		if cookie_decoded:
			email = cookie_decoded['email']
			booking_info = getBookingInfo(email)
			response['data']['date'] = booking_info['date']
			response['data']['time'] = booking_info['time']
			response['data']['price'] = booking_info['price']
			response['data']['attraction']['id'] = booking_info['attraction_id']
			if booking_info['attraction_id'] != None:
				attraction_id = booking_info['attraction_id']
				attraction_info = getAttractionInfo(attraction_id)
				response['data']['attraction']['name'] = attraction_info['name']
				response['data']['attraction']['address'] = attraction_info['address']
				response['data']['attraction']['image'] = attraction_info['image']
				return jsonify(response)
			else:
				return jsonify(response)

		else:
			error['message'] = '尚未登入'
			return jsonify (error)

	# Post a booking order to db
	elif request.method == "POST":
		response = {"ok": True}
		error = {"error": True, "message": ""}
		print ("Get the post message", request)
		# Check the login status
		try:	
			cookie = request.cookies.get('access_token')
			cookie_decoded = jwt.decode(cookie,'secret',algorithms="HS256")
		except:
			error['message'] = '尚未登入'
			return jsonify (error)
		# Check login validity
		if cookie_decoded:
			# Track the user by email
			print ("Authenticated successfully")
			email = cookie_decoded['email']
			attraction_id = request.get_json()['attractionId']
			date = request.get_json()['date']
			time = request.get_json()['time']
			price = request.get_json()['price']
			# Check if the email(user) has already booked
			try:
				if getBookingInfo(email)['attraction_id'] != None:
					print ("Ready to post information")
					query = """SET SQL_SAFE_UPDATES = 0"""
					cursor.execute(query)
					print ("Step one done")
					query = """UPDATE booking  
								SET attraction_id = %s, date_ = %s, time_ = %s, price = %s
							    WHERE email = %s;"""
					cursor.execute(query, (attraction_id, date, time, price, email))
					print ("Step two done")
					query = """SET SQL_SAFE_UPDATES = 1"""
					cursor.execute(query)
					connection.commit()
					print ("successfully posted")
					return jsonify(response)

				else:
					query = """INSERT INTO booking (attraction_id, date_, time_, price, email)
								VALUES (%s, %s, %s, %s, %s)
								"""
					cursor.execute(query, (attraction_id, date, time, price, email))
					connection.commit()
					print ("successfully posted")
					return jsonify(response)
		

			except:
				error['message'] = '建立失敗'
				return jsonify (error)

		else:
			error['message'] = '尚未登入'
			return jsonify (error)

	# Delete a booking in db
	elif request.method == "DELETE":
		response = {"ok": True}
		error = {"error": True, "message": ""}
		try:	
			cookie = request.cookies.get('access_token')
			cookie_decoded = jwt.decode(cookie,'secret',algorithms="HS256")
		except:
			error['message'] = '尚未登入'
			return jsonify (error)
		# Check login validity
		if cookie_decoded:
			email = cookie_decoded['email']
			try:
				query = """DELETE FROM booking WHERE email = %s"""
				cursor.execute(query, (email,))
				connection.commit()
				return jsonify(response)

			except:
				error['message'] = "刪除失敗"
				return jsonify(error)

		else:
			error['message'] = "尚未登入"
			return jsonify(error)
			

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

app.run(host='0.0.0.0', port=3000)