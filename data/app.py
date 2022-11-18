# Python program to read
# json file


import json
import mysql.connector
# Opening JSON file
f = open('taipei-attractions.json',encoding="utf-8")

# returns JSON object as
# a dictionary
data = json.load(f)

# Iterating through the json
# list
#for i in data['result']['results']:
#	print(i)


#Redefine the data structure
"""name, category, rate, address, MRT
#direction, description, memo time, pictures"""

Attractions = []

Attraction = {
    'name':'',
    'category':'',
    'rate':'',
    'address':'',
    'MRT':'',
    'direction':'',
    'longitude':'',
    'latitude':'',
    'description':'',
    'memo_time':'',
    'pictures':'',
    }

#append every attraction as Dict to Attractions (list)

for i in data['result']['results']:
    #You need to empty the dict otherwise it cannot be updated
    Attraction = {
        'name':'',
        'category':'',
        'rate':'',
        'address':'',
        'MRT':'',
        'direction':'',
        'longitude':'',
        'latitude':'',
        'description':'',
        'memo_time':'',
        'pictures':'',
        }
    Attraction['name'] = i['name']
    Attraction['category'] = i['CAT']
    Attraction['rate'] = i['rate']
    Attraction['address'] = i['address']
    Attraction['MRT'] = i['MRT']
    Attraction['direction'] = i['direction']
    Attraction['longitude'] = i['longitude']
    Attraction['latitude'] = i['latitude']
    Attraction['description'] = i['description']
    Attraction['memo_time'] = i['MEMO_TIME']
    Attraction['pictures'] = i['file']
    Attractions.append(Attraction)



#Create a database class 
class Database:

    def __init__(self,user,password,database):
        self.user = user        
        self.password = password
        self.database = database

    def __repr__(self):
        return f'<Database: {self.database}>'

#Refer to the target database
mydb = Database('root','811223','taipei_tour')


#Connect the database
connection = mysql.connector.connect(user=mydb.user, 
                                password=mydb.password,
                                host='127.0.0.1',
                                database=mydb.database
                                )

try:    
    print (connection.is_connected())
    db_Info = connection.get_server_info()
    print("Connected to MySQL Server version ", db_Info)
    cursor = connection.cursor()
    cursor.execute("select database();")
    record = cursor.fetchone()
    print("You're connected to database: ", record)

except:
    print ("Error while connecting to MySQL")

#Create a Table
query = """CREATE TABLE spot (
    id bigint Primary Key auto_increment, 
    name varchar(255) NOT NULL,
    category varchar(255) NOT NULL,
    rate int not null default 0,
    address varchar(255) NOT NULL,
    mrt varchar(64),
    direction varchar(1000),
    longitude varchar(255),
    latitude varchar(255),
    description varchar(5000),
    memo_time varchar(1000),
    images varchar(5000)
    ) 
"""
cursor.execute(query)
connection.commit()   

#Import the data into the table
query = """INSERT INTO spot (name, category, rate, address, mrt, 
    direction, longitude, latitude, description, memo_time, images) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
print ('query read!')


##Convert the pictures list into String

for i in Attractions:
    print('Processing')
    cursor.execute(query, (i['name'], i['category'], i['rate'], i['address'], i['MRT'], 
                             i['direction'], i['longitude'], i['latitude'], i['description'],
                             i['memo_time'], i['pictures']))

connection.commit()    


print ('Done')
# Closing file
f.close()
