import json
import mysql.connector


"""Define the columns of the table "member" (id, name, email, password(hashed), seed)"""

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
query = """CREATE TABLE booking (
    id bigint Primary Key auto_increment, 
    attraction_id varchar(255) NOT NULL,
    date_ varchar(255) NOT NULL,
    time_ varchar(255) NOT NULL,
    price varchar(255) NOT NULL,
    email varchar(255) NOT NULL
    ) 
"""
cursor.execute(query)
connection.commit()   
