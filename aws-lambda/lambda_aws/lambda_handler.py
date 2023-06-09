import boto3
import pymysql
import csv
import pandas as pd

s3_cient = boto3.client('s3')

# Read CSV file content from S3 bucket
def read_data_from_s3(event):
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    s3_file_name = event["Records"][0]["s3"]["object"]["key"]
    print(f"Bucket Name: {bucket_name}, S3 File:  {s3_file_name}")
    resp = s3_cient.get_object(Bucket=bucket_name, Key=s3_file_name)

    # CSV -> Pandas Cleaning
    
    results = []
    
    match s3_file_name:
        case "student.csv":
            studentdf = pd.read_csv(resp['Body'], sep=',')
            studentdf = studentdf.drop(columns='Email')
            results = studentdf.values.tolist()
        case "teacher.csv":
            teacherdf = pd.read_csv(resp['Body'], sep=',')
            teacherdf = teacherdf.drop(columns='Email')
            results = teacherdf.values.tolist()
        case "admin.csv":
            admindf = pd.read_csv(resp['Body'], sep=',')
            admindf = admindf.drop(columns='Email')
            results = admindf.values.tolist()
        case "course.csv":
            coursedf = pd.read_csv(resp['Body'], sep=',')
            results = coursedf.values.tolist()
        case "grade.csv":
            gradesdf = pd.read_csv(resp['Body'], sep=',')
            gradesdf.rename(columns={'Grade ID': 'ID'}, inplace=True)
            results = gradesdf.values.tolist()

    print("----- Returning Cleaned and Parsed Data! -----")
    return (results, s3_file_name)

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

    # Lambda Function is called for every file uploaded
    insert_dict = {
        'student.csv': 'INSERT INTO student (id, name) VALUES (%s, %s)',
        'teacher.csv': 'INSERT INTO teacher (id, name) VALUES (%s, %s)',
        'admin.csv': 'INSERT INTO admin (id, name) VALUES (%s, %s)',
        'course.csv': 'INSERT INTO course (id, name, subject, teacher_id) VALUES (%s, %s, %s, %s)',
        'grade.csv': 'INSERT INTO grade (id, student_id, course_id, num_val) VALUES (%s, %s, %s, %s)'
    }

    with connection.cursor() as cursor:
        try:
            results, csv_file_name = read_data_from_s3(event)
            print(f"S3 Bucket and File Read: {csv_file_name}")

            if csv_file_name in insert_dict:
                insert_query = insert_dict[csv_file_name]
                # Enter record into SQL if contraints pass
                for record in results:
                    try:
                        cursor.execute(insert_query, record)
                        connection.commit()
                    except Exception as e:
                        pass

            print(cursor.rowcount, f"Record inserted successfully from {csv_file_name} file")

        except Exception as e:
            print(e)

    #     # Display teacher table records
    #     # for row in cur:
    #     #     print (row)
    if connection: #commit the execution
        connection.commit()
        print("Committing...")