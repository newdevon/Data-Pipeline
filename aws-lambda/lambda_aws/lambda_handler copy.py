import boto3
import pymysql

s3_cient = boto3.client('s3')

# Read CSV file content from S3 bucket
def read_data_from_s3(event):
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    s3_file_name = event["Records"][0]["s3"]["object"]["key"]
    print(f"Bucket Name: {bucket_name}, S3 File:  {s3_file_name}")
    resp = s3_cient.get_object(Bucket=bucket_name, Key=s3_file_name)

    data = resp['Body'].read().decode('utf-8')
    data = data.split("\n")
    return data

def lambda_handler(event, context):
    rds_endpoint  = "sms-db.cgu7tdjenxsr.us-east-2.rds.amazonaws.com"
    username = "admin"
    password = "mr15etQsxFxCZauiwjZF" # RDS Mysql password
    db_name = "school" # RDS MySQL DB name
    connection = None
    try:
        connection = pymysql.connect(host=rds_endpoint, user=username, passwd=password, db=db_name, connect_timeout=5)
    except pymysql.MySQLError as e:
        print("ERROR: Unexpected error: Could not connect to MySQL instance.")

    try:
        cursor = connection.cursor()

        sql_script1 = "DROP TABLE IF EXISTS teacher;" 
        cursor.execute(sql_script1)
        connection.commit() #commit the execution

        sql_script2 = "CREATE TABLE teacher (id SERIAL PRIMARY KEY, name varchar(50), email varchar(50));"
        cursor.execute(sql_script2)
        connection.commit() #commit the execution
        print("Created 'teacher' Table")
        
    except Exception as e:
        print(e)

    data = read_data_from_s3(event)

    with connection.cursor() as cur:
        for person in data: # Iterate over S3 csv file content and insert into MySQL database
            try:
                person = person.replace("\n","").split(",")
                #print(person)
                #print (">>>>>>>"+str(person))
                cur.execute('INSERT INTO teacher (name, email) VALUES ("'+str(person[1])+'", "'+str(person[2])+'")')
                connection.commit()
                #print("inserted record")
            except Exception as e:
                print(e)
                continue
        cur.execute("select * from teacher")
        # Display teacher table records
        # for row in cur:
        #     print (row)
    if connection:
        connection.commit()