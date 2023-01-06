from flask import *
import mysql.connector
import bcrypt
import jwt
import datetime
import model
import requests
import json

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.secret_key = "Thisismysecretkey000000111111"

mydb = model.Database('root','811223','taipei_tour')

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


	# Get information from the database (with or without keyword)
    # Data structure => tuple list [(id, name.....), (id, name.....), ...]
    # See the number of pages and if there is a next page
	keyword = request.args.get('keyword')
	page = int(request.args.get('page'))
	row_num = int()
	if  keyword != None:
		keyword_name = '%' + request.args.get('keyword') + '%'
		keyword_cat = request.args.get('keyword')
		query = """SELECT id, name, category, description, address,
						direction, mrt, longitude, latitude, images
					FROM spot
					WHERE name LIKE %s 
						OR category = %s
					LIMIT %s, %s
						"""
		entry = mydb.commit_query(query, keyword_name, keyword_cat, page * 12, 12)
		
		# Get the value (row_num)
		query = """SELECT COUNT(*)
					FROM spot
					WHERE name LIKE %s 
						OR category = %s
					
						"""
		# first [0] => first item in fetchall(list)
		# second [0] => first item in the tuple(COUNT(*),....)
		row_num = mydb.commit_query(query, keyword_name, keyword_cat)[0][0]
		
	
	else:
		query = """SELECT id, name, category, description, address,
						  direction, mrt, longitude, latitude, images
				   FROM spot
				   LIMIT %s, %s"""
		entry = mydb.commit_query(query, page * 12, 12)

		# Get the value (row_num)
		query = """SELECT COUNT(*)
					FROM spot					
						"""
		row_num = mydb.commit_query(query)[0][0]


	# Check if there is any informatsion
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

	# Get the information from the database
	attraction_id = int(attraction_id)

	query = """SELECT id, name, category, description, address,
						  direction, mrt, longitude, latitude, images
				   FROM spot
				   WHERE id = %s"""

	try:
		entry = mydb.commit_query(query, attraction_id)[0]
		

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

	# Get all the attractions from the database
	query = """SELECT category FROM spot"""
	entry = mydb.commit_query("""SELECT category FROM spot""")	

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
	result = mydb.commit_query("""Select email FROM member WHERE email = %s""", email)

	if len(result) != 0:
		error['message'] = "帳號已經存在"
		return error

	else:
		query = """INSERT INTO member (name, email, password, salt) VALUES (%s, %s, %s, %s)"""
		mydb.commit_query(query, name, email, password, salt)
		return response




@app.route("/api/user/auth", methods = ["GET", "PUT", "DELETE"])
def user_info():
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
			result = mydb.getUserdbInfo(email)
			response['data'].update([('id',result['id']),
									('name',result['name']),
									('email',result['email'])])

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

		myresult = mydb.commit_query("SELECT * FROM member WHERE email =  %s", email)


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
			booking_info = mydb.getBookingInfo(email)
			response['data'].update([('date',booking_info['date']), 
									('time', booking_info['time']), 
									('price',booking_info['price'])])
			response['data']['attraction']['id'] = booking_info['attraction_id']
			if booking_info['attraction_id'] != None:
				attraction_id = booking_info['attraction_id']
				attraction_info = mydb.getAttractionInfo(attraction_id)
				response['data']['attraction'].update([('name', attraction_info['name']),
														('address',attraction_info['address']),
														('image', attraction_info['image'])])
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
				if mydb.getBookingInfo(email)['attraction_id'] != None:
					mydb.commit_query("SET SQL_SAFE_UPDATES = 0")
					query = """UPDATE booking  
								SET attraction_id = %s, 
								date_ = %s, 
								time_ = %s, 
								price = %s
							    WHERE email = %s;"""
					mydb.commit_query(query, attraction_id, date, time, price, email)
					mydb.commit_query("SET SQL_SAFE_UPDATES = 1")
					return jsonify(response)

				else:
					query = """INSERT INTO booking (attraction_id, date_, time_, price, email)
								VALUES (%s, %s, %s, %s, %s)
								"""
					mydb.commit_query(query, attraction_id, date, time, price, email)
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
				mydb.commit_query("""DELETE FROM booking WHERE email = %s""", email)
				return jsonify(response)

			except:
				error['message'] = "刪除失敗"
				return jsonify(error)

		else:
			error['message'] = "尚未登入"
			return jsonify(error)
			


@app.route("/api/orders", methods = ["GET", "POST"])
def order_api():

	#Send the purchase information to tappay server
	if request.method == "POST":
		error = {"error": True, "message": ""}
		request_body = request.get_json()
		
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
			user_email = cookie_decoded['email']
			print ("Authenticated successfully")

			# Define order number
			user_id = mydb.getUserdbInfo(user_email)['id']
			dt_string = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
			order_number = dt_string + str(user_id)

			# Get prime
			prime = request_body['prime']

			# Define order info
			attraction_id = request_body['order']['trip']['attraction']['id']
			attraction_name = request_body['order']['trip']['attraction']['name']
			attraction_address = request_body['order']['trip']['attraction']['address']
			attraction_image = request_body['order']['trip']['attraction']['image']
			price = int(request_body['order']['price'])		
			date = request_body['order']['trip']['date']
			time = request_body['order']['trip']['time']
			contact_name = request_body['order']['contact']['name']
			contact_email = request_body['order']['contact']['email']
			contact_mobile = request_body['order']['contact']['phone']

			# Set payment status as Not paid
			status = "未付款"

			# Feed the information into the db
			try:
				mydb.commit_query("""INSERT INTO ordering (order_number, 
															user_email,
															attraction_id,
															attraction_name,
															attraction_address,
															attraction_image,
															date_,
															time_,
															price,
															contact_name,
															contact_email,
															contact_mobile,
															status)
									 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
					   				""", order_number, user_email,attraction_id, attraction_name,
					   				attraction_address, attraction_image, date, time, price, contact_name,
					   				contact_email, contact_mobile, status)

			except:
				error['message'] = "訂單建立失敗"
				return jsonify(error)


			# Talk to TapPay Server
			tpurl = 'https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime'
			p_key = 'partner_u0naLA9KEkXKFSQ2ITGbLmALbZ7lox2m3bMrSyXo72YCsbpuYndbgOOL'
			merchant_id = 'vincejim91126_CTBC'
			tpheaders = {'Content-type':'application/json', 'x-api-key' : p_key}

			tpbody = {"prime": prime,
			        "partner_key": p_key,
			        "merchant_id": merchant_id,
			        "amount": price,
			        "details":"Tourist Attraction Guidance Fee",
			        "cardholder": {
			            "phone_number": contact_mobile,
			            "name": contact_name,
			            "email": contact_email,
			             },
			        "remember": False
			        } 
			        
			tpresponse = requests.post(tpurl, headers=tpheaders, json = tpbody)

			# If payment succeeds, send the message to the frontend
			if json.loads(tpresponse.text)['status'] == 0:
				response = {"data":{"number":order_number,
									"payment":{"status":0,
												"message":"付款成功"
												}
									}
							}


				# Update datebase status
				mydb.commit_query("""UPDATE ordering 
									 SET status = '已付款' 
									 WHERE order_number = %s""", order_number)

				# Delete booking info
				mydb.commit_query("""DELETE FROM booking WHERE email = %s""", user_email)


				return jsonify(response)


			else:
				response = {"data":{"number":order_number,
									"payment":{"status":1,
												"message":"付款失敗"
												}
									}
							}
				
				return jsonify(response)



		else:
			error['message'] = '登入狀態錯誤'
			return jsonify (error)



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