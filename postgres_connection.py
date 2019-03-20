import psycopg2

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
