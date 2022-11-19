from flask import *
import mysql.connector


app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True


# Create the database object
class Database:

    def __init__(self,user,password,database):
        self.user = user        
        self.password = password
        self.database = database

    def __repr__(self):
        return f'<Database: {self.database}>'

mydb = Database('root','811223','taipei_tour')


# Pages
@app.route("/")
def index():
	return render_template("index.html")

# Tourist attractions search with GET method (page,keyword)
@app.route("/api/attractions", methods=["GET"])
def attractions():
	
	# Set the formula with page numbers (input) and ids (outputs)
	"""page = request.args.get('page')
	page = int(page)
	attraction_ids = []
	for i in range(12):
		attraction_ids.append(page*12 + i)"""

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
	keyword = request.args.get('keyword')
	if  keyword != None:
		keyword_name = '%' + request.args.get('keyword') + '%'
		keyword_cat = request.args.get('keyword')
		print (keyword)
		query = """SELECT id, name, category, description, address,
						direction, mrt, longitude, latitude, images
					FROM spot
					WHERE name LIKE %s 
						OR category = %s
						"""
		cursor.execute(query, (keyword_name, keyword_cat))
		entry = cursor.fetchall()
	
	else:
		query = """SELECT id, name, category, description, address,
						  direction, mrt, longitude, latitude, images
				   FROM spot"""
		cursor.execute(query)
		entry = cursor.fetchall()



	# Calculate the number of rows 
	row_num = len(entry)
	print ("How many rows in the keyword search? ", len(entry))

	# Calculate the number of pages
	page_num = row_num // 12 + 1

	# Calculate the sequence numbers of each attraction in the page 
	# Assign each row to each page and define next_page value
	pg_entry = []
	attraction_row_num = []
	page = request.args.get('page')
	page = int(page)	

	if page < page_num - 1:
		for i in range(12):
			attraction_row_num.append(page*12 + i)
		response['next_page'] = page + 1
	elif page == page_num - 1:
		for i in range(page*12, row_num):
			attraction_row_num.append(i)
		response['next_page'] = None
	else:
		error['message'] = '頁數輸入超出範圍'
		return (error)

	# What if there isn't any information to display
	try:
		for i in entry[attraction_row_num[0]:attraction_row_num[-1] + 1]:
			pg_entry.append(i)
    
		print ("How many rows in the page? ", len(pg_entry))

	except:
		error['message'] = '無法取得任何資料'
		return (error)

	# Combine the information from the database with the response
	for i in pg_entry:
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
def attraction(attraction_id):

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

	# Combine the information with the response format
	"""attraction = {'id':int(),
				'name':str(),
				'category':str(),
				'description':str(),
				'address':str(),
				'transport':str(),
				'mrt':str(),
				'lat':float(),
				'lng':float(),
				'images':[]
				}"""
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
	#return render_template("attraction.html")

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

@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

app.run(port=3000)