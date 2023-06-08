import mysql.connector
import config

#Set connection variable
rds_endpoint = config.rds_endpoint
database_name = config.db_name

try:
        connection = mysql.connector.connect(
                                            user=config.username,
                                            password=config.password,
                                            host=rds_endpoint,
                                            database=database_name
        )
        cursor = connection.cursor()

        sql_query1 = "DROP TABLE IF EXISTS student;" 
        cursor.execute(sql_query1)
        connection.commit() #commit the execution

        sql_query2 = "CREATE TABLE student (id SERIAL PRIMARY KEY, name varchar(50), email varchar(50));"
        cursor.execute(sql_query2)
        connection.commit()

        sql_query3 = "INSERT INTO student (name, email) VALUES ('John Doe', 'jd12@gmail.com');"
        cursor.execute(sql_query3)
        connection.commit()

        #SELECT aws_s3.table_import_from_s3('student','','(format csv)','(sfs-misc-data,data.csv,us-east-2)');"
        
        
        cursor.close() 
        connection.close()
        
except Exception as e:
    print(e)