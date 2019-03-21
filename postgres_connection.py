import psycopg2
from sqlalchemy import create_engine
import os
from os import environ
import secret

# There are two different manners in which python can connect to the postgres db.  One of them is psycopg2 and the other is sqlalchemy.  There are minor differences to both of them.

# This is the psycopg2 method

try:
    connection = psycopg2.connect(user = "sqlxamuciiofie",
                                  password = "86b317ef4be1dc74d800442ecdfe1447933e12298c36a5333d6a3fdfddc27b9d",
                                  host = "ec2-54-83-50-174.compute-1.amazonaws.com",
                                  port = "5432",
                                  database = "d33ltdp29n43i3")
    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print("Connection successful")     
    cursor.execute("SELECT * FROM users;") 
    record = cursor.fetchall()
    print(record)
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)


# This is the sqlalchemy method

user_database_url = environ.get('DATABASE_URL', secret.user_database_url)
engine = create_engine(user_database_url)
connection = engine.connect()
print("Connection using sqlalchemy is also successful")
result = connection.execute("select * from users")
for row in result:
    print("users:", row['email'])
connection.close()
