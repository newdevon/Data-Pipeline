import pymysql

# results = [(1,'Noah Johnson','noah.johnson@example.com'), (2,'Amelia Brown','amelia.brown@example.com'), (3,'Benjamin Green','benjamin.green@example.com'), (4,'Charlotte Jones','charlotte.jones@example.com'), (5,'Daniel Campbell','daniel.campbell@example.com'), (6,'Abigail Jones','abigail.jones@example.com')]

raw = ['ID,Name,Email\r', '1,Noah Johnson,noah.johnson@example.com\r', '2,Amelia Brown,amelia.brown@example.com\r', '3,Benjamin Green,benjamin.green@example.com\r', '4,Charlotte Jones,charlotte.jones@example.com\r', '5,Daniel Campbell,daniel.campbell@example.com\r', '6,Abigail Jones,abigail.jones@example.com\r', '7,Benjamin Brown,benjamin.brown@example.com\r', '8,Caroline Moore,caroline.moore@example.com\r', '9,Daniel Sander,daniel.sander@example.com\r', '10,Emily Davis,emily.davis@example.com\r', '11,Felicia Addams,felicia.addams@example.com\r', '12,Gabriel Sanchez,gabriel.sanchez@example.com\r', '13,Henry Lee,henry.lee@example.com\r', '14,Isabella Allen,isabella.allen@example.com\r', '15,James Kenn,james.kenn@example.com\r', '16,Edward Levine,edward.levine@example.com\r', '17,Clayton Peck,clayton.peck@example.com\r', '18,Cara Hernandez,cara.hernandez@example.com\r', '19,Adam Bell,adam.bell@example.com\r', '20,Kathy Valdez,kathy.valdez@example.com']

results = []
for i in range(1, len(raw)):
    row = raw[i].split(',')
    results.append(row)

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
    'student.csv': 'INSERT INTO student (id, name, email) VALUES (%s, %s, %s)',
    'teacher.csv': 'INSERT INTO teacher (id, name, email) VALUES (%s, %s, %s)',
    'admin.csv': 'INSERT INTO admin (id, name, email) VALUES (%s, %s, %s)',
    'course.csv': 'INSERT INTO course (id, name, teacher_id) VALUES (%s, %s, %s)',
    'grade.csv': 'INSERT INTO grade (id, student_id, course_id, num_val) VALUES (%s, %s, %s, %s)'
}

with connection.cursor() as cursor:
    try:
        results, csv_file_name = results, "admin.csv" 
        print(f"S3 Bucket and File Read: {csv_file_name}")

        if csv_file_name in insert_dict:
            insert_query = insert_dict[csv_file_name]
            print("------ failed executemany ------")
            cursor.executemany(insert_query, results)
            print("------ passed executemany ------")
            connection.commit()
            print(cursor.rowcount, f"Record inserted successfully from {csv_file_name} file")

        # if csv_file_name in insert_dict:
        #     insert_query = insert_dict[csv_file_name]
        #     print("------ fail before executemany ------")
        #     for record in results:
        #         print(record)
        #         print(record[2])
        #         print(type(record[2]))
        #         cursor.execute(insert_query, record)
        #         connection.commit()
        #     print("------ pass after executemany ------")
        #     print(cursor.rowcount, f"Record inserted successfully from {csv_file_name} file")
        
    
    except Exception as e:
        print(e)