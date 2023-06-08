import json
import boto3
import csv
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
s3_client = boto3.client('s3')

# Read CSV file content from S3 bucket
def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    csv_file = event['Records'][0]['s3']['object']['key']
    csv_file_obj = s3_client.get_object(Bucket=bucket, Key=csv_file)
    lines = csv_file_obj['Body'].read().decode('utf-8').split()
    
    results = []
    for row in csv.DictReader(lines):
        results.append(row.values())
    print(results)
    
    connection = mysql.connector.connect(host='xxxxxxxxxxxxxxx.ap-south-1.rds.amazonaws.com',database='employeedb',user='xxxxxx',password='xxxxxx')
    
    tables_dict = {
        'student': 'INSERT INTO table1 (empid, empname, empaddress) VALUES (%s, %s, %s)',
        'teacher': 'INSERT INTO table2 (empid, empname, empaddress) VALUES (%s, %s, %s)',
        'admin': 'INSERT INTO table5 (empid, empname, empaddress) VALUES (%s, %s, %s)',
        'course': 'INSERT INTO table3 (empid, empname, empaddress) VALUES (%s, %s, %s)',
        'grade': 'INSERT INTO table4 (empid, empname, empaddress) VALUES (%s, %s, %s)'
    }
    if csv_file in tables_dict:
        mysql_empsql_insert_query = tables_dict[csv_file]
        cursor = connection.cursor()
        cursor.executemany(mysql_empsql_insert_query,results)
        connection.commit()
        print(cursor.rowcount, f"Record inserted successfully from {csv_file} file")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
